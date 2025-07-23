r'''
# `google_database_migration_service_connection_profile`

Refer to the Terraform Registry for docs: [`google_database_migration_service_connection_profile`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile).
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


class DatabaseMigrationServiceConnectionProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile google_database_migration_service_connection_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connection_profile_id: builtins.str,
        alloydb: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileAlloydb", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudsql: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileCloudsql", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        mysql: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileMysql", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileOracle", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfilePostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile google_database_migration_service_connection_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_profile_id: The ID of the connection profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#connection_profile_id DatabaseMigrationServiceConnectionProfile#connection_profile_id}
        :param alloydb: alloydb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#alloydb DatabaseMigrationServiceConnectionProfile#alloydb}
        :param cloudsql: cloudsql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cloudsql DatabaseMigrationServiceConnectionProfile#cloudsql}
        :param display_name: The connection profile display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#display_name DatabaseMigrationServiceConnectionProfile#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#id DatabaseMigrationServiceConnectionProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The resource labels for connection profile to use to annotate any related underlying resources such as Compute Engine VMs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#labels DatabaseMigrationServiceConnectionProfile#labels}
        :param location: The location where the connection profile should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#location DatabaseMigrationServiceConnectionProfile#location}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#mysql DatabaseMigrationServiceConnectionProfile#mysql}
        :param oracle: oracle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#oracle DatabaseMigrationServiceConnectionProfile#oracle}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#postgresql DatabaseMigrationServiceConnectionProfile#postgresql}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#project DatabaseMigrationServiceConnectionProfile#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#timeouts DatabaseMigrationServiceConnectionProfile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee107f15e32ecc699de7e35d616c41c1e7fdcb58f1898daac32b9b0d99c1bf73)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DatabaseMigrationServiceConnectionProfileConfig(
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
        '''Generates CDKTF code for importing a DatabaseMigrationServiceConnectionProfile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DatabaseMigrationServiceConnectionProfile to import.
        :param import_from_id: The id of the existing DatabaseMigrationServiceConnectionProfile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DatabaseMigrationServiceConnectionProfile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73672f351dc21c85eeb049c9ae0620be7582217a10456f120763895a506a8abc)
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
        settings: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileAlloydbSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cluster_id: Required. The AlloyDB cluster ID that this connection profile is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cluster_id DatabaseMigrationServiceConnectionProfile#cluster_id}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#settings DatabaseMigrationServiceConnectionProfile#settings}
        '''
        value = DatabaseMigrationServiceConnectionProfileAlloydb(
            cluster_id=cluster_id, settings=settings
        )

        return typing.cast(None, jsii.invoke(self, "putAlloydb", [value]))

    @jsii.member(jsii_name="putCloudsql")
    def put_cloudsql(
        self,
        *,
        settings: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileCloudsqlSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#settings DatabaseMigrationServiceConnectionProfile#settings}
        '''
        value = DatabaseMigrationServiceConnectionProfileCloudsql(settings=settings)

        return typing.cast(None, jsii.invoke(self, "putCloudsql", [value]))

    @jsii.member(jsii_name="putMysql")
    def put_mysql(
        self,
        *,
        cloud_sql_id: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        ssl: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileMysqlSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_sql_id: If the source is a Cloud SQL database, use this field to provide the Cloud SQL instance ID of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cloud_sql_id DatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        :param host: The IP or hostname of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#host DatabaseMigrationServiceConnectionProfile#host}
        :param password: Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        :param port: The network port of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ssl DatabaseMigrationServiceConnectionProfile#ssl}
        :param username: The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        '''
        value = DatabaseMigrationServiceConnectionProfileMysql(
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
        forward_ssh_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        private_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileOracleSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        static_service_ip_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_service: Required. Database service for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_service DatabaseMigrationServiceConnectionProfile#database_service}
        :param host: Required. The IP or hostname of the source Oracle database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#host DatabaseMigrationServiceConnectionProfile#host}
        :param password: Required. Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        :param port: Required. The network port of the source Oracle database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        :param username: Required. The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        :param forward_ssh_connectivity: forward_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#forward_ssh_connectivity DatabaseMigrationServiceConnectionProfile#forward_ssh_connectivity}
        :param private_connectivity: private_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_connectivity DatabaseMigrationServiceConnectionProfile#private_connectivity}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ssl DatabaseMigrationServiceConnectionProfile#ssl}
        :param static_service_ip_connectivity: static_service_ip_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#static_service_ip_connectivity DatabaseMigrationServiceConnectionProfile#static_service_ip_connectivity}
        '''
        value = DatabaseMigrationServiceConnectionProfileOracle(
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
        ssl: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfilePostgresqlSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alloydb_cluster_id: If the connected database is an AlloyDB instance, use this field to provide the AlloyDB cluster ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#alloydb_cluster_id DatabaseMigrationServiceConnectionProfile#alloydb_cluster_id}
        :param cloud_sql_id: If the source is a Cloud SQL database, use this field to provide the Cloud SQL instance ID of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cloud_sql_id DatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        :param host: The IP or hostname of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#host DatabaseMigrationServiceConnectionProfile#host}
        :param password: Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        :param port: The network port of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ssl DatabaseMigrationServiceConnectionProfile#ssl}
        :param username: The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        '''
        value = DatabaseMigrationServiceConnectionProfilePostgresql(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#create DatabaseMigrationServiceConnectionProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#delete DatabaseMigrationServiceConnectionProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#update DatabaseMigrationServiceConnectionProfile#update}.
        '''
        value = DatabaseMigrationServiceConnectionProfileTimeouts(
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
    ) -> "DatabaseMigrationServiceConnectionProfileAlloydbOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileAlloydbOutputReference", jsii.get(self, "alloydb"))

    @builtins.property
    @jsii.member(jsii_name="cloudsql")
    def cloudsql(
        self,
    ) -> "DatabaseMigrationServiceConnectionProfileCloudsqlOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileCloudsqlOutputReference", jsii.get(self, "cloudsql"))

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
    def error(self) -> "DatabaseMigrationServiceConnectionProfileErrorList":
        return typing.cast("DatabaseMigrationServiceConnectionProfileErrorList", jsii.get(self, "error"))

    @builtins.property
    @jsii.member(jsii_name="mysql")
    def mysql(self) -> "DatabaseMigrationServiceConnectionProfileMysqlOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileMysqlOutputReference", jsii.get(self, "mysql"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="oracle")
    def oracle(
        self,
    ) -> "DatabaseMigrationServiceConnectionProfileOracleOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileOracleOutputReference", jsii.get(self, "oracle"))

    @builtins.property
    @jsii.member(jsii_name="postgresql")
    def postgresql(
        self,
    ) -> "DatabaseMigrationServiceConnectionProfilePostgresqlOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfilePostgresqlOutputReference", jsii.get(self, "postgresql"))

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
    ) -> "DatabaseMigrationServiceConnectionProfileTimeoutsOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="alloydbInput")
    def alloydb_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileAlloydb"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileAlloydb"], jsii.get(self, "alloydbInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudsqlInput")
    def cloudsql_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileCloudsql"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileCloudsql"], jsii.get(self, "cloudsqlInput"))

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
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileMysql"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileMysql"], jsii.get(self, "mysqlInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleInput")
    def oracle_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileOracle"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileOracle"], jsii.get(self, "oracleInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlInput")
    def postgresql_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfilePostgresql"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfilePostgresql"], jsii.get(self, "postgresqlInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DatabaseMigrationServiceConnectionProfileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DatabaseMigrationServiceConnectionProfileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionProfileId")
    def connection_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionProfileId"))

    @connection_profile_id.setter
    def connection_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a578d97fe3b5858f83f3cae36f3a4ef494aefa5925783e0996bc4585dfa4771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionProfileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6352c23d13920c1c11aaba4c5c9d4a36bf8ebaa3c6acde4d2629169be7bce417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2726e3e09a2f0a635915552799171af2cf8b2c377ea06ead36813d55d548d35a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0ad497cfadfaa18b1b8d3c56a3b22599eecf1f8ff7b1f55d903719efc52d40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f55e6864b9cd7f0ebad2beb46359331d3293785382d393c6724bbf427514791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dcaa868af6838ad878decd98972e248964261c8494d166dafd5928a7d2a7a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileAlloydb",
    jsii_struct_bases=[],
    name_mapping={"cluster_id": "clusterId", "settings": "settings"},
)
class DatabaseMigrationServiceConnectionProfileAlloydb:
    def __init__(
        self,
        *,
        cluster_id: builtins.str,
        settings: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileAlloydbSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cluster_id: Required. The AlloyDB cluster ID that this connection profile is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cluster_id DatabaseMigrationServiceConnectionProfile#cluster_id}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#settings DatabaseMigrationServiceConnectionProfile#settings}
        '''
        if isinstance(settings, dict):
            settings = DatabaseMigrationServiceConnectionProfileAlloydbSettings(**settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd16f8bda8488f726e9fc7c00ead05ba41bc82f1d9d90b546e1a9351da831fb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cluster_id DatabaseMigrationServiceConnectionProfile#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileAlloydbSettings"]:
        '''settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#settings DatabaseMigrationServiceConnectionProfile#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileAlloydbSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileAlloydb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileAlloydbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileAlloydbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc051083d0ee97096bcf9d6b1278e3173aadbeefb63b9c1f61dc6addee117d61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        *,
        initial_user: typing.Union["DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser", typing.Dict[builtins.str, typing.Any]],
        vpc_network: builtins.str,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        primary_instance_settings: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param initial_user: initial_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#initial_user DatabaseMigrationServiceConnectionProfile#initial_user}
        :param vpc_network: Required. The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP. The network must belong to the same project as the cluster. It is specified in the form: 'projects/{project_number}/global/networks/{network_id}'. This is required to create a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#vpc_network DatabaseMigrationServiceConnectionProfile#vpc_network}
        :param labels: Labels for the AlloyDB cluster created by DMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#labels DatabaseMigrationServiceConnectionProfile#labels}
        :param primary_instance_settings: primary_instance_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#primary_instance_settings DatabaseMigrationServiceConnectionProfile#primary_instance_settings}
        '''
        value = DatabaseMigrationServiceConnectionProfileAlloydbSettings(
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
    ) -> "DatabaseMigrationServiceConnectionProfileAlloydbSettingsOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileAlloydbSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileAlloydbSettings"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileAlloydbSettings"], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac8ebad5000e0911bc9bb1dec75394e009abdcd9a1cc90a13edd0d79005937a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydb]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a0299c4bb190dd8b6a366967a2d444df7398d04e52de16dd09c8a2842428fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileAlloydbSettings",
    jsii_struct_bases=[],
    name_mapping={
        "initial_user": "initialUser",
        "vpc_network": "vpcNetwork",
        "labels": "labels",
        "primary_instance_settings": "primaryInstanceSettings",
    },
)
class DatabaseMigrationServiceConnectionProfileAlloydbSettings:
    def __init__(
        self,
        *,
        initial_user: typing.Union["DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser", typing.Dict[builtins.str, typing.Any]],
        vpc_network: builtins.str,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        primary_instance_settings: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param initial_user: initial_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#initial_user DatabaseMigrationServiceConnectionProfile#initial_user}
        :param vpc_network: Required. The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP. The network must belong to the same project as the cluster. It is specified in the form: 'projects/{project_number}/global/networks/{network_id}'. This is required to create a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#vpc_network DatabaseMigrationServiceConnectionProfile#vpc_network}
        :param labels: Labels for the AlloyDB cluster created by DMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#labels DatabaseMigrationServiceConnectionProfile#labels}
        :param primary_instance_settings: primary_instance_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#primary_instance_settings DatabaseMigrationServiceConnectionProfile#primary_instance_settings}
        '''
        if isinstance(initial_user, dict):
            initial_user = DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser(**initial_user)
        if isinstance(primary_instance_settings, dict):
            primary_instance_settings = DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings(**primary_instance_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b6c5b37ddc1a7c380741a81b22b47e856570adafda7a04ad2c4919ceef14d34)
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
    ) -> "DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser":
        '''initial_user block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#initial_user DatabaseMigrationServiceConnectionProfile#initial_user}
        '''
        result = self._values.get("initial_user")
        assert result is not None, "Required property 'initial_user' is missing"
        return typing.cast("DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser", result)

    @builtins.property
    def vpc_network(self) -> builtins.str:
        '''Required.

        The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP. The network must belong to the same project as the cluster.
        It is specified in the form: 'projects/{project_number}/global/networks/{network_id}'. This is required to create a cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#vpc_network DatabaseMigrationServiceConnectionProfile#vpc_network}
        '''
        result = self._values.get("vpc_network")
        assert result is not None, "Required property 'vpc_network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels for the AlloyDB cluster created by DMS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#labels DatabaseMigrationServiceConnectionProfile#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def primary_instance_settings(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings"]:
        '''primary_instance_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#primary_instance_settings DatabaseMigrationServiceConnectionProfile#primary_instance_settings}
        '''
        result = self._values.get("primary_instance_settings")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileAlloydbSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "user": "user"},
)
class DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser:
    def __init__(self, *, password: builtins.str, user: builtins.str) -> None:
        '''
        :param password: The initial password for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        :param user: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#user DatabaseMigrationServiceConnectionProfile#user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ef02e658d274cb5543578c8d449d99f9a3b9ad15b19fcb9821ea3834f707354)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "user": user,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''The initial password for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user(self) -> builtins.str:
        '''The database username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#user DatabaseMigrationServiceConnectionProfile#user}
        '''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c942d5a0ef7e526b2041e61a1472b87819b05936be45652ecc6a0348dbb35eb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__554b6d0062158b29f4be518112b5a7ec42c22b4f20fe5ec0dbc60d17e6b108bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af29ce75b0542dec19dca902859a1bc72d11eca78265fb3b9e0fc4263f4e040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad794a34f40d5cf869466c452869dcb545e570204f56e320384d5d3d22b709c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DatabaseMigrationServiceConnectionProfileAlloydbSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileAlloydbSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70f33fde6d6287c96d0e36b4432771a3014647919f903624d62ec0ab71a2c314)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInitialUser")
    def put_initial_user(self, *, password: builtins.str, user: builtins.str) -> None:
        '''
        :param password: The initial password for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        :param user: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#user DatabaseMigrationServiceConnectionProfile#user}
        '''
        value = DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser(
            password=password, user=user
        )

        return typing.cast(None, jsii.invoke(self, "putInitialUser", [value]))

    @jsii.member(jsii_name="putPrimaryInstanceSettings")
    def put_primary_instance_settings(
        self,
        *,
        id: builtins.str,
        machine_config: typing.Union["DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig", typing.Dict[builtins.str, typing.Any]],
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#id DatabaseMigrationServiceConnectionProfile#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param machine_config: machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#machine_config DatabaseMigrationServiceConnectionProfile#machine_config}
        :param database_flags: Database flags to pass to AlloyDB when DMS is creating the AlloyDB cluster and instances. See the AlloyDB documentation for how these can be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_flags DatabaseMigrationServiceConnectionProfile#database_flags}
        :param labels: Labels for the AlloyDB primary instance created by DMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#labels DatabaseMigrationServiceConnectionProfile#labels}
        '''
        value = DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings(
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
    ) -> DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUserOutputReference:
        return typing.cast(DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUserOutputReference, jsii.get(self, "initialUser"))

    @builtins.property
    @jsii.member(jsii_name="primaryInstanceSettings")
    def primary_instance_settings(
        self,
    ) -> "DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsOutputReference", jsii.get(self, "primaryInstanceSettings"))

    @builtins.property
    @jsii.member(jsii_name="initialUserInput")
    def initial_user_input(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser], jsii.get(self, "initialUserInput"))

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
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings"], jsii.get(self, "primaryInstanceSettingsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6f289e885dcee0f4408b011a451b5c11af059536a26f076fd4f6fbde1d770fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcNetwork")
    def vpc_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcNetwork"))

    @vpc_network.setter
    def vpc_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaea7ffa245f3a3842c179422671bd58fe518bd54d0c886a38e8d7ddf0ba0672)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettings]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43543b3a81f983aef457789e0b02d941567618e537c23d217713ef937b4a0e7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "machine_config": "machineConfig",
        "database_flags": "databaseFlags",
        "labels": "labels",
    },
)
class DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings:
    def __init__(
        self,
        *,
        id: builtins.str,
        machine_config: typing.Union["DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig", typing.Dict[builtins.str, typing.Any]],
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#id DatabaseMigrationServiceConnectionProfile#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param machine_config: machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#machine_config DatabaseMigrationServiceConnectionProfile#machine_config}
        :param database_flags: Database flags to pass to AlloyDB when DMS is creating the AlloyDB cluster and instances. See the AlloyDB documentation for how these can be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_flags DatabaseMigrationServiceConnectionProfile#database_flags}
        :param labels: Labels for the AlloyDB primary instance created by DMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#labels DatabaseMigrationServiceConnectionProfile#labels}
        '''
        if isinstance(machine_config, dict):
            machine_config = DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig(**machine_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f793181036ad5e5b8b9899c4d2119ee21f5077f40d0be393a9592f3028e921)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#id DatabaseMigrationServiceConnectionProfile#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def machine_config(
        self,
    ) -> "DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig":
        '''machine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#machine_config DatabaseMigrationServiceConnectionProfile#machine_config}
        '''
        result = self._values.get("machine_config")
        assert result is not None, "Required property 'machine_config' is missing"
        return typing.cast("DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig", result)

    @builtins.property
    def database_flags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Database flags to pass to AlloyDB when DMS is creating the AlloyDB cluster and instances.

        See the AlloyDB documentation for how these can be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_flags DatabaseMigrationServiceConnectionProfile#database_flags}
        '''
        result = self._values.get("database_flags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels for the AlloyDB primary instance created by DMS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#labels DatabaseMigrationServiceConnectionProfile#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig",
    jsii_struct_bases=[],
    name_mapping={"cpu_count": "cpuCount"},
)
class DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig:
    def __init__(self, *, cpu_count: jsii.Number) -> None:
        '''
        :param cpu_count: The number of CPU's in the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cpu_count DatabaseMigrationServiceConnectionProfile#cpu_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3dcb69b73e9a031effc6987e8b3866fa4d759834e209068b241abdb1331ec12)
            check_type(argname="argument cpu_count", value=cpu_count, expected_type=type_hints["cpu_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu_count": cpu_count,
        }

    @builtins.property
    def cpu_count(self) -> jsii.Number:
        '''The number of CPU's in the VM instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cpu_count DatabaseMigrationServiceConnectionProfile#cpu_count}
        '''
        result = self._values.get("cpu_count")
        assert result is not None, "Required property 'cpu_count' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15aa8e8d19a3e4705f6a457f87401b9c4d163fd038da6e24e7e23a8c9652634f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97e3a662fe1cd314aa40e23a70fd1a39193fc1d3b72d46fc8e9b26d38e4ff619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55aa0f7564d1da9d064f064f5ef3b8b0d7f2cbc92c2612db3c2f7b45fb9e3ded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5b8a61999350bd1a6b63f35cdfca8de2e7332f2c89d3497565f14aecbd6c1ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMachineConfig")
    def put_machine_config(self, *, cpu_count: jsii.Number) -> None:
        '''
        :param cpu_count: The number of CPU's in the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cpu_count DatabaseMigrationServiceConnectionProfile#cpu_count}
        '''
        value = DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig(
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
    ) -> DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfigOutputReference:
        return typing.cast(DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfigOutputReference, jsii.get(self, "machineConfig"))

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
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig], jsii.get(self, "machineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseFlags")
    def database_flags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "databaseFlags"))

    @database_flags.setter
    def database_flags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f19b14b870c1ea292636ac0ec8c5ce89b906d2d4fb00a5139db78a0380acbd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseFlags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d9e81a455ea460b0f7e07aece4ed72130979b1fec07ff88c043a256dbeb582f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344099e96b523069c71e53b7a0e9f9a9a55fe8405165287c133bceda239dd4eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2986a31c0fc40595da1924da70a4bd3e69979d6f0dc6dc76e75765106d3ed568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileCloudsql",
    jsii_struct_bases=[],
    name_mapping={"settings": "settings"},
)
class DatabaseMigrationServiceConnectionProfileCloudsql:
    def __init__(
        self,
        *,
        settings: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileCloudsqlSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#settings DatabaseMigrationServiceConnectionProfile#settings}
        '''
        if isinstance(settings, dict):
            settings = DatabaseMigrationServiceConnectionProfileCloudsqlSettings(**settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad759f28eddfc1bb17ba353bb107bc6a73b090ebd04c40a50c37e98f918f77d)
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if settings is not None:
            self._values["settings"] = settings

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileCloudsqlSettings"]:
        '''settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#settings DatabaseMigrationServiceConnectionProfile#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileCloudsqlSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileCloudsql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileCloudsqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileCloudsqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea41376fde5e4dad5ca38869544e036b2279a6c7cc1302eacb63c34a8ffbe618)
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
        ip_config: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_password: typing.Optional[builtins.str] = None,
        storage_auto_resize_limit: typing.Optional[builtins.str] = None,
        tier: typing.Optional[builtins.str] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_id: The Database Migration Service source connection profile ID, in the format: projects/my_project_name/locations/us-central1/connectionProfiles/connection_profile_ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#source_id DatabaseMigrationServiceConnectionProfile#source_id}
        :param activation_policy: The activation policy specifies when the instance is activated; it is applicable only when the instance state is 'RUNNABLE'. Possible values: ["ALWAYS", "NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#activation_policy DatabaseMigrationServiceConnectionProfile#activation_policy}
        :param auto_storage_increase: If you enable this setting, Cloud SQL checks your available storage every 30 seconds. If the available storage falls below a threshold size, Cloud SQL automatically adds additional storage capacity. If the available storage repeatedly falls below the threshold size, Cloud SQL continues to add storage until it reaches the maximum of 30 TB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#auto_storage_increase DatabaseMigrationServiceConnectionProfile#auto_storage_increase}
        :param cmek_key_name: The KMS key name used for the csql instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cmek_key_name DatabaseMigrationServiceConnectionProfile#cmek_key_name}
        :param collation: The Cloud SQL default instance level collation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#collation DatabaseMigrationServiceConnectionProfile#collation}
        :param database_flags: The database flags passed to the Cloud SQL instance at startup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_flags DatabaseMigrationServiceConnectionProfile#database_flags}
        :param database_version: The database engine type and version. Currently supported values located at https://cloud.google.com/database-migration/docs/reference/rest/v1/projects.locations.connectionProfiles#sqldatabaseversion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_version DatabaseMigrationServiceConnectionProfile#database_version}
        :param data_disk_size_gb: The storage capacity available to the database, in GB. The minimum (and default) size is 10GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#data_disk_size_gb DatabaseMigrationServiceConnectionProfile#data_disk_size_gb}
        :param data_disk_type: The type of storage. Possible values: ["PD_SSD", "PD_HDD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#data_disk_type DatabaseMigrationServiceConnectionProfile#data_disk_type}
        :param edition: The edition of the given Cloud SQL instance. Possible values: ["ENTERPRISE", "ENTERPRISE_PLUS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#edition DatabaseMigrationServiceConnectionProfile#edition}
        :param ip_config: ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ip_config DatabaseMigrationServiceConnectionProfile#ip_config}
        :param root_password: Input only. Initial root password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#root_password DatabaseMigrationServiceConnectionProfile#root_password}
        :param storage_auto_resize_limit: The maximum size to which storage capacity can be automatically increased. The default value is 0, which specifies that there is no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#storage_auto_resize_limit DatabaseMigrationServiceConnectionProfile#storage_auto_resize_limit}
        :param tier: The tier (or machine type) for this instance, for example: db-n1-standard-1 (MySQL instances) or db-custom-1-3840 (PostgreSQL instances). For more information, see https://cloud.google.com/sql/docs/mysql/instance-settings Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#tier DatabaseMigrationServiceConnectionProfile#tier}
        :param user_labels: The resource labels for a Cloud SQL instance to use to annotate any related underlying resources such as Compute Engine VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#user_labels DatabaseMigrationServiceConnectionProfile#user_labels}
        :param zone: The Google Cloud Platform zone where your Cloud SQL datdabse instance is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#zone DatabaseMigrationServiceConnectionProfile#zone}
        '''
        value = DatabaseMigrationServiceConnectionProfileCloudsqlSettings(
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
    ) -> "DatabaseMigrationServiceConnectionProfileCloudsqlSettingsOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileCloudsqlSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileCloudsqlSettings"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileCloudsqlSettings"], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsql]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26aa7130715d320c2e4407a3765764801a87927bbd95709b326f10ee938148d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileCloudsqlSettings",
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
class DatabaseMigrationServiceConnectionProfileCloudsqlSettings:
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
        ip_config: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_password: typing.Optional[builtins.str] = None,
        storage_auto_resize_limit: typing.Optional[builtins.str] = None,
        tier: typing.Optional[builtins.str] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_id: The Database Migration Service source connection profile ID, in the format: projects/my_project_name/locations/us-central1/connectionProfiles/connection_profile_ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#source_id DatabaseMigrationServiceConnectionProfile#source_id}
        :param activation_policy: The activation policy specifies when the instance is activated; it is applicable only when the instance state is 'RUNNABLE'. Possible values: ["ALWAYS", "NEVER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#activation_policy DatabaseMigrationServiceConnectionProfile#activation_policy}
        :param auto_storage_increase: If you enable this setting, Cloud SQL checks your available storage every 30 seconds. If the available storage falls below a threshold size, Cloud SQL automatically adds additional storage capacity. If the available storage repeatedly falls below the threshold size, Cloud SQL continues to add storage until it reaches the maximum of 30 TB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#auto_storage_increase DatabaseMigrationServiceConnectionProfile#auto_storage_increase}
        :param cmek_key_name: The KMS key name used for the csql instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cmek_key_name DatabaseMigrationServiceConnectionProfile#cmek_key_name}
        :param collation: The Cloud SQL default instance level collation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#collation DatabaseMigrationServiceConnectionProfile#collation}
        :param database_flags: The database flags passed to the Cloud SQL instance at startup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_flags DatabaseMigrationServiceConnectionProfile#database_flags}
        :param database_version: The database engine type and version. Currently supported values located at https://cloud.google.com/database-migration/docs/reference/rest/v1/projects.locations.connectionProfiles#sqldatabaseversion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_version DatabaseMigrationServiceConnectionProfile#database_version}
        :param data_disk_size_gb: The storage capacity available to the database, in GB. The minimum (and default) size is 10GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#data_disk_size_gb DatabaseMigrationServiceConnectionProfile#data_disk_size_gb}
        :param data_disk_type: The type of storage. Possible values: ["PD_SSD", "PD_HDD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#data_disk_type DatabaseMigrationServiceConnectionProfile#data_disk_type}
        :param edition: The edition of the given Cloud SQL instance. Possible values: ["ENTERPRISE", "ENTERPRISE_PLUS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#edition DatabaseMigrationServiceConnectionProfile#edition}
        :param ip_config: ip_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ip_config DatabaseMigrationServiceConnectionProfile#ip_config}
        :param root_password: Input only. Initial root password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#root_password DatabaseMigrationServiceConnectionProfile#root_password}
        :param storage_auto_resize_limit: The maximum size to which storage capacity can be automatically increased. The default value is 0, which specifies that there is no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#storage_auto_resize_limit DatabaseMigrationServiceConnectionProfile#storage_auto_resize_limit}
        :param tier: The tier (or machine type) for this instance, for example: db-n1-standard-1 (MySQL instances) or db-custom-1-3840 (PostgreSQL instances). For more information, see https://cloud.google.com/sql/docs/mysql/instance-settings Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#tier DatabaseMigrationServiceConnectionProfile#tier}
        :param user_labels: The resource labels for a Cloud SQL instance to use to annotate any related underlying resources such as Compute Engine VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#user_labels DatabaseMigrationServiceConnectionProfile#user_labels}
        :param zone: The Google Cloud Platform zone where your Cloud SQL datdabse instance is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#zone DatabaseMigrationServiceConnectionProfile#zone}
        '''
        if isinstance(ip_config, dict):
            ip_config = DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig(**ip_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00c5c553350151991716290e5cc6b9c4cd25fcb5044d7cafb48e62cb91037ee)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#source_id DatabaseMigrationServiceConnectionProfile#source_id}
        '''
        result = self._values.get("source_id")
        assert result is not None, "Required property 'source_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def activation_policy(self) -> typing.Optional[builtins.str]:
        '''The activation policy specifies when the instance is activated;

        it is applicable only when the instance state is 'RUNNABLE'. Possible values: ["ALWAYS", "NEVER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#activation_policy DatabaseMigrationServiceConnectionProfile#activation_policy}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#auto_storage_increase DatabaseMigrationServiceConnectionProfile#auto_storage_increase}
        '''
        result = self._values.get("auto_storage_increase")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cmek_key_name(self) -> typing.Optional[builtins.str]:
        '''The KMS key name used for the csql instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cmek_key_name DatabaseMigrationServiceConnectionProfile#cmek_key_name}
        '''
        result = self._values.get("cmek_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def collation(self) -> typing.Optional[builtins.str]:
        '''The Cloud SQL default instance level collation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#collation DatabaseMigrationServiceConnectionProfile#collation}
        '''
        result = self._values.get("collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_flags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The database flags passed to the Cloud SQL instance at startup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_flags DatabaseMigrationServiceConnectionProfile#database_flags}
        '''
        result = self._values.get("database_flags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def database_version(self) -> typing.Optional[builtins.str]:
        '''The database engine type and version. Currently supported values located at https://cloud.google.com/database-migration/docs/reference/rest/v1/projects.locations.connectionProfiles#sqldatabaseversion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_version DatabaseMigrationServiceConnectionProfile#database_version}
        '''
        result = self._values.get("database_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_disk_size_gb(self) -> typing.Optional[builtins.str]:
        '''The storage capacity available to the database, in GB. The minimum (and default) size is 10GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#data_disk_size_gb DatabaseMigrationServiceConnectionProfile#data_disk_size_gb}
        '''
        result = self._values.get("data_disk_size_gb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_disk_type(self) -> typing.Optional[builtins.str]:
        '''The type of storage. Possible values: ["PD_SSD", "PD_HDD"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#data_disk_type DatabaseMigrationServiceConnectionProfile#data_disk_type}
        '''
        result = self._values.get("data_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''The edition of the given Cloud SQL instance. Possible values: ["ENTERPRISE", "ENTERPRISE_PLUS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#edition DatabaseMigrationServiceConnectionProfile#edition}
        '''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_config(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig"]:
        '''ip_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ip_config DatabaseMigrationServiceConnectionProfile#ip_config}
        '''
        result = self._values.get("ip_config")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig"], result)

    @builtins.property
    def root_password(self) -> typing.Optional[builtins.str]:
        '''Input only. Initial root password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#root_password DatabaseMigrationServiceConnectionProfile#root_password}
        '''
        result = self._values.get("root_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_auto_resize_limit(self) -> typing.Optional[builtins.str]:
        '''The maximum size to which storage capacity can be automatically increased.

        The default value is 0, which specifies that there is no limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#storage_auto_resize_limit DatabaseMigrationServiceConnectionProfile#storage_auto_resize_limit}
        '''
        result = self._values.get("storage_auto_resize_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''The tier (or machine type) for this instance, for example: db-n1-standard-1 (MySQL instances) or db-custom-1-3840 (PostgreSQL instances).

        For more information, see https://cloud.google.com/sql/docs/mysql/instance-settings

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#tier DatabaseMigrationServiceConnectionProfile#tier}
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The resource labels for a Cloud SQL instance to use to annotate any related underlying resources such as Compute Engine VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#user_labels DatabaseMigrationServiceConnectionProfile#user_labels}
        '''
        result = self._values.get("user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Platform zone where your Cloud SQL datdabse instance is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#zone DatabaseMigrationServiceConnectionProfile#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileCloudsqlSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorized_networks": "authorizedNetworks",
        "enable_ipv4": "enableIpv4",
        "private_network": "privateNetwork",
        "require_ssl": "requireSsl",
    },
)
class DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig:
    def __init__(
        self,
        *,
        authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_ipv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_network: typing.Optional[builtins.str] = None,
        require_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param authorized_networks: authorized_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#authorized_networks DatabaseMigrationServiceConnectionProfile#authorized_networks}
        :param enable_ipv4: Whether the instance should be assigned an IPv4 address or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#enable_ipv4 DatabaseMigrationServiceConnectionProfile#enable_ipv4}
        :param private_network: The resource link for the VPC network from which the Cloud SQL instance is accessible for private IP. For example, projects/myProject/global/networks/default. This setting can be updated, but it cannot be removed after it is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_network DatabaseMigrationServiceConnectionProfile#private_network}
        :param require_ssl: Whether SSL connections over IP should be enforced or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#require_ssl DatabaseMigrationServiceConnectionProfile#require_ssl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4bd6c28b1f6823b6646b76015177ef4efaba909befeb8bc65089a652cf0a83)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks"]]]:
        '''authorized_networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#authorized_networks DatabaseMigrationServiceConnectionProfile#authorized_networks}
        '''
        result = self._values.get("authorized_networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks"]]], result)

    @builtins.property
    def enable_ipv4(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance should be assigned an IPv4 address or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#enable_ipv4 DatabaseMigrationServiceConnectionProfile#enable_ipv4}
        '''
        result = self._values.get("enable_ipv4")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_network(self) -> typing.Optional[builtins.str]:
        '''The resource link for the VPC network from which the Cloud SQL instance is accessible for private IP.

        For example, projects/myProject/global/networks/default.
        This setting can be updated, but it cannot be removed after it is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_network DatabaseMigrationServiceConnectionProfile#private_network}
        '''
        result = self._values.get("private_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether SSL connections over IP should be enforced or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#require_ssl DatabaseMigrationServiceConnectionProfile#require_ssl}
        '''
        result = self._values.get("require_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "expire_time": "expireTime",
        "label": "label",
        "ttl": "ttl",
    },
)
class DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks:
    def __init__(
        self,
        *,
        value: builtins.str,
        expire_time: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: The allowlisted value for the access control list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#value DatabaseMigrationServiceConnectionProfile#value}
        :param expire_time: The time when this access control entry expires in RFC 3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#expire_time DatabaseMigrationServiceConnectionProfile#expire_time}
        :param label: A label to identify this entry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#label DatabaseMigrationServiceConnectionProfile#label}
        :param ttl: Input only. The time-to-leave of this access control entry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ttl DatabaseMigrationServiceConnectionProfile#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac25165377599e5bc2b8983b18c183b76706e8d8ccc69046c161284e588bc491)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#value DatabaseMigrationServiceConnectionProfile#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expire_time(self) -> typing.Optional[builtins.str]:
        '''The time when this access control entry expires in RFC 3339 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#expire_time DatabaseMigrationServiceConnectionProfile#expire_time}
        '''
        result = self._values.get("expire_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''A label to identify this entry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#label DatabaseMigrationServiceConnectionProfile#label}
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(self) -> typing.Optional[builtins.str]:
        '''Input only. The time-to-leave of this access control entry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ttl DatabaseMigrationServiceConnectionProfile#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41e4beb0404d874a19a9b49ed1791c4814b6cdc2266b9c7438e790e09156301f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b62a7bbd12bc73b339d711c01fbac552e100bf4267c73bbcbfa587fc641b18)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3bb4cdd3f8ec1f65bd5b45f47778e18a99b966596c68bf9caeac6d820eb275)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a48686a35f56fad12647c167a1a5641e945011140ff5931f447992cb7078cea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0f2090f1c8c59897669b97f4b078cdd32989e5a32922f07a3e3ba64d96761cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad05faf7a21b9bf9f8662698e1e12abc69b45e5b60ebfe323b62660d38a05d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90b5dc1be63fdea81d697c5d7a489d0d60af2d5e83292b0a5a39b0323f71f71d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5509a256fe0a2db3a3f9de815df4701ab3b48b52f1c1899410c7dee48dc432e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f7b83d96bc19e05cf54ebe2487c84bf2be2f50d77729e17d4b6315f4f4815f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f565a93f34ea7c963316d8139600bd408c3c4172151da31d003c27bb1baaae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7004bef7bb00b36fa5ed67b9bd62b157d51404eecde628931af11427492066f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c5adc0123c9caf566cbe84df52042333a083d46aad264aaf07d67be1cd4064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83b518b3043a3b166a067c182217151d1cb13b314ed4905ee0284a83716194e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizedNetworks")
    def put_authorized_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e43d23a0bbc313a3bedcea9dbcf9616ed928cc7d4125caeb02f6b7ec0d8675)
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
    ) -> DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksList:
        return typing.cast(DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksList, jsii.get(self, "authorizedNetworks"))

    @builtins.property
    @jsii.member(jsii_name="authorizedNetworksInput")
    def authorized_networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]], jsii.get(self, "authorizedNetworksInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__89da3e518cc18bad3e931f4599de95c5f79e75a6919a1a264b47756b7788b241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIpv4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateNetwork")
    def private_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateNetwork"))

    @private_network.setter
    def private_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914d1dd537cbebc5d1e199399a085224871ca50938a2dc7549b1b9cff33d845d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27afc680e80faec9b4a62d033b010d52758254c048bf549c906e4abc35dc2fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aba16380d523eaf5a716b994b13e1faf482087ea9a88223d84670844a0c9170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DatabaseMigrationServiceConnectionProfileCloudsqlSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileCloudsqlSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5432c4ad240d42f35dc3366d4f0194ced4e7703092a24d5f97c60f5574c1a950)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpConfig")
    def put_ip_config(
        self,
        *,
        authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
        enable_ipv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_network: typing.Optional[builtins.str] = None,
        require_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param authorized_networks: authorized_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#authorized_networks DatabaseMigrationServiceConnectionProfile#authorized_networks}
        :param enable_ipv4: Whether the instance should be assigned an IPv4 address or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#enable_ipv4 DatabaseMigrationServiceConnectionProfile#enable_ipv4}
        :param private_network: The resource link for the VPC network from which the Cloud SQL instance is accessible for private IP. For example, projects/myProject/global/networks/default. This setting can be updated, but it cannot be removed after it is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_network DatabaseMigrationServiceConnectionProfile#private_network}
        :param require_ssl: Whether SSL connections over IP should be enforced or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#require_ssl DatabaseMigrationServiceConnectionProfile#require_ssl}
        '''
        value = DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig(
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
    ) -> DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigOutputReference:
        return typing.cast(DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigOutputReference, jsii.get(self, "ipConfig"))

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
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig], jsii.get(self, "ipConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__970fed04a83a816553b833fe7c398d2090def6d9b0581b3b876f90e8dbd29fdf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b5c1d5d42a6e8c298531e299e07a5983c4dbdd5b33df44605409bd794e9e6e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoStorageIncrease", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cmekKeyName")
    def cmek_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cmekKeyName"))

    @cmek_key_name.setter
    def cmek_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b54f02d873cfba6fa7586409487ecfbc8af0a0b152f1ec0ea898507fd61349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cmekKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collation")
    def collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collation"))

    @collation.setter
    def collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbca98d70091826718edf72a7c4968a4d04daaa73add28ce25c77efc8ed7118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseFlags")
    def database_flags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "databaseFlags"))

    @database_flags.setter
    def database_flags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11666d1d48ee06a6dcc96d6105e0c4ef3c860f808dd69e5c1deb9fde66e42fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseFlags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseVersion")
    def database_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseVersion"))

    @database_version.setter
    def database_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53150845e1da0f36037c028c3d576e39432f9d8ca24b36a3003d4244f9a8f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDiskSizeGb")
    def data_disk_size_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataDiskSizeGb"))

    @data_disk_size_gb.setter
    def data_disk_size_gb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__977fb2a98edc348c3b46599995bd9aa47e7cdf38afcb9685470089ca7f60ad6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDiskType")
    def data_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataDiskType"))

    @data_disk_type.setter
    def data_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8272c6ac284c052aab6040fcfa3508d4b4eeee7b07bbfddde1078777f88ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ee294a64f1805f532062387f287c3ac36a2fc746ff082335211cd598c92d5c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootPassword")
    def root_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootPassword"))

    @root_password.setter
    def root_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbef4023c5142d194206c939ed3b162d158dd5079b0c9679b506a48eb826258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceId")
    def source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceId"))

    @source_id.setter
    def source_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d1f9d6f355ab6cd54ab2fedeab52274c97d2d08ecd9de2585711324e02cbbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAutoResizeLimit")
    def storage_auto_resize_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAutoResizeLimit"))

    @storage_auto_resize_limit.setter
    def storage_auto_resize_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8664c3fdfdf5dbf18d36ca69691a004f11e5c481db003b8a8f513e9fe12de73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAutoResizeLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12a61f1d00d0f05daaeb8188f136ca8e561618b0e152b6187d3b0f6ffbca638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userLabels")
    def user_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "userLabels"))

    @user_labels.setter
    def user_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f39b8241b52994c23d59f1ebfc681016d8ad7c8122a25b799dae9dfc41f3c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa421b32064758de8da1163ae23010c93bf7cf494f988872a6b9de1cd9a3f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsqlSettings]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsqlSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsqlSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6aedd243ea7cc0dfd7ade8573fdec344ad46f427db88f810e65eb7805fd940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileConfig",
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
class DatabaseMigrationServiceConnectionProfileConfig(
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
        alloydb: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileAlloydb, typing.Dict[builtins.str, typing.Any]]] = None,
        cloudsql: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileCloudsql, typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        mysql: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileMysql", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileOracle", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfilePostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connection_profile_id: The ID of the connection profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#connection_profile_id DatabaseMigrationServiceConnectionProfile#connection_profile_id}
        :param alloydb: alloydb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#alloydb DatabaseMigrationServiceConnectionProfile#alloydb}
        :param cloudsql: cloudsql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cloudsql DatabaseMigrationServiceConnectionProfile#cloudsql}
        :param display_name: The connection profile display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#display_name DatabaseMigrationServiceConnectionProfile#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#id DatabaseMigrationServiceConnectionProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The resource labels for connection profile to use to annotate any related underlying resources such as Compute Engine VMs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#labels DatabaseMigrationServiceConnectionProfile#labels}
        :param location: The location where the connection profile should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#location DatabaseMigrationServiceConnectionProfile#location}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#mysql DatabaseMigrationServiceConnectionProfile#mysql}
        :param oracle: oracle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#oracle DatabaseMigrationServiceConnectionProfile#oracle}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#postgresql DatabaseMigrationServiceConnectionProfile#postgresql}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#project DatabaseMigrationServiceConnectionProfile#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#timeouts DatabaseMigrationServiceConnectionProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(alloydb, dict):
            alloydb = DatabaseMigrationServiceConnectionProfileAlloydb(**alloydb)
        if isinstance(cloudsql, dict):
            cloudsql = DatabaseMigrationServiceConnectionProfileCloudsql(**cloudsql)
        if isinstance(mysql, dict):
            mysql = DatabaseMigrationServiceConnectionProfileMysql(**mysql)
        if isinstance(oracle, dict):
            oracle = DatabaseMigrationServiceConnectionProfileOracle(**oracle)
        if isinstance(postgresql, dict):
            postgresql = DatabaseMigrationServiceConnectionProfilePostgresql(**postgresql)
        if isinstance(timeouts, dict):
            timeouts = DatabaseMigrationServiceConnectionProfileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f279f416437eae1710eb8338ebf701074717ef2cd63ff7e68a51970b523df263)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#connection_profile_id DatabaseMigrationServiceConnectionProfile#connection_profile_id}
        '''
        result = self._values.get("connection_profile_id")
        assert result is not None, "Required property 'connection_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alloydb(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydb]:
        '''alloydb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#alloydb DatabaseMigrationServiceConnectionProfile#alloydb}
        '''
        result = self._values.get("alloydb")
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydb], result)

    @builtins.property
    def cloudsql(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsql]:
        '''cloudsql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cloudsql DatabaseMigrationServiceConnectionProfile#cloudsql}
        '''
        result = self._values.get("cloudsql")
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsql], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The connection profile display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#display_name DatabaseMigrationServiceConnectionProfile#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#id DatabaseMigrationServiceConnectionProfile#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#labels DatabaseMigrationServiceConnectionProfile#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location where the connection profile should reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#location DatabaseMigrationServiceConnectionProfile#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mysql(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileMysql"]:
        '''mysql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#mysql DatabaseMigrationServiceConnectionProfile#mysql}
        '''
        result = self._values.get("mysql")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileMysql"], result)

    @builtins.property
    def oracle(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileOracle"]:
        '''oracle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#oracle DatabaseMigrationServiceConnectionProfile#oracle}
        '''
        result = self._values.get("oracle")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileOracle"], result)

    @builtins.property
    def postgresql(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfilePostgresql"]:
        '''postgresql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#postgresql DatabaseMigrationServiceConnectionProfile#postgresql}
        '''
        result = self._values.get("postgresql")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfilePostgresql"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#project DatabaseMigrationServiceConnectionProfile#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#timeouts DatabaseMigrationServiceConnectionProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileError",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatabaseMigrationServiceConnectionProfileError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6478c8771a3120da3dc2ba71ab848aed1f62ed03264a4dd431dea24336feaf7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabaseMigrationServiceConnectionProfileErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__875efba2ea008b0e00413afb3d348e038206c877b7fa92dc06e8adbb1c1b9009)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseMigrationServiceConnectionProfileErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feeaf483b01cd354a8de94382f4008887c8defde33c83ac0cc58008bd3b69c72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ca1c13ea48790440fda649a4af826d303f62fa21ee1cc35df0fc1f3ed99a21e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db40be90347a9dbfaf7019b98e8d261f22b118da70f9f4a0f841a4e7908dce4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DatabaseMigrationServiceConnectionProfileErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c511b9502bad579374bf4210bda925206d454021b9240086f4d7d8b86533bfb)
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
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileError]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__890877914c0eb66d3e1879c2309abaa36df6148be675a1e9cd370ce1b426c0df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileMysql",
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
class DatabaseMigrationServiceConnectionProfileMysql:
    def __init__(
        self,
        *,
        cloud_sql_id: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        ssl: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileMysqlSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_sql_id: If the source is a Cloud SQL database, use this field to provide the Cloud SQL instance ID of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cloud_sql_id DatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        :param host: The IP or hostname of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#host DatabaseMigrationServiceConnectionProfile#host}
        :param password: Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        :param port: The network port of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ssl DatabaseMigrationServiceConnectionProfile#ssl}
        :param username: The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        '''
        if isinstance(ssl, dict):
            ssl = DatabaseMigrationServiceConnectionProfileMysqlSsl(**ssl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce9137e19ac73a211392db89c74a42a11015ff32514dcfb5c92294f9fa80b91)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cloud_sql_id DatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        '''
        result = self._values.get("cloud_sql_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The IP or hostname of the source MySQL database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#host DatabaseMigrationServiceConnectionProfile#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The password for the user that Database Migration Service will be using to connect to the database.
        This field is not returned on request, and the value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The network port of the source MySQL database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssl(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileMysqlSsl"]:
        '''ssl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ssl DatabaseMigrationServiceConnectionProfile#ssl}
        '''
        result = self._values.get("ssl")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileMysqlSsl"], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username that Database Migration Service will use to connect to the database.

        The value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileMysql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileMysqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileMysqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61c0433d0d0c212f86870c75b9877831d877dd2bd710aa65c8acc871cd7b4b08)
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
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ca_certificate DatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_certificate DatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_key DatabaseMigrationServiceConnectionProfile#client_key}
        :param type: The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#type DatabaseMigrationServiceConnectionProfile#type}
        '''
        value = DatabaseMigrationServiceConnectionProfileMysqlSsl(
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
    def ssl(self) -> "DatabaseMigrationServiceConnectionProfileMysqlSslOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileMysqlSslOutputReference", jsii.get(self, "ssl"))

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
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileMysqlSsl"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileMysqlSsl"], jsii.get(self, "sslInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__159a6d1e8a2d1e8cd4d30bb7464f7d2b7ed4a74e2ccb0c6aaeec59fb0b000fd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSqlId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0660661e1757fc5f0243f78e70678cf02049e20de41e738ec7d619f318a0cfec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9b39bd0c5cf2cc0b9ec3a4b4bdfb66b7463fa94405bb0ce2949e994daaaf1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af6c23687fa639b6e7df0e9bb80b749f78ec618e4ba277998548569bb2a9dc2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c74da6541f2b936929f09d6a29b003894cdf8fb5544b7d89ced0b9f6c748e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileMysql]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileMysql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileMysql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f14e6c32c0effde402ba9365e7ae284bb2379515705038958aa38bc7a5603c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileMysqlSsl",
    jsii_struct_bases=[],
    name_mapping={
        "ca_certificate": "caCertificate",
        "client_certificate": "clientCertificate",
        "client_key": "clientKey",
        "type": "type",
    },
)
class DatabaseMigrationServiceConnectionProfileMysqlSsl:
    def __init__(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ca_certificate DatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_certificate DatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_key DatabaseMigrationServiceConnectionProfile#client_key}
        :param type: The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#type DatabaseMigrationServiceConnectionProfile#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b0e23767b80ead2b822df327f7db5ca0c640ba61ee7fb998f763f09f1ac800)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ca_certificate DatabaseMigrationServiceConnectionProfile#ca_certificate}
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server.
        If this field is used then the 'clientKey' field is mandatory

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_certificate DatabaseMigrationServiceConnectionProfile#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate.
        If this field is used then the 'clientCertificate' field is mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_key DatabaseMigrationServiceConnectionProfile#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#type DatabaseMigrationServiceConnectionProfile#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileMysqlSsl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileMysqlSslOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileMysqlSslOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__199672599d0ab53ba7220084919a0973807844f85499b5c55b335cc5e92c8817)
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
            type_hints = typing.get_type_hints(_typecheckingstub__452841198e637f2f2e69a37081dc8c16c2ff1392d1c796fe8d0d137ecb10e568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3555017a7e4d53c2f9d5de3b39cf78b628eb3742e5c29a72dc680d591d1a7e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3346d0756b7bb612af2291648e49ada6c80f696083594708459c3ff9b4813521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570cde8cef11020de972420b234bd6857b6dc88ab7f18d6d038bcf55046f912e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileMysqlSsl]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileMysqlSsl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileMysqlSsl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba043a1d1910f2e669c9755f9a7c2b88105e496652c52e27189bbd9f8eafd71d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileOracle",
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
class DatabaseMigrationServiceConnectionProfileOracle:
    def __init__(
        self,
        *,
        database_service: builtins.str,
        host: builtins.str,
        password: builtins.str,
        port: jsii.Number,
        username: builtins.str,
        forward_ssh_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        private_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
        ssl: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileOracleSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        static_service_ip_connectivity: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_service: Required. Database service for the Oracle connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_service DatabaseMigrationServiceConnectionProfile#database_service}
        :param host: Required. The IP or hostname of the source Oracle database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#host DatabaseMigrationServiceConnectionProfile#host}
        :param password: Required. Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        :param port: Required. The network port of the source Oracle database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        :param username: Required. The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        :param forward_ssh_connectivity: forward_ssh_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#forward_ssh_connectivity DatabaseMigrationServiceConnectionProfile#forward_ssh_connectivity}
        :param private_connectivity: private_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_connectivity DatabaseMigrationServiceConnectionProfile#private_connectivity}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ssl DatabaseMigrationServiceConnectionProfile#ssl}
        :param static_service_ip_connectivity: static_service_ip_connectivity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#static_service_ip_connectivity DatabaseMigrationServiceConnectionProfile#static_service_ip_connectivity}
        '''
        if isinstance(forward_ssh_connectivity, dict):
            forward_ssh_connectivity = DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity(**forward_ssh_connectivity)
        if isinstance(private_connectivity, dict):
            private_connectivity = DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity(**private_connectivity)
        if isinstance(ssl, dict):
            ssl = DatabaseMigrationServiceConnectionProfileOracleSsl(**ssl)
        if isinstance(static_service_ip_connectivity, dict):
            static_service_ip_connectivity = DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity(**static_service_ip_connectivity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c59b7ec8c1b4c03b04b6f1e79e6ad19ad82b7c56ccad27c0f75ef077f93327)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#database_service DatabaseMigrationServiceConnectionProfile#database_service}
        '''
        result = self._values.get("database_service")
        assert result is not None, "Required property 'database_service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Required. The IP or hostname of the source Oracle database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#host DatabaseMigrationServiceConnectionProfile#host}
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Required.

        Input only. The password for the user that Database Migration Service will be using to connect to the database.
        This field is not returned on request, and the value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Required. The network port of the source Oracle database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Required.

        The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def forward_ssh_connectivity(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity"]:
        '''forward_ssh_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#forward_ssh_connectivity DatabaseMigrationServiceConnectionProfile#forward_ssh_connectivity}
        '''
        result = self._values.get("forward_ssh_connectivity")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity"], result)

    @builtins.property
    def private_connectivity(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity"]:
        '''private_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_connectivity DatabaseMigrationServiceConnectionProfile#private_connectivity}
        '''
        result = self._values.get("private_connectivity")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity"], result)

    @builtins.property
    def ssl(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileOracleSsl"]:
        '''ssl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ssl DatabaseMigrationServiceConnectionProfile#ssl}
        '''
        result = self._values.get("ssl")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileOracleSsl"], result)

    @builtins.property
    def static_service_ip_connectivity(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity"]:
        '''static_service_ip_connectivity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#static_service_ip_connectivity DatabaseMigrationServiceConnectionProfile#static_service_ip_connectivity}
        '''
        result = self._values.get("static_service_ip_connectivity")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileOracle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity",
    jsii_struct_bases=[],
    name_mapping={
        "hostname": "hostname",
        "port": "port",
        "username": "username",
        "password": "password",
        "private_key": "privateKey",
    },
)
class DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity:
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
        :param hostname: Required. Hostname for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#hostname DatabaseMigrationServiceConnectionProfile#hostname}
        :param port: Port for the SSH tunnel, default value is 22. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        :param username: Required. Username for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        :param password: Input only. SSH password. Only one of 'password' and 'private_key' can be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        :param private_key: Input only. SSH private key. Only one of 'password' and 'private_key' can be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_key DatabaseMigrationServiceConnectionProfile#private_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442ca9c2ecf73969b3bc55f32b5e5e3528fdbfbf117e3fc79e924b11ad21797a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#hostname DatabaseMigrationServiceConnectionProfile#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Port for the SSH tunnel, default value is 22.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Required. Username for the SSH tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Input only. SSH password. Only one of 'password' and 'private_key' can be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''Input only. SSH private key. Only one of 'password' and 'private_key' can be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_key DatabaseMigrationServiceConnectionProfile#private_key}
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0942f440680959d06087599fc609c159eb72a78ee713ba681ce30c80bad3055d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__042b99e43786dde67b8caaf6176020ea7523479f2839662fb144df7bef4093b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f555771a3e9518d72fe2dedef3ab757f61f692f00347c597e7fabafd003f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608c730504aa1c8f981717c2439ded5a02fe75e034a103c8baf19ab21c878563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2b5cf4fcaf870d9d9891c4a04aa7564b99a486576d617f29b87dc87d4a6442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ee3471464da7746b0ee754207372a9b9d29ea8dc9930eeb2c45ac8f595b86fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b61603fb284846b5fe91a6fe0cacf20baa7b300946df06210c548adc40bb09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DatabaseMigrationServiceConnectionProfileOracleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileOracleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fb176f86345389ec40e571d3d93545b664302073281ae6b939e66aa37e65ed2)
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
        :param hostname: Required. Hostname for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#hostname DatabaseMigrationServiceConnectionProfile#hostname}
        :param port: Port for the SSH tunnel, default value is 22. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        :param username: Required. Username for the SSH tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        :param password: Input only. SSH password. Only one of 'password' and 'private_key' can be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        :param private_key: Input only. SSH private key. Only one of 'password' and 'private_key' can be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_key DatabaseMigrationServiceConnectionProfile#private_key}
        '''
        value = DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity(
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
        :param private_connection: Required. The resource name (URI) of the private connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_connection DatabaseMigrationServiceConnectionProfile#private_connection}
        '''
        value = DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity(
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
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ca_certificate DatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_certificate DatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_key DatabaseMigrationServiceConnectionProfile#client_key}
        '''
        value = DatabaseMigrationServiceConnectionProfileOracleSsl(
            ca_certificate=ca_certificate,
            client_certificate=client_certificate,
            client_key=client_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSsl", [value]))

    @jsii.member(jsii_name="putStaticServiceIpConnectivity")
    def put_static_service_ip_connectivity(self) -> None:
        value = DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity()

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
    ) -> DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivityOutputReference:
        return typing.cast(DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivityOutputReference, jsii.get(self, "forwardSshConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="passwordSet")
    def password_set(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "passwordSet"))

    @builtins.property
    @jsii.member(jsii_name="privateConnectivity")
    def private_connectivity(
        self,
    ) -> "DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivityOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivityOutputReference", jsii.get(self, "privateConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="ssl")
    def ssl(
        self,
    ) -> "DatabaseMigrationServiceConnectionProfileOracleSslOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileOracleSslOutputReference", jsii.get(self, "ssl"))

    @builtins.property
    @jsii.member(jsii_name="staticServiceIpConnectivity")
    def static_service_ip_connectivity(
        self,
    ) -> "DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivityOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivityOutputReference", jsii.get(self, "staticServiceIpConnectivity"))

    @builtins.property
    @jsii.member(jsii_name="databaseServiceInput")
    def database_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardSshConnectivityInput")
    def forward_ssh_connectivity_input(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity], jsii.get(self, "forwardSshConnectivityInput"))

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
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity"], jsii.get(self, "privateConnectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="sslInput")
    def ssl_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileOracleSsl"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileOracleSsl"], jsii.get(self, "sslInput"))

    @builtins.property
    @jsii.member(jsii_name="staticServiceIpConnectivityInput")
    def static_service_ip_connectivity_input(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity"], jsii.get(self, "staticServiceIpConnectivityInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3e7de89f9887aa5224ee51a455e22ee62ea1c6ebc4d83afd301bab9a8a88f4a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a07ed61bbec21c4a6231bb350bc1feaf8ddf145a53608aae2c2959f4b1e334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__210a64be82c43ee0c21d2d803fdbe1aa7376e0d862eea668ae493fc77c8cb0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85b3ab869d15574cffcf7cbcb3c4f7b0ed3686c6d13a9bc6e17007b413d49f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e73620f7f3192c1b88a967fc152d3f329915c789bef9ee0870d9e35ec76eda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileOracle]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileOracle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileOracle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a616774d83dc0ebd4158b332fb8781c7c55572ba4d62df397a770409ca40bd2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity",
    jsii_struct_bases=[],
    name_mapping={"private_connection": "privateConnection"},
)
class DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity:
    def __init__(self, *, private_connection: builtins.str) -> None:
        '''
        :param private_connection: Required. The resource name (URI) of the private connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_connection DatabaseMigrationServiceConnectionProfile#private_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3beda1d89f215d76e397bca5de73a30cd541e260b00d87ffebd7675ecf66e6a)
            check_type(argname="argument private_connection", value=private_connection, expected_type=type_hints["private_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "private_connection": private_connection,
        }

    @builtins.property
    def private_connection(self) -> builtins.str:
        '''Required. The resource name (URI) of the private connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#private_connection DatabaseMigrationServiceConnectionProfile#private_connection}
        '''
        result = self._values.get("private_connection")
        assert result is not None, "Required property 'private_connection' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d958bf1c1a29c60a0c437d7f94e456bfff0bb15018a1355ef21b3c18125117a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5e6a4b7a52dfafa6f63340cbb8ee40f113a1f34fc45ea4a0d8e89ef64a2b289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateConnection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6cd9bff576a537110e4e164ca913fd6158904d87473b29cf663db246b7111c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileOracleSsl",
    jsii_struct_bases=[],
    name_mapping={
        "ca_certificate": "caCertificate",
        "client_certificate": "clientCertificate",
        "client_key": "clientKey",
    },
)
class DatabaseMigrationServiceConnectionProfileOracleSsl:
    def __init__(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ca_certificate DatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_certificate DatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_key DatabaseMigrationServiceConnectionProfile#client_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ed6be7059619905c5a6b321598c031a9de642962deb453bd4a7e04596ee6d5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ca_certificate DatabaseMigrationServiceConnectionProfile#ca_certificate}
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server.
        If this field is used then the 'clientKey' field is mandatory

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_certificate DatabaseMigrationServiceConnectionProfile#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate.
        If this field is used then the 'clientCertificate' field is mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_key DatabaseMigrationServiceConnectionProfile#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileOracleSsl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileOracleSslOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileOracleSslOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44ac183a20aa1fcdfcf54cd95264f5dab11870429908419e10eb8848aaeb2e04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb369cf8ebfda4067ecdfc0436195a65aecb786626074ce4f4a27b75897989c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3a825062edace4aa264fc661c6ba2dcd63151dd3c6e28b5ae07ab1b4bc2a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a268e25b41cf37ed7497bab0a6867fc85ff3078e6d8a9148fbc821fae05bb44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileOracleSsl]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileOracleSsl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileOracleSsl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85cf6601e43db433da45cb60eeb8846e9f23b25d9dd2ad7c2da203a358cd42d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__588f18c072ba8c43c47bb86566993125992d652094fc2d57a91733faa47f9cea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8370a0bd72d39d30d9a1b0e131deb019708a3ba6a0198aabb0e7796810b83bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfilePostgresql",
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
class DatabaseMigrationServiceConnectionProfilePostgresql:
    def __init__(
        self,
        *,
        alloydb_cluster_id: typing.Optional[builtins.str] = None,
        cloud_sql_id: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        ssl: typing.Optional[typing.Union["DatabaseMigrationServiceConnectionProfilePostgresqlSsl", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alloydb_cluster_id: If the connected database is an AlloyDB instance, use this field to provide the AlloyDB cluster ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#alloydb_cluster_id DatabaseMigrationServiceConnectionProfile#alloydb_cluster_id}
        :param cloud_sql_id: If the source is a Cloud SQL database, use this field to provide the Cloud SQL instance ID of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cloud_sql_id DatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        :param host: The IP or hostname of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#host DatabaseMigrationServiceConnectionProfile#host}
        :param password: Input only. The password for the user that Database Migration Service will be using to connect to the database. This field is not returned on request, and the value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        :param port: The network port of the source MySQL database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        :param ssl: ssl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ssl DatabaseMigrationServiceConnectionProfile#ssl}
        :param username: The username that Database Migration Service will use to connect to the database. The value is encrypted when stored in Database Migration Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        '''
        if isinstance(ssl, dict):
            ssl = DatabaseMigrationServiceConnectionProfilePostgresqlSsl(**ssl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82da82088baead12be71f02ebe191bd7d8457b34d804728b6699d7904bdd507)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#alloydb_cluster_id DatabaseMigrationServiceConnectionProfile#alloydb_cluster_id}
        '''
        result = self._values.get("alloydb_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_sql_id(self) -> typing.Optional[builtins.str]:
        '''If the source is a Cloud SQL database, use this field to provide the Cloud SQL instance ID of the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#cloud_sql_id DatabaseMigrationServiceConnectionProfile#cloud_sql_id}
        '''
        result = self._values.get("cloud_sql_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The IP or hostname of the source MySQL database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#host DatabaseMigrationServiceConnectionProfile#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The password for the user that Database Migration Service will be using to connect to the database.
        This field is not returned on request, and the value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#password DatabaseMigrationServiceConnectionProfile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The network port of the source MySQL database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#port DatabaseMigrationServiceConnectionProfile#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssl(
        self,
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfilePostgresqlSsl"]:
        '''ssl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ssl DatabaseMigrationServiceConnectionProfile#ssl}
        '''
        result = self._values.get("ssl")
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfilePostgresqlSsl"], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username that Database Migration Service will use to connect to the database.

        The value is encrypted when stored in Database Migration Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#username DatabaseMigrationServiceConnectionProfile#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfilePostgresql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfilePostgresqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfilePostgresqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16c08ae50dedfb9465dd503861c5f2df566cdbe73f1e1ba3c49a2137802141cc)
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
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ca_certificate DatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_certificate DatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_key DatabaseMigrationServiceConnectionProfile#client_key}
        :param type: The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#type DatabaseMigrationServiceConnectionProfile#type}
        '''
        value = DatabaseMigrationServiceConnectionProfilePostgresqlSsl(
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
    ) -> "DatabaseMigrationServiceConnectionProfilePostgresqlSslOutputReference":
        return typing.cast("DatabaseMigrationServiceConnectionProfilePostgresqlSslOutputReference", jsii.get(self, "ssl"))

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
    ) -> typing.Optional["DatabaseMigrationServiceConnectionProfilePostgresqlSsl"]:
        return typing.cast(typing.Optional["DatabaseMigrationServiceConnectionProfilePostgresqlSsl"], jsii.get(self, "sslInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1b68311104c90d21b3bf88921be1fadc07f5a8a34e9bb6e49b3e6c13385cfec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alloydbClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudSqlId")
    def cloud_sql_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudSqlId"))

    @cloud_sql_id.setter
    def cloud_sql_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fc75eaa5690fcfe8ca7d4175c12aa553cc042979833b75939b31be8777f1cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSqlId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a854d0624c5db0015a17f52aaad55037546d458dad30c1526e1fde4b9237a07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6364750d55c60ef79b4f44a06186e9af931471c83ef8fb3dc6c4a91efad9276d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0636347cb96c0891ed710a4859c58d0fa30b2c7259e35f0331aadf119984b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853bd5578fc54e1d534a378c61758786992b83dcda8cfb4647e00e7c515594c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfilePostgresql]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfilePostgresql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfilePostgresql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205ed8a99f23392bb45c3b6171d53c7ad0493c537108a809b7a9f1a60a4e186a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfilePostgresqlSsl",
    jsii_struct_bases=[],
    name_mapping={
        "ca_certificate": "caCertificate",
        "client_certificate": "clientCertificate",
        "client_key": "clientKey",
        "type": "type",
    },
)
class DatabaseMigrationServiceConnectionProfilePostgresqlSsl:
    def __init__(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ca_certificate: Input only. The x509 PEM-encoded certificate of the CA that signed the source database server's certificate. The replica will use this certificate to verify it's connecting to the right host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ca_certificate DatabaseMigrationServiceConnectionProfile#ca_certificate}
        :param client_certificate: Input only. The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server. If this field is used then the 'clientKey' field is mandatory Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_certificate DatabaseMigrationServiceConnectionProfile#client_certificate}
        :param client_key: Input only. The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate. If this field is used then the 'clientCertificate' field is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_key DatabaseMigrationServiceConnectionProfile#client_key}
        :param type: The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#type DatabaseMigrationServiceConnectionProfile#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98a8a3eadc6599b9afdbbb18f874d638c10c499e63f5115e0336c5a583e0bf8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#ca_certificate DatabaseMigrationServiceConnectionProfile#ca_certificate}
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The x509 PEM-encoded certificate that will be used by the replica to authenticate against the source database server.
        If this field is used then the 'clientKey' field is mandatory

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_certificate DatabaseMigrationServiceConnectionProfile#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''Input only.

        The unencrypted PKCS#1 or PKCS#8 PEM-encoded private key associated with the Client Certificate.
        If this field is used then the 'clientCertificate' field is mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#client_key DatabaseMigrationServiceConnectionProfile#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The current connection profile state. Possible values: ["SERVER_ONLY", "SERVER_CLIENT", "REQUIRED", "NONE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#type DatabaseMigrationServiceConnectionProfile#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfilePostgresqlSsl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfilePostgresqlSslOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfilePostgresqlSslOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c20aaaa01ef930a1be8a447325d9c60f5f95e9011422f80ad624ceb09e96a584)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d39dc445206faf4ed4118e0e50cb91fd487f211d91b9eb664382fcc13137229a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9ab5c347723290b57c229654427f99f977eb12292a16d95be80009a861ee37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c3dab7733bf2e9a8d06c84ee23f053166cebf298a4a3068614ae65e6b4ab12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1706d9cc6f5e5685ecf88cc2d948da85d4d17469af2f627c793cd8447a644e3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatabaseMigrationServiceConnectionProfilePostgresqlSsl]:
        return typing.cast(typing.Optional[DatabaseMigrationServiceConnectionProfilePostgresqlSsl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatabaseMigrationServiceConnectionProfilePostgresqlSsl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6cbf346aea6ffe3eeb53c53288e2cf9d5d1358904fa8e5258a70c4d2d59bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DatabaseMigrationServiceConnectionProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#create DatabaseMigrationServiceConnectionProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#delete DatabaseMigrationServiceConnectionProfile#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#update DatabaseMigrationServiceConnectionProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__858a5f6081dee57bcdb4a291abd95346eae2e4cf12ac9a119b17892d293c46b9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#create DatabaseMigrationServiceConnectionProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#delete DatabaseMigrationServiceConnectionProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/database_migration_service_connection_profile#update DatabaseMigrationServiceConnectionProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMigrationServiceConnectionProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseMigrationServiceConnectionProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.databaseMigrationServiceConnectionProfile.DatabaseMigrationServiceConnectionProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a628a8591ba053a2c21223b58024535ad1ff572fb04296cdb725bae5e635bc57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e937cb40c72fc529211b7ab207ba037966fafbd511f2c73dc020e65cef6acd4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2fbb166842b2a3dcd3c64d2696fdd4e651c605aed1f4b81cd747dc867a1cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f99a612000aa495a4de772eff1e1033c005213b10e270536bfba9893233e409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceConnectionProfileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceConnectionProfileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceConnectionProfileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d0d70048d31b6ca94e404cf4382e507a7fc89cde1868d3230c15e1ac5d8f8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DatabaseMigrationServiceConnectionProfile",
    "DatabaseMigrationServiceConnectionProfileAlloydb",
    "DatabaseMigrationServiceConnectionProfileAlloydbOutputReference",
    "DatabaseMigrationServiceConnectionProfileAlloydbSettings",
    "DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser",
    "DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUserOutputReference",
    "DatabaseMigrationServiceConnectionProfileAlloydbSettingsOutputReference",
    "DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings",
    "DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig",
    "DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfigOutputReference",
    "DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsOutputReference",
    "DatabaseMigrationServiceConnectionProfileCloudsql",
    "DatabaseMigrationServiceConnectionProfileCloudsqlOutputReference",
    "DatabaseMigrationServiceConnectionProfileCloudsqlSettings",
    "DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig",
    "DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks",
    "DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksList",
    "DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworksOutputReference",
    "DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigOutputReference",
    "DatabaseMigrationServiceConnectionProfileCloudsqlSettingsOutputReference",
    "DatabaseMigrationServiceConnectionProfileConfig",
    "DatabaseMigrationServiceConnectionProfileError",
    "DatabaseMigrationServiceConnectionProfileErrorList",
    "DatabaseMigrationServiceConnectionProfileErrorOutputReference",
    "DatabaseMigrationServiceConnectionProfileMysql",
    "DatabaseMigrationServiceConnectionProfileMysqlOutputReference",
    "DatabaseMigrationServiceConnectionProfileMysqlSsl",
    "DatabaseMigrationServiceConnectionProfileMysqlSslOutputReference",
    "DatabaseMigrationServiceConnectionProfileOracle",
    "DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity",
    "DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivityOutputReference",
    "DatabaseMigrationServiceConnectionProfileOracleOutputReference",
    "DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity",
    "DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivityOutputReference",
    "DatabaseMigrationServiceConnectionProfileOracleSsl",
    "DatabaseMigrationServiceConnectionProfileOracleSslOutputReference",
    "DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity",
    "DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivityOutputReference",
    "DatabaseMigrationServiceConnectionProfilePostgresql",
    "DatabaseMigrationServiceConnectionProfilePostgresqlOutputReference",
    "DatabaseMigrationServiceConnectionProfilePostgresqlSsl",
    "DatabaseMigrationServiceConnectionProfilePostgresqlSslOutputReference",
    "DatabaseMigrationServiceConnectionProfileTimeouts",
    "DatabaseMigrationServiceConnectionProfileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ee107f15e32ecc699de7e35d616c41c1e7fdcb58f1898daac32b9b0d99c1bf73(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connection_profile_id: builtins.str,
    alloydb: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileAlloydb, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudsql: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileCloudsql, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    mysql: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileMysql, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileOracle, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfilePostgresql, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__73672f351dc21c85eeb049c9ae0620be7582217a10456f120763895a506a8abc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a578d97fe3b5858f83f3cae36f3a4ef494aefa5925783e0996bc4585dfa4771(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6352c23d13920c1c11aaba4c5c9d4a36bf8ebaa3c6acde4d2629169be7bce417(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2726e3e09a2f0a635915552799171af2cf8b2c377ea06ead36813d55d548d35a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0ad497cfadfaa18b1b8d3c56a3b22599eecf1f8ff7b1f55d903719efc52d40(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f55e6864b9cd7f0ebad2beb46359331d3293785382d393c6724bbf427514791(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dcaa868af6838ad878decd98972e248964261c8494d166dafd5928a7d2a7a90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd16f8bda8488f726e9fc7c00ead05ba41bc82f1d9d90b546e1a9351da831fb(
    *,
    cluster_id: builtins.str,
    settings: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileAlloydbSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc051083d0ee97096bcf9d6b1278e3173aadbeefb63b9c1f61dc6addee117d61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac8ebad5000e0911bc9bb1dec75394e009abdcd9a1cc90a13edd0d79005937a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a0299c4bb190dd8b6a366967a2d444df7398d04e52de16dd09c8a2842428fb(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6c5b37ddc1a7c380741a81b22b47e856570adafda7a04ad2c4919ceef14d34(
    *,
    initial_user: typing.Union[DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser, typing.Dict[builtins.str, typing.Any]],
    vpc_network: builtins.str,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    primary_instance_settings: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef02e658d274cb5543578c8d449d99f9a3b9ad15b19fcb9821ea3834f707354(
    *,
    password: builtins.str,
    user: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c942d5a0ef7e526b2041e61a1472b87819b05936be45652ecc6a0348dbb35eb5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554b6d0062158b29f4be518112b5a7ec42c22b4f20fe5ec0dbc60d17e6b108bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af29ce75b0542dec19dca902859a1bc72d11eca78265fb3b9e0fc4263f4e040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad794a34f40d5cf869466c452869dcb545e570204f56e320384d5d3d22b709c(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsInitialUser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f33fde6d6287c96d0e36b4432771a3014647919f903624d62ec0ab71a2c314(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f289e885dcee0f4408b011a451b5c11af059536a26f076fd4f6fbde1d770fcb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaea7ffa245f3a3842c179422671bd58fe518bd54d0c886a38e8d7ddf0ba0672(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43543b3a81f983aef457789e0b02d941567618e537c23d217713ef937b4a0e7c(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f793181036ad5e5b8b9899c4d2119ee21f5077f40d0be393a9592f3028e921(
    *,
    id: builtins.str,
    machine_config: typing.Union[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig, typing.Dict[builtins.str, typing.Any]],
    database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3dcb69b73e9a031effc6987e8b3866fa4d759834e209068b241abdb1331ec12(
    *,
    cpu_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15aa8e8d19a3e4705f6a457f87401b9c4d163fd038da6e24e7e23a8c9652634f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e3a662fe1cd314aa40e23a70fd1a39193fc1d3b72d46fc8e9b26d38e4ff619(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55aa0f7564d1da9d064f064f5ef3b8b0d7f2cbc92c2612db3c2f7b45fb9e3ded(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettingsMachineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b8a61999350bd1a6b63f35cdfca8de2e7332f2c89d3497565f14aecbd6c1ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f19b14b870c1ea292636ac0ec8c5ce89b906d2d4fb00a5139db78a0380acbd3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9e81a455ea460b0f7e07aece4ed72130979b1fec07ff88c043a256dbeb582f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344099e96b523069c71e53b7a0e9f9a9a55fe8405165287c133bceda239dd4eb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2986a31c0fc40595da1924da70a4bd3e69979d6f0dc6dc76e75765106d3ed568(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileAlloydbSettingsPrimaryInstanceSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad759f28eddfc1bb17ba353bb107bc6a73b090ebd04c40a50c37e98f918f77d(
    *,
    settings: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileCloudsqlSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea41376fde5e4dad5ca38869544e036b2279a6c7cc1302eacb63c34a8ffbe618(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26aa7130715d320c2e4407a3765764801a87927bbd95709b326f10ee938148d4(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00c5c553350151991716290e5cc6b9c4cd25fcb5044d7cafb48e62cb91037ee(
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
    ip_config: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    root_password: typing.Optional[builtins.str] = None,
    storage_auto_resize_limit: typing.Optional[builtins.str] = None,
    tier: typing.Optional[builtins.str] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4bd6c28b1f6823b6646b76015177ef4efaba909befeb8bc65089a652cf0a83(
    *,
    authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enable_ipv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_network: typing.Optional[builtins.str] = None,
    require_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac25165377599e5bc2b8983b18c183b76706e8d8ccc69046c161284e588bc491(
    *,
    value: builtins.str,
    expire_time: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e4beb0404d874a19a9b49ed1791c4814b6cdc2266b9c7438e790e09156301f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b62a7bbd12bc73b339d711c01fbac552e100bf4267c73bbcbfa587fc641b18(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3bb4cdd3f8ec1f65bd5b45f47778e18a99b966596c68bf9caeac6d820eb275(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a48686a35f56fad12647c167a1a5641e945011140ff5931f447992cb7078cea(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f2090f1c8c59897669b97f4b078cdd32989e5a32922f07a3e3ba64d96761cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad05faf7a21b9bf9f8662698e1e12abc69b45e5b60ebfe323b62660d38a05d20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b5dc1be63fdea81d697c5d7a489d0d60af2d5e83292b0a5a39b0323f71f71d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5509a256fe0a2db3a3f9de815df4701ab3b48b52f1c1899410c7dee48dc432e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f7b83d96bc19e05cf54ebe2487c84bf2be2f50d77729e17d4b6315f4f4815f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f565a93f34ea7c963316d8139600bd408c3c4172151da31d003c27bb1baaae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7004bef7bb00b36fa5ed67b9bd62b157d51404eecde628931af11427492066f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c5adc0123c9caf566cbe84df52042333a083d46aad264aaf07d67be1cd4064(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b518b3043a3b166a067c182217151d1cb13b314ed4905ee0284a83716194e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e43d23a0bbc313a3bedcea9dbcf9616ed928cc7d4125caeb02f6b7ec0d8675(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfigAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89da3e518cc18bad3e931f4599de95c5f79e75a6919a1a264b47756b7788b241(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914d1dd537cbebc5d1e199399a085224871ca50938a2dc7549b1b9cff33d845d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27afc680e80faec9b4a62d033b010d52758254c048bf549c906e4abc35dc2fe7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aba16380d523eaf5a716b994b13e1faf482087ea9a88223d84670844a0c9170(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsqlSettingsIpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5432c4ad240d42f35dc3366d4f0194ced4e7703092a24d5f97c60f5574c1a950(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970fed04a83a816553b833fe7c398d2090def6d9b0581b3b876f90e8dbd29fdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5c1d5d42a6e8c298531e299e07a5983c4dbdd5b33df44605409bd794e9e6e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b54f02d873cfba6fa7586409487ecfbc8af0a0b152f1ec0ea898507fd61349(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbca98d70091826718edf72a7c4968a4d04daaa73add28ce25c77efc8ed7118(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11666d1d48ee06a6dcc96d6105e0c4ef3c860f808dd69e5c1deb9fde66e42fd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53150845e1da0f36037c028c3d576e39432f9d8ca24b36a3003d4244f9a8f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977fb2a98edc348c3b46599995bd9aa47e7cdf38afcb9685470089ca7f60ad6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8272c6ac284c052aab6040fcfa3508d4b4eeee7b07bbfddde1078777f88ccd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee294a64f1805f532062387f287c3ac36a2fc746ff082335211cd598c92d5c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbef4023c5142d194206c939ed3b162d158dd5079b0c9679b506a48eb826258(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d1f9d6f355ab6cd54ab2fedeab52274c97d2d08ecd9de2585711324e02cbbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8664c3fdfdf5dbf18d36ca69691a004f11e5c481db003b8a8f513e9fe12de73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12a61f1d00d0f05daaeb8188f136ca8e561618b0e152b6187d3b0f6ffbca638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f39b8241b52994c23d59f1ebfc681016d8ad7c8122a25b799dae9dfc41f3c3e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa421b32064758de8da1163ae23010c93bf7cf494f988872a6b9de1cd9a3f89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6aedd243ea7cc0dfd7ade8573fdec344ad46f427db88f810e65eb7805fd940(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileCloudsqlSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f279f416437eae1710eb8338ebf701074717ef2cd63ff7e68a51970b523df263(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection_profile_id: builtins.str,
    alloydb: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileAlloydb, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudsql: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileCloudsql, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    mysql: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileMysql, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileOracle, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfilePostgresql, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6478c8771a3120da3dc2ba71ab848aed1f62ed03264a4dd431dea24336feaf7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875efba2ea008b0e00413afb3d348e038206c877b7fa92dc06e8adbb1c1b9009(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feeaf483b01cd354a8de94382f4008887c8defde33c83ac0cc58008bd3b69c72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca1c13ea48790440fda649a4af826d303f62fa21ee1cc35df0fc1f3ed99a21e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db40be90347a9dbfaf7019b98e8d261f22b118da70f9f4a0f841a4e7908dce4d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c511b9502bad579374bf4210bda925206d454021b9240086f4d7d8b86533bfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__890877914c0eb66d3e1879c2309abaa36df6148be675a1e9cd370ce1b426c0df(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce9137e19ac73a211392db89c74a42a11015ff32514dcfb5c92294f9fa80b91(
    *,
    cloud_sql_id: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    ssl: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileMysqlSsl, typing.Dict[builtins.str, typing.Any]]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c0433d0d0c212f86870c75b9877831d877dd2bd710aa65c8acc871cd7b4b08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159a6d1e8a2d1e8cd4d30bb7464f7d2b7ed4a74e2ccb0c6aaeec59fb0b000fd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0660661e1757fc5f0243f78e70678cf02049e20de41e738ec7d619f318a0cfec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9b39bd0c5cf2cc0b9ec3a4b4bdfb66b7463fa94405bb0ce2949e994daaaf1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6c23687fa639b6e7df0e9bb80b749f78ec618e4ba277998548569bb2a9dc2f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c74da6541f2b936929f09d6a29b003894cdf8fb5544b7d89ced0b9f6c748e75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f14e6c32c0effde402ba9365e7ae284bb2379515705038958aa38bc7a5603c0(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileMysql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b0e23767b80ead2b822df327f7db5ca0c640ba61ee7fb998f763f09f1ac800(
    *,
    ca_certificate: typing.Optional[builtins.str] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199672599d0ab53ba7220084919a0973807844f85499b5c55b335cc5e92c8817(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452841198e637f2f2e69a37081dc8c16c2ff1392d1c796fe8d0d137ecb10e568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3555017a7e4d53c2f9d5de3b39cf78b628eb3742e5c29a72dc680d591d1a7e55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3346d0756b7bb612af2291648e49ada6c80f696083594708459c3ff9b4813521(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570cde8cef11020de972420b234bd6857b6dc88ab7f18d6d038bcf55046f912e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba043a1d1910f2e669c9755f9a7c2b88105e496652c52e27189bbd9f8eafd71d(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileMysqlSsl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c59b7ec8c1b4c03b04b6f1e79e6ad19ad82b7c56ccad27c0f75ef077f93327(
    *,
    database_service: builtins.str,
    host: builtins.str,
    password: builtins.str,
    port: jsii.Number,
    username: builtins.str,
    forward_ssh_connectivity: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    private_connectivity: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
    ssl: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileOracleSsl, typing.Dict[builtins.str, typing.Any]]] = None,
    static_service_ip_connectivity: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442ca9c2ecf73969b3bc55f32b5e5e3528fdbfbf117e3fc79e924b11ad21797a(
    *,
    hostname: builtins.str,
    port: jsii.Number,
    username: builtins.str,
    password: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0942f440680959d06087599fc609c159eb72a78ee713ba681ce30c80bad3055d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042b99e43786dde67b8caaf6176020ea7523479f2839662fb144df7bef4093b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f555771a3e9518d72fe2dedef3ab757f61f692f00347c597e7fabafd003f40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608c730504aa1c8f981717c2439ded5a02fe75e034a103c8baf19ab21c878563(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2b5cf4fcaf870d9d9891c4a04aa7564b99a486576d617f29b87dc87d4a6442(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee3471464da7746b0ee754207372a9b9d29ea8dc9930eeb2c45ac8f595b86fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b61603fb284846b5fe91a6fe0cacf20baa7b300946df06210c548adc40bb09(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileOracleForwardSshConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb176f86345389ec40e571d3d93545b664302073281ae6b939e66aa37e65ed2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7de89f9887aa5224ee51a455e22ee62ea1c6ebc4d83afd301bab9a8a88f4a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a07ed61bbec21c4a6231bb350bc1feaf8ddf145a53608aae2c2959f4b1e334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210a64be82c43ee0c21d2d803fdbe1aa7376e0d862eea668ae493fc77c8cb0d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85b3ab869d15574cffcf7cbcb3c4f7b0ed3686c6d13a9bc6e17007b413d49f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e73620f7f3192c1b88a967fc152d3f329915c789bef9ee0870d9e35ec76eda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a616774d83dc0ebd4158b332fb8781c7c55572ba4d62df397a770409ca40bd2c(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileOracle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3beda1d89f215d76e397bca5de73a30cd541e260b00d87ffebd7675ecf66e6a(
    *,
    private_connection: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d958bf1c1a29c60a0c437d7f94e456bfff0bb15018a1355ef21b3c18125117a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e6a4b7a52dfafa6f63340cbb8ee40f113a1f34fc45ea4a0d8e89ef64a2b289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6cd9bff576a537110e4e164ca913fd6158904d87473b29cf663db246b7111c2(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileOraclePrivateConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ed6be7059619905c5a6b321598c031a9de642962deb453bd4a7e04596ee6d5(
    *,
    ca_certificate: typing.Optional[builtins.str] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ac183a20aa1fcdfcf54cd95264f5dab11870429908419e10eb8848aaeb2e04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb369cf8ebfda4067ecdfc0436195a65aecb786626074ce4f4a27b75897989c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3a825062edace4aa264fc661c6ba2dcd63151dd3c6e28b5ae07ab1b4bc2a68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a268e25b41cf37ed7497bab0a6867fc85ff3078e6d8a9148fbc821fae05bb44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85cf6601e43db433da45cb60eeb8846e9f23b25d9dd2ad7c2da203a358cd42d(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileOracleSsl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588f18c072ba8c43c47bb86566993125992d652094fc2d57a91733faa47f9cea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8370a0bd72d39d30d9a1b0e131deb019708a3ba6a0198aabb0e7796810b83bf(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfileOracleStaticServiceIpConnectivity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82da82088baead12be71f02ebe191bd7d8457b34d804728b6699d7904bdd507(
    *,
    alloydb_cluster_id: typing.Optional[builtins.str] = None,
    cloud_sql_id: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    ssl: typing.Optional[typing.Union[DatabaseMigrationServiceConnectionProfilePostgresqlSsl, typing.Dict[builtins.str, typing.Any]]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c08ae50dedfb9465dd503861c5f2df566cdbe73f1e1ba3c49a2137802141cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b68311104c90d21b3bf88921be1fadc07f5a8a34e9bb6e49b3e6c13385cfec4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fc75eaa5690fcfe8ca7d4175c12aa553cc042979833b75939b31be8777f1cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a854d0624c5db0015a17f52aaad55037546d458dad30c1526e1fde4b9237a07a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6364750d55c60ef79b4f44a06186e9af931471c83ef8fb3dc6c4a91efad9276d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0636347cb96c0891ed710a4859c58d0fa30b2c7259e35f0331aadf119984b87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853bd5578fc54e1d534a378c61758786992b83dcda8cfb4647e00e7c515594c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205ed8a99f23392bb45c3b6171d53c7ad0493c537108a809b7a9f1a60a4e186a(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfilePostgresql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98a8a3eadc6599b9afdbbb18f874d638c10c499e63f5115e0336c5a583e0bf8(
    *,
    ca_certificate: typing.Optional[builtins.str] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20aaaa01ef930a1be8a447325d9c60f5f95e9011422f80ad624ceb09e96a584(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39dc445206faf4ed4118e0e50cb91fd487f211d91b9eb664382fcc13137229a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9ab5c347723290b57c229654427f99f977eb12292a16d95be80009a861ee37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c3dab7733bf2e9a8d06c84ee23f053166cebf298a4a3068614ae65e6b4ab12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1706d9cc6f5e5685ecf88cc2d948da85d4d17469af2f627c793cd8447a644e3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6cbf346aea6ffe3eeb53c53288e2cf9d5d1358904fa8e5258a70c4d2d59bb5(
    value: typing.Optional[DatabaseMigrationServiceConnectionProfilePostgresqlSsl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__858a5f6081dee57bcdb4a291abd95346eae2e4cf12ac9a119b17892d293c46b9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a628a8591ba053a2c21223b58024535ad1ff572fb04296cdb725bae5e635bc57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e937cb40c72fc529211b7ab207ba037966fafbd511f2c73dc020e65cef6acd4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2fbb166842b2a3dcd3c64d2696fdd4e651c605aed1f4b81cd747dc867a1cc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f99a612000aa495a4de772eff1e1033c005213b10e270536bfba9893233e409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d0d70048d31b6ca94e404cf4382e507a7fc89cde1868d3230c15e1ac5d8f8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseMigrationServiceConnectionProfileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
