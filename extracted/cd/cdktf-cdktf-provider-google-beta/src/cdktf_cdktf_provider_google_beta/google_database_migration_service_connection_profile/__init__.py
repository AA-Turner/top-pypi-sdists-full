r'''
# `google_database_migration_service_connection_profile`

Refer to the Terraform Registry for docs: [`google_database_migration_service_connection_profile`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile).
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


class GoogleDatabaseMigrationServiceConnectionProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile google_database_migration_service_connection_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connection_profile_id: builtins.str,
        alloydb: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileAlloydb", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudsql: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileCloudsql", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        mysql: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileMysql", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileOracle", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfilePostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile google_database_migration_service_connection_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_profile_id: The ID of the connection profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#connection_profile_id GoogleDatabaseMigrationServiceConnectionProfile#connection_profile_id}
        :param alloydb: alloydb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#alloydb GoogleDatabaseMigrationServiceConnectionProfile#alloydb}
        :param cloudsql: cloudsql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cloudsql GoogleDatabaseMigrationServiceConnectionProfile#cloudsql}
        :param display_name: The connection profile display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#display_name GoogleDatabaseMigrationServiceConnectionProfile#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#id GoogleDatabaseMigrationServiceConnectionProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The resource labels for connection profile to use to annotate any related underlying resources such as Compute Engine VMs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#labels GoogleDatabaseMigrationServiceConnectionProfile#labels}
        :param location: The location where the connection profile should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#location GoogleDatabaseMigrationServiceConnectionProfile#location}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#mysql GoogleDatabaseMigrationServiceConnectionProfile#mysql}
        :param oracle: oracle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#oracle GoogleDatabaseMigrationServiceConnectionProfile#oracle}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#postgresql GoogleDatabaseMigrationServiceConnectionProfile#postgresql}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#project GoogleDatabaseMigrationServiceConnectionProfile#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#timeouts GoogleDatabaseMigrationServiceConnectionProfile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d01694ebbc906a04d387729c2bb0397561d102a003432bad9c18820bec51410b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDatabaseMigrationServiceConnectionProfileConfig(
            connection_profile_id=connection_profile_id,
            alloydb=alloydb,
            cloudsql=cloudsql,
            display_name=display_name,
            id=id,
            labels=labels,
            location=location,
            mysql=mysql,
            oracle=oracle,
            postgresql=postgresql,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleDatabaseMigrationServiceConnectionProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDatabaseMigrationServiceConnectionProfile to import.
        :param import_from_id: The id of the existing GoogleDatabaseMigrationServiceConnectionProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDatabaseMigrationServiceConnectionProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b280534fe0d863a3c1371af7e9ff782803ac7d615c41c3defcb28e23e74b048c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAlloydb")
    def put_alloydb(
        self,
        *,
        cluster_id: builtins.str,
        settings: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cluster_id: Required. The AlloyDB cluster ID that this connection profile is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cluster_id GoogleDatabaseMigrationServiceConnectionProfile#cluster_id}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#settings GoogleDatabaseMigrationServiceConnectionProfile#settings}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileAlloydb(
            cluster_id=cluster_id, settings=settings
        )

        return typing.cast(None, jsii.invoke(self, "putAlloydb", [value]))

    @jsii.member(jsii_name="putCloudsql")
    def put_cloudsql(
        self,
        *,
        settings: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#settings GoogleDatabaseMigrationServiceConnectionProfile#settings}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileCloudsql(
            settings=settings
        )

        return typing.cast(None, jsii.invoke(self, "putCloudsql", [value]))

    @jsii.member(jsii_name="putMysql")
    def put_mysql(
        self,
        *,
        cloud_sql_id: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        ssl: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_sql_id: If the source is a Cloud SQL database, use this field to provide the Cloud SQL instance ID of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cloud_sql_id GoogleDatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        :param host: The IP or hostname of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#host GoogleDatabaseMigrationServiceConnectionProfile#host}
        :param password: Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        :param port: The network port of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ssl GoogleDatabaseMigrationServiceConnectionProfile#ssl}
        :param username: The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileMysql(
            cloud_sql_id=cloud_sql_id,
            host=host,
            password=password,
            port=port,
            ssl=ssl,
            username=username,
        )

        return typing.cast(None, jsii.invoke(self, "putMysql", [value]))

    @jsii.member(jsii_name="putOracle")
    def put_oracle(
        self,
        *,
        database_service: builtins.str,
        host: builtins.str,
        password: builtins.str,
        port: jsii.Number,
        username: builtins.str,
        forward_ssh_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        private_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileOracleSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        static_service_ip_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_service: Required. Database service for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_service GoogleDatabaseMigrationServiceConnectionProfile#database_service}
        :param host: Required. The IP or hostname of the source Oracle database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#host GoogleDatabaseMigrationServiceConnectionProfile#host}
        :param password: Required. Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        :param port: Required. The network port of the source Oracle database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        :param username: Required. The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        :param forward_ssh_connectivity: forward_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#forward_ssh_connectivity GoogleDatabaseMigrationServiceConnectionProfile#forward_ssh_connectivity}
        :param private_connectivity: private_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_connectivity GoogleDatabaseMigrationServiceConnectionProfile#private_connectivity}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ssl GoogleDatabaseMigrationServiceConnectionProfile#ssl}
        :param static_service_ip_connectivity: static_service_ip_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#static_service_ip_connectivity GoogleDatabaseMigrationServiceConnectionProfile#static_service_ip_connectivity}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileOracle(
            database_service=database_service,
            host=host,
            password=password,
            port=port,
            username=username,
            forward_ssh_connectivity=forward_ssh_connectivity,
            private_connectivity=private_connectivity,
            ssl=ssl,
            static_service_ip_connectivity=static_service_ip_connectivity,
        )

        return typing.cast(None, jsii.invoke(self, "putOracle", [value]))

    @jsii.member(jsii_name="putPostgresql")
    def put_postgresql(
        self,
        *,
        alloydb_cluster_id: typing.Optional[builtins.str] = None,
        cloud_sql_id: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        ssl: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alloydb_cluster_id: If the connected database is an AlloyDB instance, use this field to provide the AlloyDB cluster ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#alloydb_cluster_id GoogleDatabaseMigrationServiceConnectionProfile#alloydb_cluster_id}
        :param cloud_sql_id: If the source is a Cloud SQL database, use this field to provide the Cloud SQL instance ID of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cloud_sql_id GoogleDatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        :param host: The IP or hostname of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#host GoogleDatabaseMigrationServiceConnectionProfile#host}
        :param password: Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        :param port: The network port of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ssl GoogleDatabaseMigrationServiceConnectionProfile#ssl}
        :param username: The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfilePostgresql(
            alloydb_cluster_id=alloydb_cluster_id,
            cloud_sql_id=cloud_sql_id,
            host=host,
            password=password,
            port=port,
            ssl=ssl,
            username=username,
        )

        return typing.cast(None, jsii.invoke(self, "putPostgresql", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#create GoogleDatabaseMigrationServiceConnectionProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#delete GoogleDatabaseMigrationServiceConnectionProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#update GoogleDatabaseMigrationServiceConnectionProfile#update}.
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAlloydb")
    def reset_alloydb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlloydb", []))

    @jsii.member(jsii_name="resetCloudsql")
    def reset_cloudsql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudsql", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMysql")
    def reset_mysql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysql", []))

    @jsii.member(jsii_name="resetOracle")
    def reset_oracle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracle", []))

    @jsii.member(jsii_name="resetPostgresql")
    def reset_postgresql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresql", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="alloydb")
    def alloydb(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileAlloydbOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileAlloydbOutputReference", jsii.get(self, "alloydb"))

    @builtins.property
    @jsii.member(jsii_name="cloudsql")
    def cloudsql(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileCloudsqlOutputReference", jsii.get(self, "cloudsql"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dbprovider")
    def dbprovider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbprovider"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(self) -> "GoogleDatabaseMigrationServiceConnectionProfileErrorList":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileErrorList", jsii.get(self, "error"))

    @builtins.property
    @jsii.member(jsii_name="mysql")
    def mysql(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileMysqlOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileMysqlOutputReference", jsii.get(self, "mysql"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="oracle")
    def oracle(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileOracleOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileOracleOutputReference", jsii.get(self, "oracle"))

    @builtins.property
    @jsii.member(jsii_name="postgresql")
    def postgresql(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfilePostgresqlOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfilePostgresqlOutputReference", jsii.get(self, "postgresql"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileTimeoutsOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="alloydbInput")
    def alloydb_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileAlloydb"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileAlloydb"], jsii.get(self, "alloydbInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudsqlInput")
    def cloudsql_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileCloudsql"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileCloudsql"], jsii.get(self, "cloudsqlInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionProfileIdInput")
    def connection_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

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
    @jsii.member(jsii_name="mysqlInput")
    def mysql_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileMysql"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileMysql"], jsii.get(self, "mysqlInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleInput")
    def oracle_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracle"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracle"], jsii.get(self, "oracleInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlInput")
    def postgresql_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfilePostgresql"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfilePostgresql"], jsii.get(self, "postgresqlInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDatabaseMigrationServiceConnectionProfileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDatabaseMigrationServiceConnectionProfileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionProfileId")
    def connection_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionProfileId"))

    @connection_profile_id.setter
    def connection_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5aba8a74ed9411562733e08f2798c3bb378561e8d0f211585b07d18711f5d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionProfileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9503b6f4071608a7dd5915d6019e7a5de5da17b05ba7269e39ed9fd8f5f94c9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05a9971dca939fff137ce1617b551bf3b199ba1196577f76c81a729f3de8a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d2b25f3bc4fcccca54d27b11fab45417ad504bfd4514ccdd10bfb90e6986f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f798246b745c6e830e1620e9216d9a79b1b16281d9b3efb124fa20df2c8e404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5cf6459a3ef0fe7f32c39296420262c2cd87dfaa9b2530ac1358de157a5ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileAlloydb",
    jsii_struct_bases=[],
    name_mapping={"cluster_id": "clusterId", "settings": "settings"},
)
class GoogleDatabaseMigrationServiceConnectionProfileAlloydb:
    def __init__(
        self,
        *,
        cluster_id: builtins.str,
        settings: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cluster_id: Required. The AlloyDB cluster ID that this connection profile is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cluster_id GoogleDatabaseMigrationServiceConnectionProfile#cluster_id}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#settings GoogleDatabaseMigrationServiceConnectionProfile#settings}
        '''
        if isinstance(settings, dict):
            settings = GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings(**settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ed60f604f611ea059c7f5372d01b108149cde18e193e36b75d2658e018de97)
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
        }
        if settings is not None:
            self._values["settings"] = settings

    @builtins.property
    def cluster_id(self) -> builtins.str:
        '''Required. The AlloyDB cluster ID that this connection profile is associated with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cluster_id GoogleDatabaseMigrationServiceConnectionProfile#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings"]:
        '''settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#settings GoogleDatabaseMigrationServiceConnectionProfile#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileAlloydb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileAlloydbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileAlloydbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__561e2d121fd7aafc330f71371f3fe9f5130b146d9c93142ef05e31fdd69b2e16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        *,
        initial_user: typing.Union["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser", typing.Dict[builtins.str, typing.Any]],
        vpc_network: builtins.str,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        primary_instance_settings: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param initial_user: initial_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#initial_user GoogleDatabaseMigrationServiceConnectionProfile#initial_user}
        :param vpc_network: Required. The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP. The network must belong to the same project as the cluster. It is specified in the form: 'projects/{project_number}/global/networks/{network_id}'. This is required to create a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#vpc_network GoogleDatabaseMigrationServiceConnectionProfile#vpc_network}
        :param labels: Labels for the AlloyDB cluster created by DMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#labels GoogleDatabaseMigrationServiceConnectionProfile#labels}
        :param primary_instance_settings: primary_instance_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#primary_instance_settings GoogleDatabaseMigrationServiceConnectionProfile#primary_instance_settings}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings(
            initial_user=initial_user,
            vpc_network=vpc_network,
            labels=labels,
            primary_instance_settings=primary_instance_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putSettings", [value]))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings"], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a561378881ade5485c30199d28e945d958fb3c3ad2e91baac7c989aa8c1b08fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydb]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6afdb8b214f817e4da2284b7444cfdd2f57731a3704030b3ea7017ea053b4e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings",
    jsii_struct_bases=[],
    name_mapping={
        "initial_user": "initialUser",
        "vpc_network": "vpcNetwork",
        "labels": "labels",
        "primary_instance_settings": "primaryInstanceSettings",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings:
    def __init__(
        self,
        *,
        initial_user: typing.Union["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser", typing.Dict[builtins.str, typing.Any]],
        vpc_network: builtins.str,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        primary_instance_settings: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param initial_user: initial_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#initial_user GoogleDatabaseMigrationServiceConnectionProfile#initial_user}
        :param vpc_network: Required. The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP. The network must belong to the same project as the cluster. It is specified in the form: 'projects/{project_number}/global/networks/{network_id}'. This is required to create a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#vpc_network GoogleDatabaseMigrationServiceConnectionProfile#vpc_network}
        :param labels: Labels for the AlloyDB cluster created by DMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#labels GoogleDatabaseMigrationServiceConnectionProfile#labels}
        :param primary_instance_settings: primary_instance_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#primary_instance_settings GoogleDatabaseMigrationServiceConnectionProfile#primary_instance_settings}
        '''
        if isinstance(initial_user, dict):
            initial_user = GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser(**initial_user)
        if isinstance(primary_instance_settings, dict):
            primary_instance_settings = GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings(**primary_instance_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b237996364b1436c83592ecd73b155c4b52fae3c77210288526e9a6136a9ee)
            check_type(argname="argument initial_user", value=initial_user, expected_type=type_hints["initial_user"])
            check_type(argname="argument vpc_network", value=vpc_network, expected_type=type_hints["vpc_network"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument primary_instance_settings", value=primary_instance_settings, expected_type=type_hints["primary_instance_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "initial_user": initial_user,
            "vpc_network": vpc_network,
        }
        if labels is not None:
            self._values["labels"] = labels
        if primary_instance_settings is not None:
            self._values["primary_instance_settings"] = primary_instance_settings

    @builtins.property
    def initial_user(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser":
        '''initial_user block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#initial_user GoogleDatabaseMigrationServiceConnectionProfile#initial_user}
        '''
        result = self._values.get("initial_user")
        assert result is not None, "Required property 'initial_user' is missing"
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser", result)

    @builtins.property
    def vpc_network(self) -> builtins.str:
        '''Required.

        The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP. The network must belong to the same project as the cluster.
        It is specified in the form: 'projects/{project_number}/global/networks/{network_id}'. This is required to create a cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#vpc_network GoogleDatabaseMigrationServiceConnectionProfile#vpc_network}
        '''
        result = self._values.get("vpc_network")
        assert result is not None, "Required property 'vpc_network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels for the AlloyDB cluster created by DMS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#labels GoogleDatabaseMigrationServiceConnectionProfile#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def primary_instance_settings(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings"]:
        '''primary_instance_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#primary_instance_settings GoogleDatabaseMigrationServiceConnectionProfile#primary_instance_settings}
        '''
        result = self._values.get("primary_instance_settings")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "user": "user"},
)
class GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser:
    def __init__(self, *, password: builtins.str, user: builtins.str) -> None:
        '''
        :param password: The initial password for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        :param user: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#user GoogleDatabaseMigrationServiceConnectionProfile#user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a09d034e16cfb8541b1b40673b92eb8dd64f11abfecddc68f104c0b907d2209)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "user": user,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''The initial password for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user(self) -> builtins.str:
        '''The database username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#user GoogleDatabaseMigrationServiceConnectionProfile#user}
        '''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7459fc148fcd63a82a1ba2b96ef13b883ce11cf663f0ffa27395560788a05f86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordSet")
    def password_set(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "passwordSet"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9298a9c865503f843f57f7fcb8abe8724ac7ca18c55fa099882a1ab1cac2fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd22c25ed0346ed495eab2110b44ed6de38b1db4a81f66a2a92aef5bd1615d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b048f8a6a891b6b05127693af64b78cef1ab4cd326e86880f891ab0d7b1c1f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f51f0d2b97af3d75f78eb9bc7e74983da14c9830e38be434d49b1ed60c6c524)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInitialUser")
    def put_initial_user(self, *, password: builtins.str, user: builtins.str) -> None:
        '''
        :param password: The initial password for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        :param user: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#user GoogleDatabaseMigrationServiceConnectionProfile#user}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser(
            password=password, user=user
        )

        return typing.cast(None, jsii.invoke(self, "putInitialUser", [value]))

    @jsii.member(jsii_name="putPrimaryInstanceSettings")
    def put_primary_instance_settings(
        self,
        *,
        id: builtins.str,
        machine_config: typing.Union["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig", typing.Dict[builtins.str, typing.Any]],
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#id GoogleDatabaseMigrationServiceConnectionProfile#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param machine_config: machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#machine_config GoogleDatabaseMigrationServiceConnectionProfile#machine_config}
        :param database_flags: Database flags to pass to AlloyDB when DMS is creating the AlloyDB cluster and instances. See the AlloyDB documentation for how these can be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_flags GoogleDatabaseMigrationServiceConnectionProfile#database_flags}
        :param labels: Labels for the AlloyDB primary instance created by DMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#labels GoogleDatabaseMigrationServiceConnectionProfile#labels}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings(
            id=id,
            machine_config=machine_config,
            database_flags=database_flags,
            labels=labels,
        )

        return typing.cast(None, jsii.invoke(self, "putPrimaryInstanceSettings", [value]))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetPrimaryInstanceSettings")
    def reset_primary_instance_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryInstanceSettings", []))

    @builtins.property
    @jsii.member(jsii_name="initialUser")
    def initial_user(
        self,
    ) -> GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUserOutputReference:
        return typing.cast(GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUserOutputReference, jsii.get(self, "initialUser"))

    @builtins.property
    @jsii.member(jsii_name="primaryInstanceSettings")
    def primary_instance_settings(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsOutputReference", jsii.get(self, "primaryInstanceSettings"))

    @builtins.property
    @jsii.member(jsii_name="initialUserInput")
    def initial_user_input(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser], jsii.get(self, "initialUserInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryInstanceSettingsInput")
    def primary_instance_settings_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings"], jsii.get(self, "primaryInstanceSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkInput")
    def vpc_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2d25dbf3b61654f97c834b8e02a4438e084c2f0c75fc8cabc9814b79d9b4b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcNetwork")
    def vpc_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcNetwork"))

    @vpc_network.setter
    def vpc_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897930971619b82a245d1b267080f8fab188102e15dd33fa8bf959be8aee52da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822bafd5c8fd5d5c5f651653453b1204589b9fbfa27cfb63e1acdb90609e4b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "machine_config": "machineConfig",
        "database_flags": "databaseFlags",
        "labels": "labels",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings:
    def __init__(
        self,
        *,
        id: builtins.str,
        machine_config: typing.Union["GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig", typing.Dict[builtins.str, typing.Any]],
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#id GoogleDatabaseMigrationServiceConnectionProfile#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param machine_config: machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#machine_config GoogleDatabaseMigrationServiceConnectionProfile#machine_config}
        :param database_flags: Database flags to pass to AlloyDB when DMS is creating the AlloyDB cluster and instances. See the AlloyDB documentation for how these can be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_flags GoogleDatabaseMigrationServiceConnectionProfile#database_flags}
        :param labels: Labels for the AlloyDB primary instance created by DMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#labels GoogleDatabaseMigrationServiceConnectionProfile#labels}
        '''
        if isinstance(machine_config, dict):
            machine_config = GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig(**machine_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a119c5bf9a64a0e2059b4761cbdfd7eb202974deb4a90214ca0ab3a34f442e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument machine_config", value=machine_config, expected_type=type_hints["machine_config"])
            check_type(argname="argument database_flags", value=database_flags, expected_type=type_hints["database_flags"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "machine_config": machine_config,
        }
        if database_flags is not None:
            self._values["database_flags"] = database_flags
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def id(self) -> builtins.str:
        '''The database username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#id GoogleDatabaseMigrationServiceConnectionProfile#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def machine_config(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig":
        '''machine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#machine_config GoogleDatabaseMigrationServiceConnectionProfile#machine_config}
        '''
        result = self._values.get("machine_config")
        assert result is not None, "Required property 'machine_config' is missing"
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig", result)

    @builtins.property
    def database_flags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Database flags to pass to AlloyDB when DMS is creating the AlloyDB cluster and instances.

        See the AlloyDB documentation for how these can be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_flags GoogleDatabaseMigrationServiceConnectionProfile#database_flags}
        '''
        result = self._values.get("database_flags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels for the AlloyDB primary instance created by DMS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#labels GoogleDatabaseMigrationServiceConnectionProfile#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig",
    jsii_struct_bases=[],
    name_mapping={"cpu_count": "cpuCount"},
)
class GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig:
    def __init__(self, *, cpu_count: jsii.Number) -> None:
        '''
        :param cpu_count: The number of CPU's in the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cpu_count GoogleDatabaseMigrationServiceConnectionProfile#cpu_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d5af29c3090bd9145e70f9825d44c53dd5c3fa49cda348f7e9c886eeabd5ce)
            check_type(argname="argument cpu_count", value=cpu_count, expected_type=type_hints["cpu_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu_count": cpu_count,
        }

    @builtins.property
    def cpu_count(self) -> jsii.Number:
        '''The number of CPU's in the VM instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cpu_count GoogleDatabaseMigrationServiceConnectionProfile#cpu_count}
        '''
        result = self._values.get("cpu_count")
        assert result is not None, "Required property 'cpu_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1238846c4798a42c015cc35e4f260f1e97f5dfc358401aa0895e87fb3102e261)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cpuCountInput")
    def cpu_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuCountInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCount")
    def cpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCount"))

    @cpu_count.setter
    def cpu_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9dc289afd9f8c98290f4c502aa6570640343932f8484468dbe0aed218db545e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d414c5f6afe12219b040827bb992802a2a57d6a2fec597fb8079754820f9ad03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f6bbae32a13b30f13e1d268f3e0f3ec01470dbc685aff092db6195a9b612839)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMachineConfig")
    def put_machine_config(self, *, cpu_count: jsii.Number) -> None:
        '''
        :param cpu_count: The number of CPU's in the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cpu_count GoogleDatabaseMigrationServiceConnectionProfile#cpu_count}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig(
            cpu_count=cpu_count
        )

        return typing.cast(None, jsii.invoke(self, "putMachineConfig", [value]))

    @jsii.member(jsii_name="resetDatabaseFlags")
    def reset_database_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseFlags", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @builtins.property
    @jsii.member(jsii_name="machineConfig")
    def machine_config(
        self,
    ) -> GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfigOutputReference:
        return typing.cast(GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfigOutputReference, jsii.get(self, "machineConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="databaseFlagsInput")
    def database_flags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "databaseFlagsInput"))

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
    @jsii.member(jsii_name="machineConfigInput")
    def machine_config_input(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig], jsii.get(self, "machineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseFlags")
    def database_flags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "databaseFlags"))

    @database_flags.setter
    def database_flags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6cddb654d4b1b52dd503aa05881c3d9eefa0a479383435bfc5857555b5df8b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseFlags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a31eda4f3c5f3596390aef1e6f255e8440ed77042a8f54fecfb803bc6b8a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e351fc34a6acbe42a718c96990dac09fa66a90f22eed9925c1c039aa7a066e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f1d6235a82c51a124064e64e207377397f7e26c3b4e7fb5587bc731952a722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileCloudsql",
    jsii_struct_bases=[],
    name_mapping={"settings": "settings"},
)
class GoogleDatabaseMigrationServiceConnectionProfileCloudsql:
    def __init__(
        self,
        *,
        settings: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#settings GoogleDatabaseMigrationServiceConnectionProfile#settings}
        '''
        if isinstance(settings, dict):
            settings = GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings(**settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1635efb9aab433e8e957214265cba858148ff1f8c9647b0f74649bf2119e7bf6)
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if settings is not None:
            self._values["settings"] = settings

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings"]:
        '''settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#settings GoogleDatabaseMigrationServiceConnectionProfile#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileCloudsql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileCloudsqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileCloudsqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6b372c6b22bd8c4e3865c635ef609d06560fd17c0a5b520eed5c74c3e4f6148)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        *,
        source_id: builtins.str,
        activation_policy: typing.Optional[builtins.str] = None,
        auto_storage_increase: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cmek_key_name: typing.Optional[builtins.str] = None,
        collation: typing.Optional[builtins.str] = None,
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        database_version: typing.Optional[builtins.str] = None,
        data_disk_size_gb: typing.Optional[builtins.str] = None,
        data_disk_type: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        ip_config: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_password: typing.Optional[builtins.str] = None,
        storage_auto_resize_limit: typing.Optional[builtins.str] = None,
        tier: typing.Optional[builtins.str] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_id: The Database Migration Service source connection profile ID, in the format: projects/my_project_name/locations/us-central1/connectionProfiles/connection_profile_ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#source_id GoogleDatabaseMigrationServiceConnectionProfile#source_id}
        :param activation_policy: The activation policy specifies when the instance is activated; it is applicable only when the instance state is 'RUNNABLE'. Possible values: ["ALWAYS", "NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#activation_policy GoogleDatabaseMigrationServiceConnectionProfile#activation_policy}
        :param auto_storage_increase: If you enable this setting, Cloud SQL checks your available storage every 30 seconds. If the available storage falls below a threshold size, Cloud SQL automatically adds additional storage capacity. If the available storage repeatedly falls below the threshold size, Cloud SQL continues to add storage until it reaches the maximum of 30 TB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#auto_storage_increase GoogleDatabaseMigrationServiceConnectionProfile#auto_storage_increase}
        :param cmek_key_name: The KMS key name used for the csql instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cmek_key_name GoogleDatabaseMigrationServiceConnectionProfile#cmek_key_name}
        :param collation: The Cloud SQL default instance level collation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#collation GoogleDatabaseMigrationServiceConnectionProfile#collation}
        :param database_flags: The database flags passed to the Cloud SQL instance at startup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_flags GoogleDatabaseMigrationServiceConnectionProfile#database_flags}
        :param database_version: The database engine type and version. Currently supported values located at https://cloud.google.com/database-migration/docs/reference/rest/v1/projects.locations.connectionProfiles#sqldatabaseversion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_version GoogleDatabaseMigrationServiceConnectionProfile#database_version}
        :param data_disk_size_gb: The storage capacity available to the database, in GB. The minimum (and default) size is 10GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#data_disk_size_gb GoogleDatabaseMigrationServiceConnectionProfile#data_disk_size_gb}
        :param data_disk_type: The type of storage. Possible values: ["PD_SSD", "PD_HDD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#data_disk_type GoogleDatabaseMigrationServiceConnectionProfile#data_disk_type}
        :param edition: The edition of the given Cloud SQL instance. Possible values: ["ENTERPRISE", "ENTERPRISE_PLUS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#edition GoogleDatabaseMigrationServiceConnectionProfile#edition}
        :param ip_config: ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ip_config GoogleDatabaseMigrationServiceConnectionProfile#ip_config}
        :param root_password: Input only. Initial root password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#root_password GoogleDatabaseMigrationServiceConnectionProfile#root_password}
        :param storage_auto_resize_limit: The maximum size to which storage capacity can be automatically increased. The default value is 0, which specifies that there is no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#storage_auto_resize_limit GoogleDatabaseMigrationServiceConnectionProfile#storage_auto_resize_limit}
        :param tier: The tier (or machine type) for this instance, for example: db-n1-standard-1 (MySQL instances) or db-custom-1-3840 (PostgreSQL instances). For more information, see https://cloud.google.com/sql/docs/mysql/instance-settings Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#tier GoogleDatabaseMigrationServiceConnectionProfile#tier}
        :param user_labels: The resource labels for a Cloud SQL instance to use to annotate any related underlying resources such as Compute Engine VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#user_labels GoogleDatabaseMigrationServiceConnectionProfile#user_labels}
        :param zone: The Google Cloud Platform zone where your Cloud SQL datdabse instance is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#zone GoogleDatabaseMigrationServiceConnectionProfile#zone}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings(
            source_id=source_id,
            activation_policy=activation_policy,
            auto_storage_increase=auto_storage_increase,
            cmek_key_name=cmek_key_name,
            collation=collation,
            database_flags=database_flags,
            database_version=database_version,
            data_disk_size_gb=data_disk_size_gb,
            data_disk_type=data_disk_type,
            edition=edition,
            ip_config=ip_config,
            root_password=root_password,
            storage_auto_resize_limit=storage_auto_resize_limit,
            tier=tier,
            user_labels=user_labels,
            zone=zone,
        )

        return typing.cast(None, jsii.invoke(self, "putSettings", [value]))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlId")
    def cloud_sql_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudSqlId"))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings"], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsql]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c751730ef3ce4c84d496a7110a72eaca40e1294e59165021d1b7daa1141d9ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings",
    jsii_struct_bases=[],
    name_mapping={
        "source_id": "sourceId",
        "activation_policy": "activationPolicy",
        "auto_storage_increase": "autoStorageIncrease",
        "cmek_key_name": "cmekKeyName",
        "collation": "collation",
        "database_flags": "databaseFlags",
        "database_version": "databaseVersion",
        "data_disk_size_gb": "dataDiskSizeGb",
        "data_disk_type": "dataDiskType",
        "edition": "edition",
        "ip_config": "ipConfig",
        "root_password": "rootPassword",
        "storage_auto_resize_limit": "storageAutoResizeLimit",
        "tier": "tier",
        "user_labels": "userLabels",
        "zone": "zone",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings:
    def __init__(
        self,
        *,
        source_id: builtins.str,
        activation_policy: typing.Optional[builtins.str] = None,
        auto_storage_increase: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cmek_key_name: typing.Optional[builtins.str] = None,
        collation: typing.Optional[builtins.str] = None,
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        database_version: typing.Optional[builtins.str] = None,
        data_disk_size_gb: typing.Optional[builtins.str] = None,
        data_disk_type: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        ip_config: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_password: typing.Optional[builtins.str] = None,
        storage_auto_resize_limit: typing.Optional[builtins.str] = None,
        tier: typing.Optional[builtins.str] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_id: The Database Migration Service source connection profile ID, in the format: projects/my_project_name/locations/us-central1/connectionProfiles/connection_profile_ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#source_id GoogleDatabaseMigrationServiceConnectionProfile#source_id}
        :param activation_policy: The activation policy specifies when the instance is activated; it is applicable only when the instance state is 'RUNNABLE'. Possible values: ["ALWAYS", "NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#activation_policy GoogleDatabaseMigrationServiceConnectionProfile#activation_policy}
        :param auto_storage_increase: If you enable this setting, Cloud SQL checks your available storage every 30 seconds. If the available storage falls below a threshold size, Cloud SQL automatically adds additional storage capacity. If the available storage repeatedly falls below the threshold size, Cloud SQL continues to add storage until it reaches the maximum of 30 TB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#auto_storage_increase GoogleDatabaseMigrationServiceConnectionProfile#auto_storage_increase}
        :param cmek_key_name: The KMS key name used for the csql instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cmek_key_name GoogleDatabaseMigrationServiceConnectionProfile#cmek_key_name}
        :param collation: The Cloud SQL default instance level collation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#collation GoogleDatabaseMigrationServiceConnectionProfile#collation}
        :param database_flags: The database flags passed to the Cloud SQL instance at startup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_flags GoogleDatabaseMigrationServiceConnectionProfile#database_flags}
        :param database_version: The database engine type and version. Currently supported values located at https://cloud.google.com/database-migration/docs/reference/rest/v1/projects.locations.connectionProfiles#sqldatabaseversion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_version GoogleDatabaseMigrationServiceConnectionProfile#database_version}
        :param data_disk_size_gb: The storage capacity available to the database, in GB. The minimum (and default) size is 10GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#data_disk_size_gb GoogleDatabaseMigrationServiceConnectionProfile#data_disk_size_gb}
        :param data_disk_type: The type of storage. Possible values: ["PD_SSD", "PD_HDD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#data_disk_type GoogleDatabaseMigrationServiceConnectionProfile#data_disk_type}
        :param edition: The edition of the given Cloud SQL instance. Possible values: ["ENTERPRISE", "ENTERPRISE_PLUS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#edition GoogleDatabaseMigrationServiceConnectionProfile#edition}
        :param ip_config: ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ip_config GoogleDatabaseMigrationServiceConnectionProfile#ip_config}
        :param root_password: Input only. Initial root password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#root_password GoogleDatabaseMigrationServiceConnectionProfile#root_password}
        :param storage_auto_resize_limit: The maximum size to which storage capacity can be automatically increased. The default value is 0, which specifies that there is no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#storage_auto_resize_limit GoogleDatabaseMigrationServiceConnectionProfile#storage_auto_resize_limit}
        :param tier: The tier (or machine type) for this instance, for example: db-n1-standard-1 (MySQL instances) or db-custom-1-3840 (PostgreSQL instances). For more information, see https://cloud.google.com/sql/docs/mysql/instance-settings Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#tier GoogleDatabaseMigrationServiceConnectionProfile#tier}
        :param user_labels: The resource labels for a Cloud SQL instance to use to annotate any related underlying resources such as Compute Engine VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#user_labels GoogleDatabaseMigrationServiceConnectionProfile#user_labels}
        :param zone: The Google Cloud Platform zone where your Cloud SQL datdabse instance is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#zone GoogleDatabaseMigrationServiceConnectionProfile#zone}
        '''
        if isinstance(ip_config, dict):
            ip_config = GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig(**ip_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1909a163764ffcf4ba4e87cd5b5f972113b88014ff0602b6d4ab0057e3211dae)
            check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
            check_type(argname="argument activation_policy", value=activation_policy, expected_type=type_hints["activation_policy"])
            check_type(argname="argument auto_storage_increase", value=auto_storage_increase, expected_type=type_hints["auto_storage_increase"])
            check_type(argname="argument cmek_key_name", value=cmek_key_name, expected_type=type_hints["cmek_key_name"])
            check_type(argname="argument collation", value=collation, expected_type=type_hints["collation"])
            check_type(argname="argument database_flags", value=database_flags, expected_type=type_hints["database_flags"])
            check_type(argname="argument database_version", value=database_version, expected_type=type_hints["database_version"])
            check_type(argname="argument data_disk_size_gb", value=data_disk_size_gb, expected_type=type_hints["data_disk_size_gb"])
            check_type(argname="argument data_disk_type", value=data_disk_type, expected_type=type_hints["data_disk_type"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument ip_config", value=ip_config, expected_type=type_hints["ip_config"])
            check_type(argname="argument root_password", value=root_password, expected_type=type_hints["root_password"])
            check_type(argname="argument storage_auto_resize_limit", value=storage_auto_resize_limit, expected_type=type_hints["storage_auto_resize_limit"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument user_labels", value=user_labels, expected_type=type_hints["user_labels"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_id": source_id,
        }
        if activation_policy is not None:
            self._values["activation_policy"] = activation_policy
        if auto_storage_increase is not None:
            self._values["auto_storage_increase"] = auto_storage_increase
        if cmek_key_name is not None:
            self._values["cmek_key_name"] = cmek_key_name
        if collation is not None:
            self._values["collation"] = collation
        if database_flags is not None:
            self._values["database_flags"] = database_flags
        if database_version is not None:
            self._values["database_version"] = database_version
        if data_disk_size_gb is not None:
            self._values["data_disk_size_gb"] = data_disk_size_gb
        if data_disk_type is not None:
            self._values["data_disk_type"] = data_disk_type
        if edition is not None:
            self._values["edition"] = edition
        if ip_config is not None:
            self._values["ip_config"] = ip_config
        if root_password is not None:
            self._values["root_password"] = root_password
        if storage_auto_resize_limit is not None:
            self._values["storage_auto_resize_limit"] = storage_auto_resize_limit
        if tier is not None:
            self._values["tier"] = tier
        if user_labels is not None:
            self._values["user_labels"] = user_labels
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def source_id(self) -> builtins.str:
        '''The Database Migration Service source connection profile ID, in the format: projects/my_project_name/locations/us-central1/connectionProfiles/connection_profile_ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#source_id GoogleDatabaseMigrationServiceConnectionProfile#source_id}
        '''
        result = self._values.get("source_id")
        assert result is not None, "Required property 'source_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def activation_policy(self) -> typing.Optional[builtins.str]:
        '''The activation policy specifies when the instance is activated;

        it is applicable only when the instance state is 'RUNNABLE'. Possible values: ["ALWAYS", "NEVER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#activation_policy GoogleDatabaseMigrationServiceConnectionProfile#activation_policy}
        '''
        result = self._values.get("activation_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_storage_increase(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If you enable this setting, Cloud SQL checks your available storage every 30 seconds.

        If the available storage falls below a threshold size, Cloud SQL automatically adds additional storage capacity.
        If the available storage repeatedly falls below the threshold size, Cloud SQL continues to add storage until it reaches the maximum of 30 TB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#auto_storage_increase GoogleDatabaseMigrationServiceConnectionProfile#auto_storage_increase}
        '''
        result = self._values.get("auto_storage_increase")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cmek_key_name(self) -> typing.Optional[builtins.str]:
        '''The KMS key name used for the csql instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cmek_key_name GoogleDatabaseMigrationServiceConnectionProfile#cmek_key_name}
        '''
        result = self._values.get("cmek_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def collation(self) -> typing.Optional[builtins.str]:
        '''The Cloud SQL default instance level collation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#collation GoogleDatabaseMigrationServiceConnectionProfile#collation}
        '''
        result = self._values.get("collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_flags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The database flags passed to the Cloud SQL instance at startup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_flags GoogleDatabaseMigrationServiceConnectionProfile#database_flags}
        '''
        result = self._values.get("database_flags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def database_version(self) -> typing.Optional[builtins.str]:
        '''The database engine type and version. Currently supported values located at https://cloud.google.com/database-migration/docs/reference/rest/v1/projects.locations.connectionProfiles#sqldatabaseversion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_version GoogleDatabaseMigrationServiceConnectionProfile#database_version}
        '''
        result = self._values.get("database_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_disk_size_gb(self) -> typing.Optional[builtins.str]:
        '''The storage capacity available to the database, in GB. The minimum (and default) size is 10GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#data_disk_size_gb GoogleDatabaseMigrationServiceConnectionProfile#data_disk_size_gb}
        '''
        result = self._values.get("data_disk_size_gb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_disk_type(self) -> typing.Optional[builtins.str]:
        '''The type of storage. Possible values: ["PD_SSD", "PD_HDD"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#data_disk_type GoogleDatabaseMigrationServiceConnectionProfile#data_disk_type}
        '''
        result = self._values.get("data_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''The edition of the given Cloud SQL instance. Possible values: ["ENTERPRISE", "ENTERPRISE_PLUS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#edition GoogleDatabaseMigrationServiceConnectionProfile#edition}
        '''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_config(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig"]:
        '''ip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ip_config GoogleDatabaseMigrationServiceConnectionProfile#ip_config}
        '''
        result = self._values.get("ip_config")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig"], result)

    @builtins.property
    def root_password(self) -> typing.Optional[builtins.str]:
        '''Input only. Initial root password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#root_password GoogleDatabaseMigrationServiceConnectionProfile#root_password}
        '''
        result = self._values.get("root_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_auto_resize_limit(self) -> typing.Optional[builtins.str]:
        '''The maximum size to which storage capacity can be automatically increased.

        The default value is 0, which specifies that there is no limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#storage_auto_resize_limit GoogleDatabaseMigrationServiceConnectionProfile#storage_auto_resize_limit}
        '''
        result = self._values.get("storage_auto_resize_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''The tier (or machine type) for this instance, for example: db-n1-standard-1 (MySQL instances) or db-custom-1-3840 (PostgreSQL instances).

        For more information, see https://cloud.google.com/sql/docs/mysql/instance-settings

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#tier GoogleDatabaseMigrationServiceConnectionProfile#tier}
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The resource labels for a Cloud SQL instance to use to annotate any related underlying resources such as Compute Engine VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#user_labels GoogleDatabaseMigrationServiceConnectionProfile#user_labels}
        '''
        result = self._values.get("user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Platform zone where your Cloud SQL datdabse instance is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#zone GoogleDatabaseMigrationServiceConnectionProfile#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorized_networks": "authorizedNetworks",
        "enable_ipv4": "enableIpv4",
        "private_network": "privateNetwork",
        "require_ssl": "requireSsl",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig:
    def __init__(
        self,
        *,
        authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_ipv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_network: typing.Optional[builtins.str] = None,
        require_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param authorized_networks: authorized_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#authorized_networks GoogleDatabaseMigrationServiceConnectionProfile#authorized_networks}
        :param enable_ipv4: Whether the instance should be assigned an IPv4 address or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#enable_ipv4 GoogleDatabaseMigrationServiceConnectionProfile#enable_ipv4}
        :param private_network: The resource link for the VPC network from which the Cloud SQL instance is accessible for private IP. For example, projects/myProject/global/networks/default. This setting can be updated, but it cannot be removed after it is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_network GoogleDatabaseMigrationServiceConnectionProfile#private_network}
        :param require_ssl: Whether SSL connections over IP should be enforced or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#require_ssl GoogleDatabaseMigrationServiceConnectionProfile#require_ssl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d2d8fee1283784ae209eb4c532927bb1a6694f188c5e0235dcd713d6de68c6)
            check_type(argname="argument authorized_networks", value=authorized_networks, expected_type=type_hints["authorized_networks"])
            check_type(argname="argument enable_ipv4", value=enable_ipv4, expected_type=type_hints["enable_ipv4"])
            check_type(argname="argument private_network", value=private_network, expected_type=type_hints["private_network"])
            check_type(argname="argument require_ssl", value=require_ssl, expected_type=type_hints["require_ssl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorized_networks is not None:
            self._values["authorized_networks"] = authorized_networks
        if enable_ipv4 is not None:
            self._values["enable_ipv4"] = enable_ipv4
        if private_network is not None:
            self._values["private_network"] = private_network
        if require_ssl is not None:
            self._values["require_ssl"] = require_ssl

    @builtins.property
    def authorized_networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks"]]]:
        '''authorized_networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#authorized_networks GoogleDatabaseMigrationServiceConnectionProfile#authorized_networks}
        '''
        result = self._values.get("authorized_networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks"]]], result)

    @builtins.property
    def enable_ipv4(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance should be assigned an IPv4 address or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#enable_ipv4 GoogleDatabaseMigrationServiceConnectionProfile#enable_ipv4}
        '''
        result = self._values.get("enable_ipv4")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_network(self) -> typing.Optional[builtins.str]:
        '''The resource link for the VPC network from which the Cloud SQL instance is accessible for private IP.

        For example, projects/myProject/global/networks/default.
        This setting can be updated, but it cannot be removed after it is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_network GoogleDatabaseMigrationServiceConnectionProfile#private_network}
        '''
        result = self._values.get("private_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether SSL connections over IP should be enforced or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#require_ssl GoogleDatabaseMigrationServiceConnectionProfile#require_ssl}
        '''
        result = self._values.get("require_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "expire_time": "expireTime",
        "label": "label",
        "ttl": "ttl",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks:
    def __init__(
        self,
        *,
        value: builtins.str,
        expire_time: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: The allowlisted value for the access control list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#value GoogleDatabaseMigrationServiceConnectionProfile#value}
        :param expire_time: The time when this access control entry expires in RFC 3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#expire_time GoogleDatabaseMigrationServiceConnectionProfile#expire_time}
        :param label: A label to identify this entry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#label GoogleDatabaseMigrationServiceConnectionProfile#label}
        :param ttl: Input only. The time-to-leave of this access control entry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ttl GoogleDatabaseMigrationServiceConnectionProfile#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7c1f58ad2b9b325c8af6bc1c889e5871be2acbfde501725bd47f9cba96ff97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument expire_time", value=expire_time, expected_type=type_hints["expire_time"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if expire_time is not None:
            self._values["expire_time"] = expire_time
        if label is not None:
            self._values["label"] = label
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def value(self) -> builtins.str:
        '''The allowlisted value for the access control list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#value GoogleDatabaseMigrationServiceConnectionProfile#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expire_time(self) -> typing.Optional[builtins.str]:
        '''The time when this access control entry expires in RFC 3339 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#expire_time GoogleDatabaseMigrationServiceConnectionProfile#expire_time}
        '''
        result = self._values.get("expire_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''A label to identify this entry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#label GoogleDatabaseMigrationServiceConnectionProfile#label}
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(self) -> typing.Optional[builtins.str]:
        '''Input only. The time-to-leave of this access control entry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ttl GoogleDatabaseMigrationServiceConnectionProfile#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2ea893a60f681f588e5d21f4f1b6d2d5b0e439c48a8d154256ba74fbfb74cc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d3b4a8b94a29db16f1d59be79942b5ad001196dd9088d27248eb997f873227)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de0a5685e029ed8e45c24d63e1b54cd5d49c90374799d2694194f6c1cf4631a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1179b56239ed7f175437be9c4d8a4b0ef717566f0e9c6050ba32bfa3536cf2f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb911bfdcc6166f2247dd4e6f3731e2535305da3a8b35effcc80837a6fd0553d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b49c28d27191e427f3e74b78aae4b388b5551787f4bceffc5dceb0a4286613b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__975ee0d6c0804cfe1124722ec8d3b40de543344d5c5ba0144cb09b6e1937c94e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExpireTime")
    def reset_expire_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpireTime", []))

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @builtins.property
    @jsii.member(jsii_name="expireTimeInput")
    def expire_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expireTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @expire_time.setter
    def expire_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e92428898a5eeabe2ff683cbda2083c972268de5ca1808a3947b1f418a0373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16e11ae7e22141d95b1f12c1b13964565a177b5db9c78426ec8c0e552542f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc43a3f6d0aa186e3c928d7b2f27460ffb6fb9ca9cfd1e5ba1c2ac0d4658d732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__870b8420a91a47057db25fa1648a100dd639321636c9a2b93795a5f33d653507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3775ab6a74fb4ed7a0a0a62c99e51ae934a9d54b77e856874e7dc9c0199316b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2da8acf13ba2b61dee96cb6ed7cf76299bbff9d777bf44461170e13f35eb69d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizedNetworks")
    def put_authorized_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db62518812e1ba05c0734b9ed893bbf89a9693b57d128f0a2d1f1aa50e2758a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthorizedNetworks", [value]))

    @jsii.member(jsii_name="resetAuthorizedNetworks")
    def reset_authorized_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizedNetworks", []))

    @jsii.member(jsii_name="resetEnableIpv4")
    def reset_enable_ipv4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIpv4", []))

    @jsii.member(jsii_name="resetPrivateNetwork")
    def reset_private_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateNetwork", []))

    @jsii.member(jsii_name="resetRequireSsl")
    def reset_require_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireSsl", []))

    @builtins.property
    @jsii.member(jsii_name="authorizedNetworks")
    def authorized_networks(
        self,
    ) -> GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksList:
        return typing.cast(GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksList, jsii.get(self, "authorizedNetworks"))

    @builtins.property
    @jsii.member(jsii_name="authorizedNetworksInput")
    def authorized_networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]], jsii.get(self, "authorizedNetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIpv4Input")
    def enable_ipv4_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIpv4Input"))

    @builtins.property
    @jsii.member(jsii_name="privateNetworkInput")
    def private_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="requireSslInput")
    def require_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireSslInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIpv4")
    def enable_ipv4(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIpv4"))

    @enable_ipv4.setter
    def enable_ipv4(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1500c37639be1ae2d1c2c6a8cbc396674b6d89042957b9ead701f4f9b75a8e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIpv4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateNetwork")
    def private_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateNetwork"))

    @private_network.setter
    def private_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1dec437c8276a0bdad2ef883cb0a60ab0437a12141b3ee0aee1e34afad7d97b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireSsl")
    def require_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireSsl"))

    @require_ssl.setter
    def require_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02647aa27773c4896a15fa8ca1107ea6f859a57dc5a88b5e36e82b72216aa38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c8dbc5bd6d9cba659c14e3a13a4f50717ee22f8490d78bccd26146af56beae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9de667471cdfbdd92985ba85be82b40871de20188ff704ead64be85e12359c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpConfig")
    def put_ip_config(
        self,
        *,
        authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_ipv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_network: typing.Optional[builtins.str] = None,
        require_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param authorized_networks: authorized_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#authorized_networks GoogleDatabaseMigrationServiceConnectionProfile#authorized_networks}
        :param enable_ipv4: Whether the instance should be assigned an IPv4 address or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#enable_ipv4 GoogleDatabaseMigrationServiceConnectionProfile#enable_ipv4}
        :param private_network: The resource link for the VPC network from which the Cloud SQL instance is accessible for private IP. For example, projects/myProject/global/networks/default. This setting can be updated, but it cannot be removed after it is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_network GoogleDatabaseMigrationServiceConnectionProfile#private_network}
        :param require_ssl: Whether SSL connections over IP should be enforced or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#require_ssl GoogleDatabaseMigrationServiceConnectionProfile#require_ssl}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig(
            authorized_networks=authorized_networks,
            enable_ipv4=enable_ipv4,
            private_network=private_network,
            require_ssl=require_ssl,
        )

        return typing.cast(None, jsii.invoke(self, "putIpConfig", [value]))

    @jsii.member(jsii_name="resetActivationPolicy")
    def reset_activation_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActivationPolicy", []))

    @jsii.member(jsii_name="resetAutoStorageIncrease")
    def reset_auto_storage_increase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoStorageIncrease", []))

    @jsii.member(jsii_name="resetCmekKeyName")
    def reset_cmek_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCmekKeyName", []))

    @jsii.member(jsii_name="resetCollation")
    def reset_collation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollation", []))

    @jsii.member(jsii_name="resetDatabaseFlags")
    def reset_database_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseFlags", []))

    @jsii.member(jsii_name="resetDatabaseVersion")
    def reset_database_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseVersion", []))

    @jsii.member(jsii_name="resetDataDiskSizeGb")
    def reset_data_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDiskSizeGb", []))

    @jsii.member(jsii_name="resetDataDiskType")
    def reset_data_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDiskType", []))

    @jsii.member(jsii_name="resetEdition")
    def reset_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdition", []))

    @jsii.member(jsii_name="resetIpConfig")
    def reset_ip_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpConfig", []))

    @jsii.member(jsii_name="resetRootPassword")
    def reset_root_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootPassword", []))

    @jsii.member(jsii_name="resetStorageAutoResizeLimit")
    def reset_storage_auto_resize_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAutoResizeLimit", []))

    @jsii.member(jsii_name="resetTier")
    def reset_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTier", []))

    @jsii.member(jsii_name="resetUserLabels")
    def reset_user_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserLabels", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="ipConfig")
    def ip_config(
        self,
    ) -> GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigOutputReference:
        return typing.cast(GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigOutputReference, jsii.get(self, "ipConfig"))

    @builtins.property
    @jsii.member(jsii_name="rootPasswordSet")
    def root_password_set(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "rootPasswordSet"))

    @builtins.property
    @jsii.member(jsii_name="activationPolicyInput")
    def activation_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="autoStorageIncreaseInput")
    def auto_storage_increase_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoStorageIncreaseInput"))

    @builtins.property
    @jsii.member(jsii_name="cmekKeyNameInput")
    def cmek_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cmekKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="collationInput")
    def collation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collationInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseFlagsInput")
    def database_flags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "databaseFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseVersionInput")
    def database_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskSizeGbInput")
    def data_disk_size_gb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskTypeInput")
    def data_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="editionInput")
    def edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigInput")
    def ip_config_input(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig], jsii.get(self, "ipConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="rootPasswordInput")
    def root_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIdInput")
    def source_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAutoResizeLimitInput")
    def storage_auto_resize_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAutoResizeLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="userLabelsInput")
    def user_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "userLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="activationPolicy")
    def activation_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activationPolicy"))

    @activation_policy.setter
    def activation_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b92575e48e69622fd81c86efa945cd685f15b66dc0d8de94dd26ee40a9f1a60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoStorageIncrease")
    def auto_storage_increase(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoStorageIncrease"))

    @auto_storage_increase.setter
    def auto_storage_increase(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e33dce9efbb55185f48d3e3a1b53676998fd6b21702649a3bbb4bc4b30f95ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoStorageIncrease", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cmekKeyName")
    def cmek_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cmekKeyName"))

    @cmek_key_name.setter
    def cmek_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b0c2a59c508143012831fcbb5e82d87af92b2408964197844912408510e9b71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cmekKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collation")
    def collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collation"))

    @collation.setter
    def collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f8a08656e3e58faae1306da26ca8dc4f2633e23085d7c6af5ea2049f31fb26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseFlags")
    def database_flags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "databaseFlags"))

    @database_flags.setter
    def database_flags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436fa46a7ed31a89fb3825c6a1710d029b8c9d64123970852bacfc26a24c1b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseFlags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseVersion")
    def database_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseVersion"))

    @database_version.setter
    def database_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c6379391979b4042c149b7dee1c380c044a834eacd5d89c9ad17027451f9aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDiskSizeGb")
    def data_disk_size_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataDiskSizeGb"))

    @data_disk_size_gb.setter
    def data_disk_size_gb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__133c193cbc0225030f469a06a3780fa85f80df03c10af19d4e17e6835b94dc77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDiskType")
    def data_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataDiskType"))

    @data_disk_type.setter
    def data_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34eb36c0ec7ab349616f8826a7e1ea16adaf255a31af2124fe02275f9e124784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe17bb32cc1eb8d3dbbcdfae156ea704aac8ff8310996d56f4afae384c4b751c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootPassword")
    def root_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootPassword"))

    @root_password.setter
    def root_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a13db801cb878c090a83cd4fde03fd438bdf4f04e1d30f29601de20d4635990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceId")
    def source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceId"))

    @source_id.setter
    def source_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91774d4b3e0cde9fb06fb3571afac3ba9121b018f8a3f616357a739414b18e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAutoResizeLimit")
    def storage_auto_resize_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAutoResizeLimit"))

    @storage_auto_resize_limit.setter
    def storage_auto_resize_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae20b481dec63b1935d6d8cdc7f272941b0662649a0e118f376cfd843ade7410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAutoResizeLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f72415528f6ba85df17b47321f1fb1eee334be7414305f072eaa387fe391807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userLabels")
    def user_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "userLabels"))

    @user_labels.setter
    def user_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b3e090eaef763c6278f5291edf193215ad3210256ada4f87ace52a9765b799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43567b21d2a79a79b7f60440404bf3d92911f4cd29a99dfb74121e5124d35d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce2842ebbb2cdcd0c176146f78ebba89daf3fb6eab3f19664114ab7a76ddf9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileConfig",
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
        "alloydb": "alloydb",
        "cloudsql": "cloudsql",
        "display_name": "displayName",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "mysql": "mysql",
        "oracle": "oracle",
        "postgresql": "postgresql",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfileConfig(
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
        connection_profile_id: builtins.str,
        alloydb: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileAlloydb, typing.Dict[builtins.str, typing.Any]]] = None,
        cloudsql: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileCloudsql, typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        mysql: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileMysql", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileOracle", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfilePostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connection_profile_id: The ID of the connection profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#connection_profile_id GoogleDatabaseMigrationServiceConnectionProfile#connection_profile_id}
        :param alloydb: alloydb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#alloydb GoogleDatabaseMigrationServiceConnectionProfile#alloydb}
        :param cloudsql: cloudsql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cloudsql GoogleDatabaseMigrationServiceConnectionProfile#cloudsql}
        :param display_name: The connection profile display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#display_name GoogleDatabaseMigrationServiceConnectionProfile#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#id GoogleDatabaseMigrationServiceConnectionProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The resource labels for connection profile to use to annotate any related underlying resources such as Compute Engine VMs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#labels GoogleDatabaseMigrationServiceConnectionProfile#labels}
        :param location: The location where the connection profile should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#location GoogleDatabaseMigrationServiceConnectionProfile#location}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#mysql GoogleDatabaseMigrationServiceConnectionProfile#mysql}
        :param oracle: oracle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#oracle GoogleDatabaseMigrationServiceConnectionProfile#oracle}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#postgresql GoogleDatabaseMigrationServiceConnectionProfile#postgresql}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#project GoogleDatabaseMigrationServiceConnectionProfile#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#timeouts GoogleDatabaseMigrationServiceConnectionProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(alloydb, dict):
            alloydb = GoogleDatabaseMigrationServiceConnectionProfileAlloydb(**alloydb)
        if isinstance(cloudsql, dict):
            cloudsql = GoogleDatabaseMigrationServiceConnectionProfileCloudsql(**cloudsql)
        if isinstance(mysql, dict):
            mysql = GoogleDatabaseMigrationServiceConnectionProfileMysql(**mysql)
        if isinstance(oracle, dict):
            oracle = GoogleDatabaseMigrationServiceConnectionProfileOracle(**oracle)
        if isinstance(postgresql, dict):
            postgresql = GoogleDatabaseMigrationServiceConnectionProfilePostgresql(**postgresql)
        if isinstance(timeouts, dict):
            timeouts = GoogleDatabaseMigrationServiceConnectionProfileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afcc5fc5e127d51f78d072f002b44a8ebeb5605e681f08341615305d49f85f18)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument connection_profile_id", value=connection_profile_id, expected_type=type_hints["connection_profile_id"])
            check_type(argname="argument alloydb", value=alloydb, expected_type=type_hints["alloydb"])
            check_type(argname="argument cloudsql", value=cloudsql, expected_type=type_hints["cloudsql"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument mysql", value=mysql, expected_type=type_hints["mysql"])
            check_type(argname="argument oracle", value=oracle, expected_type=type_hints["oracle"])
            check_type(argname="argument postgresql", value=postgresql, expected_type=type_hints["postgresql"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_profile_id": connection_profile_id,
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
        if alloydb is not None:
            self._values["alloydb"] = alloydb
        if cloudsql is not None:
            self._values["cloudsql"] = cloudsql
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if mysql is not None:
            self._values["mysql"] = mysql
        if oracle is not None:
            self._values["oracle"] = oracle
        if postgresql is not None:
            self._values["postgresql"] = postgresql
        if project is not None:
            self._values["project"] = project
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
        '''The ID of the connection profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#connection_profile_id GoogleDatabaseMigrationServiceConnectionProfile#connection_profile_id}
        '''
        result = self._values.get("connection_profile_id")
        assert result is not None, "Required property 'connection_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alloydb(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydb]:
        '''alloydb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#alloydb GoogleDatabaseMigrationServiceConnectionProfile#alloydb}
        '''
        result = self._values.get("alloydb")
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydb], result)

    @builtins.property
    def cloudsql(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsql]:
        '''cloudsql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cloudsql GoogleDatabaseMigrationServiceConnectionProfile#cloudsql}
        '''
        result = self._values.get("cloudsql")
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsql], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The connection profile display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#display_name GoogleDatabaseMigrationServiceConnectionProfile#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#id GoogleDatabaseMigrationServiceConnectionProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The resource labels for connection profile to use to annotate any related underlying resources such as Compute Engine VMs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#labels GoogleDatabaseMigrationServiceConnectionProfile#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location where the connection profile should reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#location GoogleDatabaseMigrationServiceConnectionProfile#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mysql(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileMysql"]:
        '''mysql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#mysql GoogleDatabaseMigrationServiceConnectionProfile#mysql}
        '''
        result = self._values.get("mysql")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileMysql"], result)

    @builtins.property
    def oracle(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracle"]:
        '''oracle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#oracle GoogleDatabaseMigrationServiceConnectionProfile#oracle}
        '''
        result = self._values.get("oracle")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracle"], result)

    @builtins.property
    def postgresql(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfilePostgresql"]:
        '''postgresql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#postgresql GoogleDatabaseMigrationServiceConnectionProfile#postgresql}
        '''
        result = self._values.get("postgresql")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfilePostgresql"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#project GoogleDatabaseMigrationServiceConnectionProfile#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#timeouts GoogleDatabaseMigrationServiceConnectionProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileError",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDatabaseMigrationServiceConnectionProfileError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__809fb64f0a7d9d4cbed7b7a363b6ab2e96587a78b045c05e7a3a6f8b0446b265)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9001d10b9d6535ddce5092df9dc663431ef57c58c70fb71d488ba999175a7c1a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecce2d3a232c82f7ac79208b21a1ab1b80819c3c3becb9a2e9bc3d488a907978)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa7534e7a552f8c8581d10bf14d3940dc249a36dcb2c7e1097fbb11f80895585)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfde9690fb369047541ec0b1de97d54f76c079cd96dd133c16cafdc033e83969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDatabaseMigrationServiceConnectionProfileErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65d62d6b063c438d90f57941ee4955d2e88c1b4b6ef17a94f3c8caabcbb3bdd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> _cdktf_9a9027ec.StringMapList:
        return typing.cast(_cdktf_9a9027ec.StringMapList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileError]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7917f3bd15f610fbac62d602eba0ea3f44a0a5b0e915469d6f4122d7adc67a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileMysql",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_sql_id": "cloudSqlId",
        "host": "host",
        "password": "password",
        "port": "port",
        "ssl": "ssl",
        "username": "username",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfileMysql:
    def __init__(
        self,
        *,
        cloud_sql_id: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        ssl: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_sql_id: If the source is a Cloud SQL database, use this field to provide the Cloud SQL instance ID of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cloud_sql_id GoogleDatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        :param host: The IP or hostname of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#host GoogleDatabaseMigrationServiceConnectionProfile#host}
        :param password: Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        :param port: The network port of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ssl GoogleDatabaseMigrationServiceConnectionProfile#ssl}
        :param username: The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        '''
        if isinstance(ssl, dict):
            ssl = GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl(**ssl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e41d699785711bfab3a5d7746efb928849a2b6b9ed71fda6ff34e7ca0dd31d6)
            check_type(argname="argument cloud_sql_id", value=cloud_sql_id, expected_type=type_hints["cloud_sql_id"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument ssl", value=ssl, expected_type=type_hints["ssl"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_sql_id is not None:
            self._values["cloud_sql_id"] = cloud_sql_id
        if host is not None:
            self._values["host"] = host
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if ssl is not None:
            self._values["ssl"] = ssl
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def cloud_sql_id(self) -> typing.Optional[builtins.str]:
        '''If the source is a Cloud SQL database, use this field to provide the Cloud SQL instance ID of the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cloud_sql_id GoogleDatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        '''
        result = self._values.get("cloud_sql_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The IP or hostname of the source MySQL database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#host GoogleDatabaseMigrationServiceConnectionProfile#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The password for the user that Database Migration Service will be using to connect to the database.
        This field is not returned on request, and the value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The network port of the source MySQL database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssl(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl"]:
        '''ssl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ssl GoogleDatabaseMigrationServiceConnectionProfile#ssl}
        '''
        result = self._values.get("ssl")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl"], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username that Database Migration Service will use to connect to the database.

        The value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileMysql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileMysqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileMysqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cc0769123f8c383e4ade5d4a466626ee30627a207f688fa3865fe93e091c296)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSsl")
    def put_ssl(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ca_certificate GoogleDatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_certificate GoogleDatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_key GoogleDatabaseMigrationServiceConnectionProfile#client_key}
        :param type: The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#type GoogleDatabaseMigrationServiceConnectionProfile#type}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl(
            ca_certificate=ca_certificate,
            client_certificate=client_certificate,
            client_key=client_key,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putSsl", [value]))

    @jsii.member(jsii_name="resetCloudSqlId")
    def reset_cloud_sql_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSqlId", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetSsl")
    def reset_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsl", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="passwordSet")
    def password_set(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "passwordSet"))

    @builtins.property
    @jsii.member(jsii_name="ssl")
    def ssl(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileMysqlSslOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileMysqlSslOutputReference", jsii.get(self, "ssl"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlIdInput")
    def cloud_sql_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudSqlIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="sslInput")
    def ssl_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl"], jsii.get(self, "sslInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlId")
    def cloud_sql_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudSqlId"))

    @cloud_sql_id.setter
    def cloud_sql_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9781ed5529b40a949fab88bd54f2b0aec16223ed8e78fcbf8a69b358267430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSqlId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79e346e16fb14262a2f34d5e44441f44342e0d86f5b52779005a979aef8d2a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357021e937f828c9015fdfdea80d760720cf3b0351c16bf36d051da2d83c90a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d138c0e58973002f60723a221aec25421341bc64a4ae5f5d03604dc1e4b813e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a8a83f83650e098248a9226921798e8814fb35848f035e119f109c39ee18fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileMysql]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileMysql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileMysql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338344e20fdce09329e458c11cb821df82740a6472a769f8fd8a559d60619c95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl",
    jsii_struct_bases=[],
    name_mapping={
        "ca_certificate": "caCertificate",
        "client_certificate": "clientCertificate",
        "client_key": "clientKey",
        "type": "type",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl:
    def __init__(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ca_certificate GoogleDatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_certificate GoogleDatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_key GoogleDatabaseMigrationServiceConnectionProfile#client_key}
        :param type: The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#type GoogleDatabaseMigrationServiceConnectionProfile#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954aa6385c992731dc4399cecec47557e5ceaa937ec787ae1292dacc91e8c84c)
            check_type(argname="argument ca_certificate", value=ca_certificate, expected_type=type_hints["ca_certificate"])
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument client_key", value=client_key, expected_type=type_hints["client_key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ca_certificate is not None:
            self._values["ca_certificate"] = ca_certificate
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if client_key is not None:
            self._values["client_key"] = client_key
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def ca_certificate(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The x509 PEM-encoded certificate of the CA that signed the source database server's certificate.
        The replica will use this certificate to verify it's connecting to the right host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ca_certificate GoogleDatabaseMigrationServiceConnectionProfile#ca_certificate}
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server.
        If this field is used then the 'clientKey' field is mandatory

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_certificate GoogleDatabaseMigrationServiceConnectionProfile#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate.
        If this field is used then the 'clientCertificate' field is mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_key GoogleDatabaseMigrationServiceConnectionProfile#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#type GoogleDatabaseMigrationServiceConnectionProfile#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileMysqlSslOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileMysqlSslOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f31fd3012bb42e012b2d415482c0bcdbf794adc9a674bf12a963daabb55ab59)
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

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertificate")
    def ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertificate"))

    @ca_certificate.setter
    def ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1c09f4b172e67b4d39032dd4203ff8b3bcbe24698a0cc1d57d57b3fd5480c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88bb5a969d183c88ab819bcaabe72a9132ca9f3e73bf3c39b4e8eda222106bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8bbf53b7cc62bed7f2c3a3e92d8cb058b4f4294d85aeefef5b61d06b1aca24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4f3d42936938d59b859c7199e2f75697c2c5cf954b7d1580ee5c541368bbd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ededa412b4de095579022aaeb8f98fc7e6e0bdc46f908cc443cd2bb68bbde1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileOracle",
    jsii_struct_bases=[],
    name_mapping={
        "database_service": "databaseService",
        "host": "host",
        "password": "password",
        "port": "port",
        "username": "username",
        "forward_ssh_connectivity": "forwardSshConnectivity",
        "private_connectivity": "privateConnectivity",
        "ssl": "ssl",
        "static_service_ip_connectivity": "staticServiceIpConnectivity",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfileOracle:
    def __init__(
        self,
        *,
        database_service: builtins.str,
        host: builtins.str,
        password: builtins.str,
        port: jsii.Number,
        username: builtins.str,
        forward_ssh_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        private_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileOracleSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        static_service_ip_connectivity: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_service: Required. Database service for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_service GoogleDatabaseMigrationServiceConnectionProfile#database_service}
        :param host: Required. The IP or hostname of the source Oracle database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#host GoogleDatabaseMigrationServiceConnectionProfile#host}
        :param password: Required. Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        :param port: Required. The network port of the source Oracle database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        :param username: Required. The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        :param forward_ssh_connectivity: forward_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#forward_ssh_connectivity GoogleDatabaseMigrationServiceConnectionProfile#forward_ssh_connectivity}
        :param private_connectivity: private_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_connectivity GoogleDatabaseMigrationServiceConnectionProfile#private_connectivity}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ssl GoogleDatabaseMigrationServiceConnectionProfile#ssl}
        :param static_service_ip_connectivity: static_service_ip_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#static_service_ip_connectivity GoogleDatabaseMigrationServiceConnectionProfile#static_service_ip_connectivity}
        '''
        if isinstance(forward_ssh_connectivity, dict):
            forward_ssh_connectivity = GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity(**forward_ssh_connectivity)
        if isinstance(private_connectivity, dict):
            private_connectivity = GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity(**private_connectivity)
        if isinstance(ssl, dict):
            ssl = GoogleDatabaseMigrationServiceConnectionProfileOracleSsl(**ssl)
        if isinstance(static_service_ip_connectivity, dict):
            static_service_ip_connectivity = GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity(**static_service_ip_connectivity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb48a064d9a6f7c60f3fff518855f22e505da5b885c9d49a8fdb4d0b4cdbb92f)
            check_type(argname="argument database_service", value=database_service, expected_type=type_hints["database_service"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument forward_ssh_connectivity", value=forward_ssh_connectivity, expected_type=type_hints["forward_ssh_connectivity"])
            check_type(argname="argument private_connectivity", value=private_connectivity, expected_type=type_hints["private_connectivity"])
            check_type(argname="argument ssl", value=ssl, expected_type=type_hints["ssl"])
            check_type(argname="argument static_service_ip_connectivity", value=static_service_ip_connectivity, expected_type=type_hints["static_service_ip_connectivity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_service": database_service,
            "host": host,
            "password": password,
            "port": port,
            "username": username,
        }
        if forward_ssh_connectivity is not None:
            self._values["forward_ssh_connectivity"] = forward_ssh_connectivity
        if private_connectivity is not None:
            self._values["private_connectivity"] = private_connectivity
        if ssl is not None:
            self._values["ssl"] = ssl
        if static_service_ip_connectivity is not None:
            self._values["static_service_ip_connectivity"] = static_service_ip_connectivity

    @builtins.property
    def database_service(self) -> builtins.str:
        '''Required. Database service for the Oracle connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#database_service GoogleDatabaseMigrationServiceConnectionProfile#database_service}
        '''
        result = self._values.get("database_service")
        assert result is not None, "Required property 'database_service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Required. The IP or hostname of the source Oracle database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#host GoogleDatabaseMigrationServiceConnectionProfile#host}
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Required.

        Input only. The password for the user that Database Migration Service will be using to connect to the database.
        This field is not returned on request, and the value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Required. The network port of the source Oracle database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Required.

        The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def forward_ssh_connectivity(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity"]:
        '''forward_ssh_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#forward_ssh_connectivity GoogleDatabaseMigrationServiceConnectionProfile#forward_ssh_connectivity}
        '''
        result = self._values.get("forward_ssh_connectivity")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity"], result)

    @builtins.property
    def private_connectivity(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity"]:
        '''private_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_connectivity GoogleDatabaseMigrationServiceConnectionProfile#private_connectivity}
        '''
        result = self._values.get("private_connectivity")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity"], result)

    @builtins.property
    def ssl(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracleSsl"]:
        '''ssl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ssl GoogleDatabaseMigrationServiceConnectionProfile#ssl}
        '''
        result = self._values.get("ssl")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracleSsl"], result)

    @builtins.property
    def static_service_ip_connectivity(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity"]:
        '''static_service_ip_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#static_service_ip_connectivity GoogleDatabaseMigrationServiceConnectionProfile#static_service_ip_connectivity}
        '''
        result = self._values.get("static_service_ip_connectivity")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileOracle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity",
    jsii_struct_bases=[],
    name_mapping={
        "hostname": "hostname",
        "port": "port",
        "username": "username",
        "password": "password",
        "private_key": "privateKey",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity:
    def __init__(
        self,
        *,
        hostname: builtins.str,
        port: jsii.Number,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: Required. Hostname for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#hostname GoogleDatabaseMigrationServiceConnectionProfile#hostname}
        :param port: Port for the SSH tunnel, default value is 22. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        :param username: Required. Username for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        :param password: Input only. SSH password. Only one of 'password' and 'private_key' can be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        :param private_key: Input only. SSH private key. Only one of 'password' and 'private_key' can be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_key GoogleDatabaseMigrationServiceConnectionProfile#private_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9eea1e6a584f80815b2713223edd5584245bf2daaceca91bf9399593f2db7e)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostname": hostname,
            "port": port,
            "username": username,
        }
        if password is not None:
            self._values["password"] = password
        if private_key is not None:
            self._values["private_key"] = private_key

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Required. Hostname for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#hostname GoogleDatabaseMigrationServiceConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Port for the SSH tunnel, default value is 22.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Required. Username for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Input only. SSH password. Only one of 'password' and 'private_key' can be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''Input only. SSH private key. Only one of 'password' and 'private_key' can be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_key GoogleDatabaseMigrationServiceConnectionProfile#private_key}
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49f848fabb03f4227dfaea743b39229cba8e12d0fa4ed28e59c65c9094b44754)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5ef503848cbb6aa555e8bcca6279b728c4d0cee4d6941d17d8748412eb71149f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180502245efe6c346b6e4a7176430b577ae01dd537c7d114287f06f245cf49e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f861cd4366604600cd788dc60e1ec65b11bc0fe25793b1874939a28e4c2243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201b10c9a3df72debcea59c0de55f61a1998f404148cca83588463ae6204735f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e28ec7a6bc3d0de1b6c5bd66c02db3e47e0e53ffcbe5e65101ab3e261879448c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ac559993246f090038b267e2929f2d8916818f8ea76e0828db06e4edc2b1a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDatabaseMigrationServiceConnectionProfileOracleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileOracleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45d2b67ec671c8bfa5a5be667b911cb80cf112d551aaf505b239d3c31dde955d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putForwardSshConnectivity")
    def put_forward_ssh_connectivity(
        self,
        *,
        hostname: builtins.str,
        port: jsii.Number,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: Required. Hostname for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#hostname GoogleDatabaseMigrationServiceConnectionProfile#hostname}
        :param port: Port for the SSH tunnel, default value is 22. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        :param username: Required. Username for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        :param password: Input only. SSH password. Only one of 'password' and 'private_key' can be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        :param private_key: Input only. SSH private key. Only one of 'password' and 'private_key' can be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_key GoogleDatabaseMigrationServiceConnectionProfile#private_key}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            private_key=private_key,
        )

        return typing.cast(None, jsii.invoke(self, "putForwardSshConnectivity", [value]))

    @jsii.member(jsii_name="putPrivateConnectivity")
    def put_private_connectivity(self, *, private_connection: builtins.str) -> None:
        '''
        :param private_connection: Required. The resource name (URI) of the private connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_connection GoogleDatabaseMigrationServiceConnectionProfile#private_connection}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity(
            private_connection=private_connection
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateConnectivity", [value]))

    @jsii.member(jsii_name="putSsl")
    def put_ssl(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ca_certificate GoogleDatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_certificate GoogleDatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_key GoogleDatabaseMigrationServiceConnectionProfile#client_key}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfileOracleSsl(
            ca_certificate=ca_certificate,
            client_certificate=client_certificate,
            client_key=client_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSsl", [value]))

    @jsii.member(jsii_name="putStaticServiceIpConnectivity")
    def put_static_service_ip_connectivity(self) -> None:
        value = GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity()

        return typing.cast(None, jsii.invoke(self, "putStaticServiceIpConnectivity", [value]))

    @jsii.member(jsii_name="resetForwardSshConnectivity")
    def reset_forward_ssh_connectivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardSshConnectivity", []))

    @jsii.member(jsii_name="resetPrivateConnectivity")
    def reset_private_connectivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateConnectivity", []))

    @jsii.member(jsii_name="resetSsl")
    def reset_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsl", []))

    @jsii.member(jsii_name="resetStaticServiceIpConnectivity")
    def reset_static_service_ip_connectivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticServiceIpConnectivity", []))

    @builtins.property
    @jsii.member(jsii_name="forwardSshConnectivity")
    def forward_ssh_connectivity(
        self,
    ) -> GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivityOutputReference:
        return typing.cast(GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivityOutputReference, jsii.get(self, "forwardSshConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="passwordSet")
    def password_set(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "passwordSet"))

    @builtins.property
    @jsii.member(jsii_name="privateConnectivity")
    def private_connectivity(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivityOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivityOutputReference", jsii.get(self, "privateConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="ssl")
    def ssl(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileOracleSslOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileOracleSslOutputReference", jsii.get(self, "ssl"))

    @builtins.property
    @jsii.member(jsii_name="staticServiceIpConnectivity")
    def static_service_ip_connectivity(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivityOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivityOutputReference", jsii.get(self, "staticServiceIpConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="databaseServiceInput")
    def database_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardSshConnectivityInput")
    def forward_ssh_connectivity_input(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity], jsii.get(self, "forwardSshConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="privateConnectivityInput")
    def private_connectivity_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity"], jsii.get(self, "privateConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="sslInput")
    def ssl_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracleSsl"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracleSsl"], jsii.get(self, "sslInput"))

    @builtins.property
    @jsii.member(jsii_name="staticServiceIpConnectivityInput")
    def static_service_ip_connectivity_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity"], jsii.get(self, "staticServiceIpConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseService")
    def database_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseService"))

    @database_service.setter
    def database_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc020f1c1319a1ffd0432400175c356373c98a4d95e80fa6810b317923f61346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ebfd0678ed0c5ae8e23f6fd6395959a71bdcf563b210b618e81c44cea90d99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f4e4dd4917dcea9ed2c828fb7e9c220aaff19a92a1ebbbfcc0d469fa77ee58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24283ebe9ec99b1a4b6e829636f7201dfeb40b4e27e5dbc8c17fd786a1ae5a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c671ef048a1333136d14956cd7cc7580a47235eda49384d55e29eb659e09340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracle]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53a82111a68b4fd26395737c5499fef849020253fe4377015f04906b3db62fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity",
    jsii_struct_bases=[],
    name_mapping={"private_connection": "privateConnection"},
)
class GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity:
    def __init__(self, *, private_connection: builtins.str) -> None:
        '''
        :param private_connection: Required. The resource name (URI) of the private connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_connection GoogleDatabaseMigrationServiceConnectionProfile#private_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc83ac65104f2b0891eae859f01ba3f9f9e77cb1d9a0e9d0b2012d3a1ff6939)
            check_type(argname="argument private_connection", value=private_connection, expected_type=type_hints["private_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "private_connection": private_connection,
        }

    @builtins.property
    def private_connection(self) -> builtins.str:
        '''Required. The resource name (URI) of the private connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#private_connection GoogleDatabaseMigrationServiceConnectionProfile#private_connection}
        '''
        result = self._values.get("private_connection")
        assert result is not None, "Required property 'private_connection' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eceebc014e7e9cab5ff2934ca8ae971ecdcd7c4df847c13b38c7f17fa5012b6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c669cada0017ccefa7422a3af8415de40913b8b7c7ed0602e58f6531bbc2608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateConnection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856cbf3621d384dd676e9313743359fb1dbdce9e66e6f3911eb4269296f749fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileOracleSsl",
    jsii_struct_bases=[],
    name_mapping={
        "ca_certificate": "caCertificate",
        "client_certificate": "clientCertificate",
        "client_key": "clientKey",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfileOracleSsl:
    def __init__(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ca_certificate GoogleDatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_certificate GoogleDatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_key GoogleDatabaseMigrationServiceConnectionProfile#client_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279bd90caa1283367d2a339f07f1caea159185b5f7166b9c2951e0c14f770d9c)
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
        '''Input only.

        The x509 PEM-encoded certificate of the CA that signed the source database server's certificate.
        The replica will use this certificate to verify it's connecting to the right host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ca_certificate GoogleDatabaseMigrationServiceConnectionProfile#ca_certificate}
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server.
        If this field is used then the 'clientKey' field is mandatory

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_certificate GoogleDatabaseMigrationServiceConnectionProfile#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate.
        If this field is used then the 'clientCertificate' field is mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_key GoogleDatabaseMigrationServiceConnectionProfile#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileOracleSsl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileOracleSslOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileOracleSslOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01a0d1ed617e7db9ed23dd53d3ca5d0d0551f87dff9d5a6c3af85bb084ca0067)
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
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__045f35572427985ada487487b4184fd78f97b387c90b39a935d024794440a0cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7bf4532a97c14e2635063103ad50fc091f94a70159b5a77f861049bd80b0859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660ea4e871e6e8c805f8eeca9aefed54f25e573f0578b08393c66f0b6bbcba91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleSsl]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleSsl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleSsl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d905789309c39e2c48c2c005078cfb10a305dc28754f0ad98948066310117d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bee23023d6b32fe24d8fbeca813fccf5a749e947bedd7c64bf5df3006caf201)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09bbf795e8f8940b68eb0302452b79d18020d7e18f7255db2797f14f6fdc8fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfilePostgresql",
    jsii_struct_bases=[],
    name_mapping={
        "alloydb_cluster_id": "alloydbClusterId",
        "cloud_sql_id": "cloudSqlId",
        "host": "host",
        "password": "password",
        "port": "port",
        "ssl": "ssl",
        "username": "username",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfilePostgresql:
    def __init__(
        self,
        *,
        alloydb_cluster_id: typing.Optional[builtins.str] = None,
        cloud_sql_id: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        ssl: typing.Optional[typing.Union["GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alloydb_cluster_id: If the connected database is an AlloyDB instance, use this field to provide the AlloyDB cluster ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#alloydb_cluster_id GoogleDatabaseMigrationServiceConnectionProfile#alloydb_cluster_id}
        :param cloud_sql_id: If the source is a Cloud SQL database, use this field to provide the Cloud SQL instance ID of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cloud_sql_id GoogleDatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        :param host: The IP or hostname of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#host GoogleDatabaseMigrationServiceConnectionProfile#host}
        :param password: Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        :param port: The network port of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ssl GoogleDatabaseMigrationServiceConnectionProfile#ssl}
        :param username: The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        '''
        if isinstance(ssl, dict):
            ssl = GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl(**ssl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a5c297140d5f8fd0af7c921b9b50b6212994eb3359d0973ef18beee55bde80)
            check_type(argname="argument alloydb_cluster_id", value=alloydb_cluster_id, expected_type=type_hints["alloydb_cluster_id"])
            check_type(argname="argument cloud_sql_id", value=cloud_sql_id, expected_type=type_hints["cloud_sql_id"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument ssl", value=ssl, expected_type=type_hints["ssl"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alloydb_cluster_id is not None:
            self._values["alloydb_cluster_id"] = alloydb_cluster_id
        if cloud_sql_id is not None:
            self._values["cloud_sql_id"] = cloud_sql_id
        if host is not None:
            self._values["host"] = host
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if ssl is not None:
            self._values["ssl"] = ssl
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def alloydb_cluster_id(self) -> typing.Optional[builtins.str]:
        '''If the connected database is an AlloyDB instance, use this field to provide the AlloyDB cluster ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#alloydb_cluster_id GoogleDatabaseMigrationServiceConnectionProfile#alloydb_cluster_id}
        '''
        result = self._values.get("alloydb_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_sql_id(self) -> typing.Optional[builtins.str]:
        '''If the source is a Cloud SQL database, use this field to provide the Cloud SQL instance ID of the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#cloud_sql_id GoogleDatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        '''
        result = self._values.get("cloud_sql_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The IP or hostname of the source MySQL database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#host GoogleDatabaseMigrationServiceConnectionProfile#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The password for the user that Database Migration Service will be using to connect to the database.
        This field is not returned on request, and the value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#password GoogleDatabaseMigrationServiceConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The network port of the source MySQL database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#port GoogleDatabaseMigrationServiceConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssl(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl"]:
        '''ssl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ssl GoogleDatabaseMigrationServiceConnectionProfile#ssl}
        '''
        result = self._values.get("ssl")
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl"], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username that Database Migration Service will use to connect to the database.

        The value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#username GoogleDatabaseMigrationServiceConnectionProfile#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfilePostgresql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfilePostgresqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfilePostgresqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84c8a2f6f1941c28bcfc6f608545e68dda6f2973c57a9b16c10a97beacbbdd26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSsl")
    def put_ssl(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ca_certificate GoogleDatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_certificate GoogleDatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_key GoogleDatabaseMigrationServiceConnectionProfile#client_key}
        :param type: The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#type GoogleDatabaseMigrationServiceConnectionProfile#type}
        '''
        value = GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl(
            ca_certificate=ca_certificate,
            client_certificate=client_certificate,
            client_key=client_key,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putSsl", [value]))

    @jsii.member(jsii_name="resetAlloydbClusterId")
    def reset_alloydb_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlloydbClusterId", []))

    @jsii.member(jsii_name="resetCloudSqlId")
    def reset_cloud_sql_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSqlId", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetSsl")
    def reset_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsl", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="networkArchitecture")
    def network_architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkArchitecture"))

    @builtins.property
    @jsii.member(jsii_name="passwordSet")
    def password_set(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "passwordSet"))

    @builtins.property
    @jsii.member(jsii_name="ssl")
    def ssl(
        self,
    ) -> "GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSslOutputReference":
        return typing.cast("GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSslOutputReference", jsii.get(self, "ssl"))

    @builtins.property
    @jsii.member(jsii_name="alloydbClusterIdInput")
    def alloydb_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alloydbClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlIdInput")
    def cloud_sql_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudSqlIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="sslInput")
    def ssl_input(
        self,
    ) -> typing.Optional["GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl"]:
        return typing.cast(typing.Optional["GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl"], jsii.get(self, "sslInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="alloydbClusterId")
    def alloydb_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alloydbClusterId"))

    @alloydb_cluster_id.setter
    def alloydb_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8286bf7ea9deef5e3e1d2c7a6d7eafc0007f84c56fa5d52fbff2dd87935f127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alloydbClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudSqlId")
    def cloud_sql_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudSqlId"))

    @cloud_sql_id.setter
    def cloud_sql_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5572e208446a046ba03cf7a323cbe9a86bcc7931515e0698aa7ad438a9bb0481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSqlId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b10a3dd3b0e87c74782cf47e020df5f2015d7446d096a4ba623f82f0e02eded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff2e818fc03f5698ba87817e44db53c00e3e6ef382e920390f5857ddb12e9f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd2657e97f552301f04530049a2c75ebfa512c53df1cee5c33863166cd512ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5647e41361b239ad911bda6af09ffa2532d7a7dbb90805dca75e74cbe2aa9e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfilePostgresql]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfilePostgresql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfilePostgresql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479554ffb7062e6239434e034bac4b3abd913df05a6e367d015b9b294ed87ffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl",
    jsii_struct_bases=[],
    name_mapping={
        "ca_certificate": "caCertificate",
        "client_certificate": "clientCertificate",
        "client_key": "clientKey",
        "type": "type",
    },
)
class GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl:
    def __init__(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ca_certificate GoogleDatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_certificate GoogleDatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_key GoogleDatabaseMigrationServiceConnectionProfile#client_key}
        :param type: The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#type GoogleDatabaseMigrationServiceConnectionProfile#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411657d0034fe6a26ca679a8a467e973feac870baa544aded6fc12e8cbf9259a)
            check_type(argname="argument ca_certificate", value=ca_certificate, expected_type=type_hints["ca_certificate"])
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument client_key", value=client_key, expected_type=type_hints["client_key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ca_certificate is not None:
            self._values["ca_certificate"] = ca_certificate
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if client_key is not None:
            self._values["client_key"] = client_key
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def ca_certificate(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The x509 PEM-encoded certificate of the CA that signed the source database server's certificate.
        The replica will use this certificate to verify it's connecting to the right host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#ca_certificate GoogleDatabaseMigrationServiceConnectionProfile#ca_certificate}
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server.
        If this field is used then the 'clientKey' field is mandatory

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_certificate GoogleDatabaseMigrationServiceConnectionProfile#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate.
        If this field is used then the 'clientCertificate' field is mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#client_key GoogleDatabaseMigrationServiceConnectionProfile#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#type GoogleDatabaseMigrationServiceConnectionProfile#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSslOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSslOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e020fd1213283f884d73f0d3b98642df55ede784f638ab8262f15a83caf2bce)
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

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertificate")
    def ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertificate"))

    @ca_certificate.setter
    def ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c02c0b1d782a4717f40674a3a6b05d9f70497e614b9e5fa84d828096191532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80312a267ca9e1c8988932e0c4079b64e17a3d8e54ff63c028e4be078388fb59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e8b5c635eadc9788c95748046806b06946bbd20d99ddecd88789dcc0179570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7752fb48397ed1c9743c11e452e008520b36b874c2c391477f7aee33eb1d21ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl]:
        return typing.cast(typing.Optional[GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87cc84408b7baf3070b0097932b1b5e72bda64b7225a2ffbc94dd323b7ef60b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDatabaseMigrationServiceConnectionProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#create GoogleDatabaseMigrationServiceConnectionProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#delete GoogleDatabaseMigrationServiceConnectionProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#update GoogleDatabaseMigrationServiceConnectionProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11a9fa80149ff2662f6ce5707b2a321bda48f26d108684090433828e0cbcb11)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#create GoogleDatabaseMigrationServiceConnectionProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#delete GoogleDatabaseMigrationServiceConnectionProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_database_migration_service_connection_profile#update GoogleDatabaseMigrationServiceConnectionProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDatabaseMigrationServiceConnectionProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDatabaseMigrationServiceConnectionProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDatabaseMigrationServiceConnectionProfile.GoogleDatabaseMigrationServiceConnectionProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e6f23930cdd0ba340a3f1d6cbaee36b6f6377f5ea00ddf77f3f3f3da80e06a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a11153ca6b0999779757dd1cb99f7bbf44f8adabac0300d81c003e69ae82dcca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4f0f2a16b1dcf6fff6eb46ef3f4c84e0f6274151c03475871ced3aee7b929b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c510c694418302831c61e2e3d5aff7215b919dd6f0cec49971c18fdde390533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceConnectionProfileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceConnectionProfileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceConnectionProfileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cbf86aad456b621858b9e49a57d4a0643ed63d82b2384b7dea13b3a928598a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDatabaseMigrationServiceConnectionProfile",
    "GoogleDatabaseMigrationServiceConnectionProfileAlloydb",
    "GoogleDatabaseMigrationServiceConnectionProfileAlloydbOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings",
    "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser",
    "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUserOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings",
    "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig",
    "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfigOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileCloudsql",
    "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings",
    "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig",
    "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks",
    "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksList",
    "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileConfig",
    "GoogleDatabaseMigrationServiceConnectionProfileError",
    "GoogleDatabaseMigrationServiceConnectionProfileErrorList",
    "GoogleDatabaseMigrationServiceConnectionProfileErrorOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileMysql",
    "GoogleDatabaseMigrationServiceConnectionProfileMysqlOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl",
    "GoogleDatabaseMigrationServiceConnectionProfileMysqlSslOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileOracle",
    "GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity",
    "GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivityOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileOracleOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity",
    "GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivityOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileOracleSsl",
    "GoogleDatabaseMigrationServiceConnectionProfileOracleSslOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity",
    "GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivityOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfilePostgresql",
    "GoogleDatabaseMigrationServiceConnectionProfilePostgresqlOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl",
    "GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSslOutputReference",
    "GoogleDatabaseMigrationServiceConnectionProfileTimeouts",
    "GoogleDatabaseMigrationServiceConnectionProfileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d01694ebbc906a04d387729c2bb0397561d102a003432bad9c18820bec51410b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connection_profile_id: builtins.str,
    alloydb: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileAlloydb, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudsql: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileCloudsql, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    mysql: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileMysql, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileOracle, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfilePostgresql, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b280534fe0d863a3c1371af7e9ff782803ac7d615c41c3defcb28e23e74b048c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5aba8a74ed9411562733e08f2798c3bb378561e8d0f211585b07d18711f5d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9503b6f4071608a7dd5915d6019e7a5de5da17b05ba7269e39ed9fd8f5f94c9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05a9971dca939fff137ce1617b551bf3b199ba1196577f76c81a729f3de8a53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d2b25f3bc4fcccca54d27b11fab45417ad504bfd4514ccdd10bfb90e6986f8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f798246b745c6e830e1620e9216d9a79b1b16281d9b3efb124fa20df2c8e404(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5cf6459a3ef0fe7f32c39296420262c2cd87dfaa9b2530ac1358de157a5ee0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ed60f604f611ea059c7f5372d01b108149cde18e193e36b75d2658e018de97(
    *,
    cluster_id: builtins.str,
    settings: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561e2d121fd7aafc330f71371f3fe9f5130b146d9c93142ef05e31fdd69b2e16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a561378881ade5485c30199d28e945d958fb3c3ad2e91baac7c989aa8c1b08fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6afdb8b214f817e4da2284b7444cfdd2f57731a3704030b3ea7017ea053b4e9(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b237996364b1436c83592ecd73b155c4b52fae3c77210288526e9a6136a9ee(
    *,
    initial_user: typing.Union[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser, typing.Dict[builtins.str, typing.Any]],
    vpc_network: builtins.str,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    primary_instance_settings: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a09d034e16cfb8541b1b40673b92eb8dd64f11abfecddc68f104c0b907d2209(
    *,
    password: builtins.str,
    user: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7459fc148fcd63a82a1ba2b96ef13b883ce11cf663f0ffa27395560788a05f86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9298a9c865503f843f57f7fcb8abe8724ac7ca18c55fa099882a1ab1cac2fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd22c25ed0346ed495eab2110b44ed6de38b1db4a81f66a2a92aef5bd1615d8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b048f8a6a891b6b05127693af64b78cef1ab4cd326e86880f891ab0d7b1c1f1(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f51f0d2b97af3d75f78eb9bc7e74983da14c9830e38be434d49b1ed60c6c524(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2d25dbf3b61654f97c834b8e02a4438e084c2f0c75fc8cabc9814b79d9b4b3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897930971619b82a245d1b267080f8fab188102e15dd33fa8bf959be8aee52da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822bafd5c8fd5d5c5f651653453b1204589b9fbfa27cfb63e1acdb90609e4b7f(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a119c5bf9a64a0e2059b4761cbdfd7eb202974deb4a90214ca0ab3a34f442e(
    *,
    id: builtins.str,
    machine_config: typing.Union[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig, typing.Dict[builtins.str, typing.Any]],
    database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d5af29c3090bd9145e70f9825d44c53dd5c3fa49cda348f7e9c886eeabd5ce(
    *,
    cpu_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1238846c4798a42c015cc35e4f260f1e97f5dfc358401aa0895e87fb3102e261(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9dc289afd9f8c98290f4c502aa6570640343932f8484468dbe0aed218db545e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d414c5f6afe12219b040827bb992802a2a57d6a2fec597fb8079754820f9ad03(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6bbae32a13b30f13e1d268f3e0f3ec01470dbc685aff092db6195a9b612839(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6cddb654d4b1b52dd503aa05881c3d9eefa0a479383435bfc5857555b5df8b9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a31eda4f3c5f3596390aef1e6f255e8440ed77042a8f54fecfb803bc6b8a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e351fc34a6acbe42a718c96990dac09fa66a90f22eed9925c1c039aa7a066e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f1d6235a82c51a124064e64e207377397f7e26c3b4e7fb5587bc731952a722(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1635efb9aab433e8e957214265cba858148ff1f8c9647b0f74649bf2119e7bf6(
    *,
    settings: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b372c6b22bd8c4e3865c635ef609d06560fd17c0a5b520eed5c74c3e4f6148(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c751730ef3ce4c84d496a7110a72eaca40e1294e59165021d1b7daa1141d9ba8(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1909a163764ffcf4ba4e87cd5b5f972113b88014ff0602b6d4ab0057e3211dae(
    *,
    source_id: builtins.str,
    activation_policy: typing.Optional[builtins.str] = None,
    auto_storage_increase: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cmek_key_name: typing.Optional[builtins.str] = None,
    collation: typing.Optional[builtins.str] = None,
    database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    database_version: typing.Optional[builtins.str] = None,
    data_disk_size_gb: typing.Optional[builtins.str] = None,
    data_disk_type: typing.Optional[builtins.str] = None,
    edition: typing.Optional[builtins.str] = None,
    ip_config: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    root_password: typing.Optional[builtins.str] = None,
    storage_auto_resize_limit: typing.Optional[builtins.str] = None,
    tier: typing.Optional[builtins.str] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d2d8fee1283784ae209eb4c532927bb1a6694f188c5e0235dcd713d6de68c6(
    *,
    authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_ipv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_network: typing.Optional[builtins.str] = None,
    require_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7c1f58ad2b9b325c8af6bc1c889e5871be2acbfde501725bd47f9cba96ff97(
    *,
    value: builtins.str,
    expire_time: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ea893a60f681f588e5d21f4f1b6d2d5b0e439c48a8d154256ba74fbfb74cc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d3b4a8b94a29db16f1d59be79942b5ad001196dd9088d27248eb997f873227(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de0a5685e029ed8e45c24d63e1b54cd5d49c90374799d2694194f6c1cf4631a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1179b56239ed7f175437be9c4d8a4b0ef717566f0e9c6050ba32bfa3536cf2f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb911bfdcc6166f2247dd4e6f3731e2535305da3a8b35effcc80837a6fd0553d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b49c28d27191e427f3e74b78aae4b388b5551787f4bceffc5dceb0a4286613b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975ee0d6c0804cfe1124722ec8d3b40de543344d5c5ba0144cb09b6e1937c94e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e92428898a5eeabe2ff683cbda2083c972268de5ca1808a3947b1f418a0373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16e11ae7e22141d95b1f12c1b13964565a177b5db9c78426ec8c0e552542f97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc43a3f6d0aa186e3c928d7b2f27460ffb6fb9ca9cfd1e5ba1c2ac0d4658d732(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__870b8420a91a47057db25fa1648a100dd639321636c9a2b93795a5f33d653507(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3775ab6a74fb4ed7a0a0a62c99e51ae934a9d54b77e856874e7dc9c0199316b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da8acf13ba2b61dee96cb6ed7cf76299bbff9d777bf44461170e13f35eb69d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db62518812e1ba05c0734b9ed893bbf89a9693b57d128f0a2d1f1aa50e2758a9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1500c37639be1ae2d1c2c6a8cbc396674b6d89042957b9ead701f4f9b75a8e17(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1dec437c8276a0bdad2ef883cb0a60ab0437a12141b3ee0aee1e34afad7d97b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02647aa27773c4896a15fa8ca1107ea6f859a57dc5a88b5e36e82b72216aa38(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c8dbc5bd6d9cba659c14e3a13a4f50717ee22f8490d78bccd26146af56beae(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9de667471cdfbdd92985ba85be82b40871de20188ff704ead64be85e12359c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b92575e48e69622fd81c86efa945cd685f15b66dc0d8de94dd26ee40a9f1a60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33dce9efbb55185f48d3e3a1b53676998fd6b21702649a3bbb4bc4b30f95ddd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0c2a59c508143012831fcbb5e82d87af92b2408964197844912408510e9b71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f8a08656e3e58faae1306da26ca8dc4f2633e23085d7c6af5ea2049f31fb26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436fa46a7ed31a89fb3825c6a1710d029b8c9d64123970852bacfc26a24c1b63(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c6379391979b4042c149b7dee1c380c044a834eacd5d89c9ad17027451f9aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133c193cbc0225030f469a06a3780fa85f80df03c10af19d4e17e6835b94dc77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34eb36c0ec7ab349616f8826a7e1ea16adaf255a31af2124fe02275f9e124784(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe17bb32cc1eb8d3dbbcdfae156ea704aac8ff8310996d56f4afae384c4b751c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a13db801cb878c090a83cd4fde03fd438bdf4f04e1d30f29601de20d4635990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91774d4b3e0cde9fb06fb3571afac3ba9121b018f8a3f616357a739414b18e66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae20b481dec63b1935d6d8cdc7f272941b0662649a0e118f376cfd843ade7410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f72415528f6ba85df17b47321f1fb1eee334be7414305f072eaa387fe391807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b3e090eaef763c6278f5291edf193215ad3210256ada4f87ace52a9765b799(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43567b21d2a79a79b7f60440404bf3d92911f4cd29a99dfb74121e5124d35d5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce2842ebbb2cdcd0c176146f78ebba89daf3fb6eab3f19664114ab7a76ddf9b(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileCloudsqlSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afcc5fc5e127d51f78d072f002b44a8ebeb5605e681f08341615305d49f85f18(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection_profile_id: builtins.str,
    alloydb: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileAlloydb, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudsql: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileCloudsql, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    mysql: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileMysql, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileOracle, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfilePostgresql, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809fb64f0a7d9d4cbed7b7a363b6ab2e96587a78b045c05e7a3a6f8b0446b265(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9001d10b9d6535ddce5092df9dc663431ef57c58c70fb71d488ba999175a7c1a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecce2d3a232c82f7ac79208b21a1ab1b80819c3c3becb9a2e9bc3d488a907978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7534e7a552f8c8581d10bf14d3940dc249a36dcb2c7e1097fbb11f80895585(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfde9690fb369047541ec0b1de97d54f76c079cd96dd133c16cafdc033e83969(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d62d6b063c438d90f57941ee4955d2e88c1b4b6ef17a94f3c8caabcbb3bdd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7917f3bd15f610fbac62d602eba0ea3f44a0a5b0e915469d6f4122d7adc67a2a(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e41d699785711bfab3a5d7746efb928849a2b6b9ed71fda6ff34e7ca0dd31d6(
    *,
    cloud_sql_id: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    ssl: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl, typing.Dict[builtins.str, typing.Any]]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc0769123f8c383e4ade5d4a466626ee30627a207f688fa3865fe93e091c296(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9781ed5529b40a949fab88bd54f2b0aec16223ed8e78fcbf8a69b358267430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79e346e16fb14262a2f34d5e44441f44342e0d86f5b52779005a979aef8d2a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357021e937f828c9015fdfdea80d760720cf3b0351c16bf36d051da2d83c90a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d138c0e58973002f60723a221aec25421341bc64a4ae5f5d03604dc1e4b813e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a8a83f83650e098248a9226921798e8814fb35848f035e119f109c39ee18fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338344e20fdce09329e458c11cb821df82740a6472a769f8fd8a559d60619c95(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileMysql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954aa6385c992731dc4399cecec47557e5ceaa937ec787ae1292dacc91e8c84c(
    *,
    ca_certificate: typing.Optional[builtins.str] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f31fd3012bb42e012b2d415482c0bcdbf794adc9a674bf12a963daabb55ab59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1c09f4b172e67b4d39032dd4203ff8b3bcbe24698a0cc1d57d57b3fd5480c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bb5a969d183c88ab819bcaabe72a9132ca9f3e73bf3c39b4e8eda222106bc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8bbf53b7cc62bed7f2c3a3e92d8cb058b4f4294d85aeefef5b61d06b1aca24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4f3d42936938d59b859c7199e2f75697c2c5cf954b7d1580ee5c541368bbd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ededa412b4de095579022aaeb8f98fc7e6e0bdc46f908cc443cd2bb68bbde1(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileMysqlSsl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb48a064d9a6f7c60f3fff518855f22e505da5b885c9d49a8fdb4d0b4cdbb92f(
    *,
    database_service: builtins.str,
    host: builtins.str,
    password: builtins.str,
    port: jsii.Number,
    username: builtins.str,
    forward_ssh_connectivity: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    private_connectivity: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileOracleSsl, typing.Dict[builtins.str, typing.Any]]] = None,
    static_service_ip_connectivity: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9eea1e6a584f80815b2713223edd5584245bf2daaceca91bf9399593f2db7e(
    *,
    hostname: builtins.str,
    port: jsii.Number,
    username: builtins.str,
    password: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f848fabb03f4227dfaea743b39229cba8e12d0fa4ed28e59c65c9094b44754(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef503848cbb6aa555e8bcca6279b728c4d0cee4d6941d17d8748412eb71149f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180502245efe6c346b6e4a7176430b577ae01dd537c7d114287f06f245cf49e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f861cd4366604600cd788dc60e1ec65b11bc0fe25793b1874939a28e4c2243(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201b10c9a3df72debcea59c0de55f61a1998f404148cca83588463ae6204735f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28ec7a6bc3d0de1b6c5bd66c02db3e47e0e53ffcbe5e65101ab3e261879448c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ac559993246f090038b267e2929f2d8916818f8ea76e0828db06e4edc2b1a9(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d2b67ec671c8bfa5a5be667b911cb80cf112d551aaf505b239d3c31dde955d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc020f1c1319a1ffd0432400175c356373c98a4d95e80fa6810b317923f61346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ebfd0678ed0c5ae8e23f6fd6395959a71bdcf563b210b618e81c44cea90d99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f4e4dd4917dcea9ed2c828fb7e9c220aaff19a92a1ebbbfcc0d469fa77ee58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24283ebe9ec99b1a4b6e829636f7201dfeb40b4e27e5dbc8c17fd786a1ae5a34(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c671ef048a1333136d14956cd7cc7580a47235eda49384d55e29eb659e09340(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53a82111a68b4fd26395737c5499fef849020253fe4377015f04906b3db62fa(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc83ac65104f2b0891eae859f01ba3f9f9e77cb1d9a0e9d0b2012d3a1ff6939(
    *,
    private_connection: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eceebc014e7e9cab5ff2934ca8ae971ecdcd7c4df847c13b38c7f17fa5012b6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c669cada0017ccefa7422a3af8415de40913b8b7c7ed0602e58f6531bbc2608(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856cbf3621d384dd676e9313743359fb1dbdce9e66e6f3911eb4269296f749fc(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279bd90caa1283367d2a339f07f1caea159185b5f7166b9c2951e0c14f770d9c(
    *,
    ca_certificate: typing.Optional[builtins.str] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a0d1ed617e7db9ed23dd53d3ca5d0d0551f87dff9d5a6c3af85bb084ca0067(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045f35572427985ada487487b4184fd78f97b387c90b39a935d024794440a0cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bf4532a97c14e2635063103ad50fc091f94a70159b5a77f861049bd80b0859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660ea4e871e6e8c805f8eeca9aefed54f25e573f0578b08393c66f0b6bbcba91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d905789309c39e2c48c2c005078cfb10a305dc28754f0ad98948066310117d8(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleSsl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bee23023d6b32fe24d8fbeca813fccf5a749e947bedd7c64bf5df3006caf201(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09bbf795e8f8940b68eb0302452b79d18020d7e18f7255db2797f14f6fdc8fcd(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a5c297140d5f8fd0af7c921b9b50b6212994eb3359d0973ef18beee55bde80(
    *,
    alloydb_cluster_id: typing.Optional[builtins.str] = None,
    cloud_sql_id: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    ssl: typing.Optional[typing.Union[GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl, typing.Dict[builtins.str, typing.Any]]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c8a2f6f1941c28bcfc6f608545e68dda6f2973c57a9b16c10a97beacbbdd26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8286bf7ea9deef5e3e1d2c7a6d7eafc0007f84c56fa5d52fbff2dd87935f127(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5572e208446a046ba03cf7a323cbe9a86bcc7931515e0698aa7ad438a9bb0481(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b10a3dd3b0e87c74782cf47e020df5f2015d7446d096a4ba623f82f0e02eded(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff2e818fc03f5698ba87817e44db53c00e3e6ef382e920390f5857ddb12e9f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd2657e97f552301f04530049a2c75ebfa512c53df1cee5c33863166cd512ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5647e41361b239ad911bda6af09ffa2532d7a7dbb90805dca75e74cbe2aa9e95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479554ffb7062e6239434e034bac4b3abd913df05a6e367d015b9b294ed87ffd(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfilePostgresql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411657d0034fe6a26ca679a8a467e973feac870baa544aded6fc12e8cbf9259a(
    *,
    ca_certificate: typing.Optional[builtins.str] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e020fd1213283f884d73f0d3b98642df55ede784f638ab8262f15a83caf2bce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c02c0b1d782a4717f40674a3a6b05d9f70497e614b9e5fa84d828096191532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80312a267ca9e1c8988932e0c4079b64e17a3d8e54ff63c028e4be078388fb59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e8b5c635eadc9788c95748046806b06946bbd20d99ddecd88789dcc0179570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7752fb48397ed1c9743c11e452e008520b36b874c2c391477f7aee33eb1d21ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87cc84408b7baf3070b0097932b1b5e72bda64b7225a2ffbc94dd323b7ef60b(
    value: typing.Optional[GoogleDatabaseMigrationServiceConnectionProfilePostgresqlSsl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11a9fa80149ff2662f6ce5707b2a321bda48f26d108684090433828e0cbcb11(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6f23930cdd0ba340a3f1d6cbaee36b6f6377f5ea00ddf77f3f3f3da80e06a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11153ca6b0999779757dd1cb99f7bbf44f8adabac0300d81c003e69ae82dcca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4f0f2a16b1dcf6fff6eb46ef3f4c84e0f6274151c03475871ced3aee7b929b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c510c694418302831c61e2e3d5aff7215b919dd6f0cec49971c18fdde390533(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cbf86aad456b621858b9e49a57d4a0643ed63d82b2384b7dea13b3a928598a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDatabaseMigrationServiceConnectionProfileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
