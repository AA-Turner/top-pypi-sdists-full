r'''
# `google_sql_database_instance`

Refer to the Terraform Registry for docs: [`google_sql_database_instance`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance).
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


class GoogleSqlDatabaseInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance google_sql_database_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database_version: builtins.str,
        clone: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceClone", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        maintenance_version: typing.Optional[builtins.str] = None,
        master_instance_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        replica_configuration: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceReplicaConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        replica_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_cluster: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceReplicationCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_backup_context: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceRestoreBackupContext", typing.Dict[builtins.str, typing.Any]]] = None,
        root_password: typing.Optional[builtins.str] = None,
        settings: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance google_sql_database_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database_version: The MySQL, PostgreSQL or SQL Server (beta) version to use. Supported values include MYSQL_5_6, MYSQL_5_7, MYSQL_8_0, MYSQL_8_4, POSTGRES_9_6, POSTGRES_10, POSTGRES_11, POSTGRES_12, POSTGRES_13, POSTGRES_14, POSTGRES_15, POSTGRES_16, POSTGRES_17, SQLSERVER_2017_STANDARD, SQLSERVER_2017_ENTERPRISE, SQLSERVER_2017_EXPRESS, SQLSERVER_2017_WEB. Database Version Policies includes an up-to-date reference of supported versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#database_version GoogleSqlDatabaseInstance#database_version}
        :param clone: clone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#clone GoogleSqlDatabaseInstance#clone}
        :param deletion_protection: Used to block Terraform from deleting a SQL Instance. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#deletion_protection GoogleSqlDatabaseInstance#deletion_protection}
        :param encryption_key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#encryption_key_name GoogleSqlDatabaseInstance#encryption_key_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#id GoogleSqlDatabaseInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_type: The type of the instance. The valid values are:- 'SQL_INSTANCE_TYPE_UNSPECIFIED', 'CLOUD_SQL_INSTANCE', 'ON_PREMISES_INSTANCE' and 'READ_REPLICA_INSTANCE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#instance_type GoogleSqlDatabaseInstance#instance_type}
        :param maintenance_version: Maintenance version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#maintenance_version GoogleSqlDatabaseInstance#maintenance_version}
        :param master_instance_name: The name of the instance that will act as the master in the replication setup. Note, this requires the master to have binary_log_enabled set, as well as existing backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#master_instance_name GoogleSqlDatabaseInstance#master_instance_name}
        :param name: The name of the instance. If the name is left blank, Terraform will randomly generate one when the instance is first created. This is done because after a name is used, it cannot be reused for up to one week. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#name GoogleSqlDatabaseInstance#name}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#project GoogleSqlDatabaseInstance#project}
        :param region: The region the instance will sit in. Note, Cloud SQL is not available in all regions. A valid region must be provided to use this resource. If a region is not provided in the resource definition, the provider region will be used instead, but this will be an apply-time error for instances if the provider region is not supported with Cloud SQL. If you choose not to provide the region argument for this resource, make sure you understand this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#region GoogleSqlDatabaseInstance#region}
        :param replica_configuration: replica_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#replica_configuration GoogleSqlDatabaseInstance#replica_configuration}
        :param replica_names: The replicas of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#replica_names GoogleSqlDatabaseInstance#replica_names}
        :param replication_cluster: replication_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#replication_cluster GoogleSqlDatabaseInstance#replication_cluster}
        :param restore_backup_context: restore_backup_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#restore_backup_context GoogleSqlDatabaseInstance#restore_backup_context}
        :param root_password: Initial root password. Required for MS SQL Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#root_password GoogleSqlDatabaseInstance#root_password}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#settings GoogleSqlDatabaseInstance#settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#timeouts GoogleSqlDatabaseInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e899509fad3e295eeec4ad1acf568ea78d89ae489d1bab40609f928e23961cc6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleSqlDatabaseInstanceConfig(
            database_version=database_version,
            clone=clone,
            deletion_protection=deletion_protection,
            encryption_key_name=encryption_key_name,
            id=id,
            instance_type=instance_type,
            maintenance_version=maintenance_version,
            master_instance_name=master_instance_name,
            name=name,
            project=project,
            region=region,
            replica_configuration=replica_configuration,
            replica_names=replica_names,
            replication_cluster=replication_cluster,
            restore_backup_context=restore_backup_context,
            root_password=root_password,
            settings=settings,
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
        '''Generates CDKTF code for importing a GoogleSqlDatabaseInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleSqlDatabaseInstance to import.
        :param import_from_id: The id of the existing GoogleSqlDatabaseInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleSqlDatabaseInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909d35caf3c7f5bc530162938e81191314371cd1bf49c25ebd15664c7d7102f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClone")
    def put_clone(
        self,
        *,
        source_instance_name: builtins.str,
        allocated_ip_range: typing.Optional[builtins.str] = None,
        database_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        point_in_time: typing.Optional[builtins.str] = None,
        preferred_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_instance_name: The name of the instance from which the point in time should be restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#source_instance_name GoogleSqlDatabaseInstance#source_instance_name}
        :param allocated_ip_range: The name of the allocated ip range for the private ip CloudSQL instance. For example: "google-managed-services-default". If set, the cloned instance ip will be created in the allocated range. The range name must comply with `RFC 1035 <https://tools.ietf.org/html/rfc1035>`_. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#allocated_ip_range GoogleSqlDatabaseInstance#allocated_ip_range}
        :param database_names: (SQL Server only, use with point_in_time) clone only the specified databases from the source instance. Clone all databases if empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#database_names GoogleSqlDatabaseInstance#database_names}
        :param point_in_time: The timestamp of the point in time that should be restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#point_in_time GoogleSqlDatabaseInstance#point_in_time}
        :param preferred_zone: (Point-in-time recovery for PostgreSQL only) Clone to an instance in the specified zone. If no zone is specified, clone to the same zone as the source instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#preferred_zone GoogleSqlDatabaseInstance#preferred_zone}
        '''
        value = GoogleSqlDatabaseInstanceClone(
            source_instance_name=source_instance_name,
            allocated_ip_range=allocated_ip_range,
            database_names=database_names,
            point_in_time=point_in_time,
            preferred_zone=preferred_zone,
        )

        return typing.cast(None, jsii.invoke(self, "putClone", [value]))

    @jsii.member(jsii_name="putReplicaConfiguration")
    def put_replica_configuration(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        cascadable_replica: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
        connect_retry_interval: typing.Optional[jsii.Number] = None,
        dump_file_path: typing.Optional[builtins.str] = None,
        failover_target: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        master_heartbeat_period: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        ssl_cipher: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
        verify_server_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param ca_certificate: PEM representation of the trusted CA's x509 certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ca_certificate GoogleSqlDatabaseInstance#ca_certificate}
        :param cascadable_replica: Specifies if a SQL Server replica is a cascadable replica. A cascadable replica is a SQL Server cross region replica that supports replica(s) under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#cascadable_replica GoogleSqlDatabaseInstance#cascadable_replica}
        :param client_certificate: PEM representation of the replica's x509 certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#client_certificate GoogleSqlDatabaseInstance#client_certificate}
        :param client_key: PEM representation of the replica's private key. The corresponding public key in encoded in the client_certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#client_key GoogleSqlDatabaseInstance#client_key}
        :param connect_retry_interval: The number of seconds between connect retries. MySQL's default is 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#connect_retry_interval GoogleSqlDatabaseInstance#connect_retry_interval}
        :param dump_file_path: Path to a SQL file in Google Cloud Storage from which replica instances are created. Format is gs://bucket/filename. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#dump_file_path GoogleSqlDatabaseInstance#dump_file_path}
        :param failover_target: Specifies if the replica is the failover target. If the field is set to true the replica will be designated as a failover replica. If the master instance fails, the replica instance will be promoted as the new master instance. Not supported for Postgres Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#failover_target GoogleSqlDatabaseInstance#failover_target}
        :param master_heartbeat_period: Time in ms between replication heartbeats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#master_heartbeat_period GoogleSqlDatabaseInstance#master_heartbeat_period}
        :param password: Password for the replication connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#password GoogleSqlDatabaseInstance#password}
        :param ssl_cipher: Permissible ciphers for use in SSL encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ssl_cipher GoogleSqlDatabaseInstance#ssl_cipher}
        :param username: Username for replication connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#username GoogleSqlDatabaseInstance#username}
        :param verify_server_certificate: True if the master's common name value is checked during the SSL handshake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#verify_server_certificate GoogleSqlDatabaseInstance#verify_server_certificate}
        '''
        value = GoogleSqlDatabaseInstanceReplicaConfiguration(
            ca_certificate=ca_certificate,
            cascadable_replica=cascadable_replica,
            client_certificate=client_certificate,
            client_key=client_key,
            connect_retry_interval=connect_retry_interval,
            dump_file_path=dump_file_path,
            failover_target=failover_target,
            master_heartbeat_period=master_heartbeat_period,
            password=password,
            ssl_cipher=ssl_cipher,
            username=username,
            verify_server_certificate=verify_server_certificate,
        )

        return typing.cast(None, jsii.invoke(self, "putReplicaConfiguration", [value]))

    @jsii.member(jsii_name="putReplicationCluster")
    def put_replication_cluster(
        self,
        *,
        failover_dr_replica_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param failover_dr_replica_name: If the instance is a primary instance, then this field identifies the disaster recovery (DR) replica. The standard format of this field is "your-project:your-instance". You can also set this field to "your-instance", but cloud SQL backend will convert it to the aforementioned standard format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#failover_dr_replica_name GoogleSqlDatabaseInstance#failover_dr_replica_name}
        '''
        value = GoogleSqlDatabaseInstanceReplicationCluster(
            failover_dr_replica_name=failover_dr_replica_name
        )

        return typing.cast(None, jsii.invoke(self, "putReplicationCluster", [value]))

    @jsii.member(jsii_name="putRestoreBackupContext")
    def put_restore_backup_context(
        self,
        *,
        backup_run_id: jsii.Number,
        instance_id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backup_run_id: The ID of the backup run to restore from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#backup_run_id GoogleSqlDatabaseInstance#backup_run_id}
        :param instance_id: The ID of the instance that the backup was taken from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#instance_id GoogleSqlDatabaseInstance#instance_id}
        :param project: The full project ID of the source instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#project GoogleSqlDatabaseInstance#project}
        '''
        value = GoogleSqlDatabaseInstanceRestoreBackupContext(
            backup_run_id=backup_run_id, instance_id=instance_id, project=project
        )

        return typing.cast(None, jsii.invoke(self, "putRestoreBackupContext", [value]))

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        *,
        tier: builtins.str,
        activation_policy: typing.Optional[builtins.str] = None,
        active_directory_config: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_machine_features: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        availability_type: typing.Optional[builtins.str] = None,
        backup_configuration: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsBackupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        collation: typing.Optional[builtins.str] = None,
        connection_pool_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connector_enforcement: typing.Optional[builtins.str] = None,
        database_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSqlDatabaseInstanceSettingsDatabaseFlags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_cache_config: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsDataCacheConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        data_disk_provisioned_iops: typing.Optional[jsii.Number] = None,
        data_disk_provisioned_throughput: typing.Optional[jsii.Number] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deny_maintenance_period: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_autoresize: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_autoresize_limit: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        enable_dataplex_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_google_ml_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        insights_config: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsInsightsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_configuration: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsIpConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        location_preference: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsLocationPreference", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_window: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        password_validation_policy: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        retain_backups_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sql_server_audit_config: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param tier: The machine type to use. See tiers for more details and supported versions. Postgres supports only shared-core machine types, and custom machine types such as db-custom-2-13312. See the Custom Machine Type Documentation to learn about specifying custom machine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#tier GoogleSqlDatabaseInstance#tier}
        :param activation_policy: This specifies when the instance should be active. Can be either ALWAYS, NEVER or ON_DEMAND. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#activation_policy GoogleSqlDatabaseInstance#activation_policy}
        :param active_directory_config: active_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#active_directory_config GoogleSqlDatabaseInstance#active_directory_config}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#advanced_machine_features GoogleSqlDatabaseInstance#advanced_machine_features}
        :param availability_type: The availability type of the Cloud SQL instance, high availability (REGIONAL) or single zone (ZONAL). For all instances, ensure that settings.backup_configuration.enabled is set to true. For MySQL instances, ensure that settings.backup_configuration.binary_log_enabled is set to true. For Postgres instances, ensure that settings.backup_configuration.point_in_time_recovery_enabled is set to true. Defaults to ZONAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#availability_type GoogleSqlDatabaseInstance#availability_type}
        :param backup_configuration: backup_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#backup_configuration GoogleSqlDatabaseInstance#backup_configuration}
        :param collation: The name of server instance collation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#collation GoogleSqlDatabaseInstance#collation}
        :param connection_pool_config: connection_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#connection_pool_config GoogleSqlDatabaseInstance#connection_pool_config}
        :param connector_enforcement: Enables the enforcement of Cloud SQL Auth Proxy or Cloud SQL connectors for all the connections. If enabled, all the direct connections are rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#connector_enforcement GoogleSqlDatabaseInstance#connector_enforcement}
        :param database_flags: database_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#database_flags GoogleSqlDatabaseInstance#database_flags}
        :param data_cache_config: data_cache_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_cache_config GoogleSqlDatabaseInstance#data_cache_config}
        :param data_disk_provisioned_iops: Provisioned number of I/O operations per second for the data disk. This field is only used for HYPERDISK_BALANCED disk types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_disk_provisioned_iops GoogleSqlDatabaseInstance#data_disk_provisioned_iops}
        :param data_disk_provisioned_throughput: Provisioned throughput measured in MiB per second for the data disk. This field is only used for HYPERDISK_BALANCED disk types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_disk_provisioned_throughput GoogleSqlDatabaseInstance#data_disk_provisioned_throughput}
        :param deletion_protection_enabled: Configuration to protect against accidental instance deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#deletion_protection_enabled GoogleSqlDatabaseInstance#deletion_protection_enabled}
        :param deny_maintenance_period: deny_maintenance_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#deny_maintenance_period GoogleSqlDatabaseInstance#deny_maintenance_period}
        :param disk_autoresize: Enables auto-resizing of the storage size. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_autoresize GoogleSqlDatabaseInstance#disk_autoresize}
        :param disk_autoresize_limit: The maximum size, in GB, to which storage capacity can be automatically increased. The default value is 0, which specifies that there is no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_autoresize_limit GoogleSqlDatabaseInstance#disk_autoresize_limit}
        :param disk_size: The size of data disk, in GB. Size of a running instance cannot be reduced but can be increased. The minimum value is 10GB for PD_SSD, PD_HDD and 20GB for HYPERDISK_BALANCED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_size GoogleSqlDatabaseInstance#disk_size}
        :param disk_type: The type of supported data disk is tier dependent and can be PD_SSD or PD_HDD or HYPERDISK_BALANCED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_type GoogleSqlDatabaseInstance#disk_type}
        :param edition: The edition of the instance, can be ENTERPRISE or ENTERPRISE_PLUS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#edition GoogleSqlDatabaseInstance#edition}
        :param enable_dataplex_integration: Enables Dataplex Integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_dataplex_integration GoogleSqlDatabaseInstance#enable_dataplex_integration}
        :param enable_google_ml_integration: Enables Vertex AI Integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_google_ml_integration GoogleSqlDatabaseInstance#enable_google_ml_integration}
        :param insights_config: insights_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#insights_config GoogleSqlDatabaseInstance#insights_config}
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ip_configuration GoogleSqlDatabaseInstance#ip_configuration}
        :param location_preference: location_preference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#location_preference GoogleSqlDatabaseInstance#location_preference}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#maintenance_window GoogleSqlDatabaseInstance#maintenance_window}
        :param password_validation_policy: password_validation_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#password_validation_policy GoogleSqlDatabaseInstance#password_validation_policy}
        :param pricing_plan: Pricing plan for this instance, can only be PER_USE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#pricing_plan GoogleSqlDatabaseInstance#pricing_plan}
        :param retain_backups_on_delete: When this parameter is set to true, Cloud SQL retains backups of the instance even after the instance is deleted. The ON_DEMAND backup will be retained until customer deletes the backup or the project. The AUTOMATED backup will be retained based on the backups retention setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retain_backups_on_delete GoogleSqlDatabaseInstance#retain_backups_on_delete}
        :param sql_server_audit_config: sql_server_audit_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#sql_server_audit_config GoogleSqlDatabaseInstance#sql_server_audit_config}
        :param time_zone: The time_zone to be used by the database engine (supported only for SQL Server), in SQL Server timezone format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#time_zone GoogleSqlDatabaseInstance#time_zone}
        :param user_labels: A set of key/value user label pairs to assign to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#user_labels GoogleSqlDatabaseInstance#user_labels}
        '''
        value = GoogleSqlDatabaseInstanceSettings(
            tier=tier,
            activation_policy=activation_policy,
            active_directory_config=active_directory_config,
            advanced_machine_features=advanced_machine_features,
            availability_type=availability_type,
            backup_configuration=backup_configuration,
            collation=collation,
            connection_pool_config=connection_pool_config,
            connector_enforcement=connector_enforcement,
            database_flags=database_flags,
            data_cache_config=data_cache_config,
            data_disk_provisioned_iops=data_disk_provisioned_iops,
            data_disk_provisioned_throughput=data_disk_provisioned_throughput,
            deletion_protection_enabled=deletion_protection_enabled,
            deny_maintenance_period=deny_maintenance_period,
            disk_autoresize=disk_autoresize,
            disk_autoresize_limit=disk_autoresize_limit,
            disk_size=disk_size,
            disk_type=disk_type,
            edition=edition,
            enable_dataplex_integration=enable_dataplex_integration,
            enable_google_ml_integration=enable_google_ml_integration,
            insights_config=insights_config,
            ip_configuration=ip_configuration,
            location_preference=location_preference,
            maintenance_window=maintenance_window,
            password_validation_policy=password_validation_policy,
            pricing_plan=pricing_plan,
            retain_backups_on_delete=retain_backups_on_delete,
            sql_server_audit_config=sql_server_audit_config,
            time_zone=time_zone,
            user_labels=user_labels,
        )

        return typing.cast(None, jsii.invoke(self, "putSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#create GoogleSqlDatabaseInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#delete GoogleSqlDatabaseInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#update GoogleSqlDatabaseInstance#update}.
        '''
        value = GoogleSqlDatabaseInstanceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetClone")
    def reset_clone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClone", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetEncryptionKeyName")
    def reset_encryption_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetMaintenanceVersion")
    def reset_maintenance_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceVersion", []))

    @jsii.member(jsii_name="resetMasterInstanceName")
    def reset_master_instance_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterInstanceName", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReplicaConfiguration")
    def reset_replica_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaConfiguration", []))

    @jsii.member(jsii_name="resetReplicaNames")
    def reset_replica_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaNames", []))

    @jsii.member(jsii_name="resetReplicationCluster")
    def reset_replication_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicationCluster", []))

    @jsii.member(jsii_name="resetRestoreBackupContext")
    def reset_restore_backup_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreBackupContext", []))

    @jsii.member(jsii_name="resetRootPassword")
    def reset_root_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootPassword", []))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

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
    @jsii.member(jsii_name="availableMaintenanceVersions")
    def available_maintenance_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availableMaintenanceVersions"))

    @builtins.property
    @jsii.member(jsii_name="clone")
    def clone(self) -> "GoogleSqlDatabaseInstanceCloneOutputReference":
        return typing.cast("GoogleSqlDatabaseInstanceCloneOutputReference", jsii.get(self, "clone"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

    @builtins.property
    @jsii.member(jsii_name="dnsNames")
    def dns_names(self) -> "GoogleSqlDatabaseInstanceDnsNamesList":
        return typing.cast("GoogleSqlDatabaseInstanceDnsNamesList", jsii.get(self, "dnsNames"))

    @builtins.property
    @jsii.member(jsii_name="firstIpAddress")
    def first_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> "GoogleSqlDatabaseInstanceIpAddressList":
        return typing.cast("GoogleSqlDatabaseInstanceIpAddressList", jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="privateIpAddress")
    def private_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="pscServiceAttachmentLink")
    def psc_service_attachment_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscServiceAttachmentLink"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddress")
    def public_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="replicaConfiguration")
    def replica_configuration(
        self,
    ) -> "GoogleSqlDatabaseInstanceReplicaConfigurationOutputReference":
        return typing.cast("GoogleSqlDatabaseInstanceReplicaConfigurationOutputReference", jsii.get(self, "replicaConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="replicationCluster")
    def replication_cluster(
        self,
    ) -> "GoogleSqlDatabaseInstanceReplicationClusterOutputReference":
        return typing.cast("GoogleSqlDatabaseInstanceReplicationClusterOutputReference", jsii.get(self, "replicationCluster"))

    @builtins.property
    @jsii.member(jsii_name="restoreBackupContext")
    def restore_backup_context(
        self,
    ) -> "GoogleSqlDatabaseInstanceRestoreBackupContextOutputReference":
        return typing.cast("GoogleSqlDatabaseInstanceRestoreBackupContextOutputReference", jsii.get(self, "restoreBackupContext"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="serverCaCert")
    def server_ca_cert(self) -> "GoogleSqlDatabaseInstanceServerCaCertList":
        return typing.cast("GoogleSqlDatabaseInstanceServerCaCertList", jsii.get(self, "serverCaCert"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailAddress")
    def service_account_email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmailAddress"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "GoogleSqlDatabaseInstanceSettingsOutputReference":
        return typing.cast("GoogleSqlDatabaseInstanceSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleSqlDatabaseInstanceTimeoutsOutputReference":
        return typing.cast("GoogleSqlDatabaseInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cloneInput")
    def clone_input(self) -> typing.Optional["GoogleSqlDatabaseInstanceClone"]:
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceClone"], jsii.get(self, "cloneInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseVersionInput")
    def database_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyNameInput")
    def encryption_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceVersionInput")
    def maintenance_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="masterInstanceNameInput")
    def master_instance_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterInstanceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaConfigurationInput")
    def replica_configuration_input(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceReplicaConfiguration"]:
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceReplicaConfiguration"], jsii.get(self, "replicaConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaNamesInput")
    def replica_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "replicaNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationClusterInput")
    def replication_cluster_input(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceReplicationCluster"]:
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceReplicationCluster"], jsii.get(self, "replicationClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreBackupContextInput")
    def restore_backup_context_input(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceRestoreBackupContext"]:
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceRestoreBackupContext"], jsii.get(self, "restoreBackupContextInput"))

    @builtins.property
    @jsii.member(jsii_name="rootPasswordInput")
    def root_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(self) -> typing.Optional["GoogleSqlDatabaseInstanceSettings"]:
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettings"], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleSqlDatabaseInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleSqlDatabaseInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseVersion")
    def database_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseVersion"))

    @database_version.setter
    def database_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97bd8841a0bc8b6b2e8b29cb97ea506718041e265fc37db0d22cc791af5e0a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28757ccd2f2286eff3d68b870e91438ab37d2ddab9c67895122733d1ec0d6e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyName")
    def encryption_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKeyName"))

    @encryption_key_name.setter
    def encryption_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b80a8b8f7be7334447d990450a13be5d177ff474baec8eab6154e5ad7c2412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8fc728ef822d600bcaebfe2a91288022efd15efc258ac48ee45aaac9d79b034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471ff664a275100ebd99d4d261a339e0150f410853cf84a09bc3321083b5431d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceVersion")
    def maintenance_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceVersion"))

    @maintenance_version.setter
    def maintenance_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14faa228e8481d5eb6aa751257231da03263565df3d512b095c62d3791bbd65c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterInstanceName")
    def master_instance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterInstanceName"))

    @master_instance_name.setter
    def master_instance_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5a80968b156f251ec2d79c9e57ac68748260fa191b8aa3be7b792c0d9fe863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterInstanceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a896ad0611b13fec4cb579eec09f4273b1adcd9a32f98c4ae0262486198f059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e614cb31201f3d2e9df59789d530720ccb1c46b81a97ad0dbee2247df6c4d1fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335d5c6c5e72095db61523561a486a65032009bf7707b81d56c7f77e5d464993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaNames")
    def replica_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "replicaNames"))

    @replica_names.setter
    def replica_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9223af3fa74e8ebd868c767d76773bb8a41a4b7cd6c489bd52fcd4127b934123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootPassword")
    def root_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootPassword"))

    @root_password.setter
    def root_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d56178431b0659f1608e5c6d5b9414ad48956f427e7eab518b78180a42711d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootPassword", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceClone",
    jsii_struct_bases=[],
    name_mapping={
        "source_instance_name": "sourceInstanceName",
        "allocated_ip_range": "allocatedIpRange",
        "database_names": "databaseNames",
        "point_in_time": "pointInTime",
        "preferred_zone": "preferredZone",
    },
)
class GoogleSqlDatabaseInstanceClone:
    def __init__(
        self,
        *,
        source_instance_name: builtins.str,
        allocated_ip_range: typing.Optional[builtins.str] = None,
        database_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        point_in_time: typing.Optional[builtins.str] = None,
        preferred_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_instance_name: The name of the instance from which the point in time should be restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#source_instance_name GoogleSqlDatabaseInstance#source_instance_name}
        :param allocated_ip_range: The name of the allocated ip range for the private ip CloudSQL instance. For example: "google-managed-services-default". If set, the cloned instance ip will be created in the allocated range. The range name must comply with `RFC 1035 <https://tools.ietf.org/html/rfc1035>`_. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#allocated_ip_range GoogleSqlDatabaseInstance#allocated_ip_range}
        :param database_names: (SQL Server only, use with point_in_time) clone only the specified databases from the source instance. Clone all databases if empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#database_names GoogleSqlDatabaseInstance#database_names}
        :param point_in_time: The timestamp of the point in time that should be restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#point_in_time GoogleSqlDatabaseInstance#point_in_time}
        :param preferred_zone: (Point-in-time recovery for PostgreSQL only) Clone to an instance in the specified zone. If no zone is specified, clone to the same zone as the source instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#preferred_zone GoogleSqlDatabaseInstance#preferred_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb72ec89b07468d03692ede1c1993050e50bbfaf82709fe288def5b6c7791b64)
            check_type(argname="argument source_instance_name", value=source_instance_name, expected_type=type_hints["source_instance_name"])
            check_type(argname="argument allocated_ip_range", value=allocated_ip_range, expected_type=type_hints["allocated_ip_range"])
            check_type(argname="argument database_names", value=database_names, expected_type=type_hints["database_names"])
            check_type(argname="argument point_in_time", value=point_in_time, expected_type=type_hints["point_in_time"])
            check_type(argname="argument preferred_zone", value=preferred_zone, expected_type=type_hints["preferred_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_instance_name": source_instance_name,
        }
        if allocated_ip_range is not None:
            self._values["allocated_ip_range"] = allocated_ip_range
        if database_names is not None:
            self._values["database_names"] = database_names
        if point_in_time is not None:
            self._values["point_in_time"] = point_in_time
        if preferred_zone is not None:
            self._values["preferred_zone"] = preferred_zone

    @builtins.property
    def source_instance_name(self) -> builtins.str:
        '''The name of the instance from which the point in time should be restored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#source_instance_name GoogleSqlDatabaseInstance#source_instance_name}
        '''
        result = self._values.get("source_instance_name")
        assert result is not None, "Required property 'source_instance_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allocated_ip_range(self) -> typing.Optional[builtins.str]:
        '''The name of the allocated ip range for the private ip CloudSQL instance.

        For example: "google-managed-services-default". If set, the cloned instance ip will be created in the allocated range. The range name must comply with `RFC 1035 <https://tools.ietf.org/html/rfc1035>`_. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#allocated_ip_range GoogleSqlDatabaseInstance#allocated_ip_range}
        '''
        result = self._values.get("allocated_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(SQL Server only, use with point_in_time) clone only the specified databases from the source instance.

        Clone all databases if empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#database_names GoogleSqlDatabaseInstance#database_names}
        '''
        result = self._values.get("database_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def point_in_time(self) -> typing.Optional[builtins.str]:
        '''The timestamp of the point in time that should be restored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#point_in_time GoogleSqlDatabaseInstance#point_in_time}
        '''
        result = self._values.get("point_in_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_zone(self) -> typing.Optional[builtins.str]:
        '''(Point-in-time recovery for PostgreSQL only) Clone to an instance in the specified zone.

        If no zone is specified, clone to the same zone as the source instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#preferred_zone GoogleSqlDatabaseInstance#preferred_zone}
        '''
        result = self._values.get("preferred_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceClone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceCloneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceCloneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b33408fe8e0e2d8ad8961f57530fa0d4cac2b7b9747a0e85b33bb21e4400135)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllocatedIpRange")
    def reset_allocated_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedIpRange", []))

    @jsii.member(jsii_name="resetDatabaseNames")
    def reset_database_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseNames", []))

    @jsii.member(jsii_name="resetPointInTime")
    def reset_point_in_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPointInTime", []))

    @jsii.member(jsii_name="resetPreferredZone")
    def reset_preferred_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredZone", []))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpRangeInput")
    def allocated_ip_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allocatedIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNamesInput")
    def database_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "databaseNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeInput")
    def point_in_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pointInTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredZoneInput")
    def preferred_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceNameInput")
    def source_instance_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInstanceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpRange")
    def allocated_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allocatedIpRange"))

    @allocated_ip_range.setter
    def allocated_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d832cee65e214efc0da2bfaccc222ffa5eb3128d8e6ccacd7474a01e6c49e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocatedIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseNames")
    def database_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "databaseNames"))

    @database_names.setter
    def database_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f01793f12f7eb7516ac96d9cc7ae439f0798c168ca7755f0d50372cd6a7ade2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pointInTime")
    def point_in_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pointInTime"))

    @point_in_time.setter
    def point_in_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e65a03add023eef2a6be962077b9396539d747b89471e067fbe286fd3b31df5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredZone")
    def preferred_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredZone"))

    @preferred_zone.setter
    def preferred_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62777194aac4f9ff2399f715fda3f42308bd6ccddaea0b6adfb3954fc1c38566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceName")
    def source_instance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceInstanceName"))

    @source_instance_name.setter
    def source_instance_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031eb9fdac094d61e74a9046ebd5a40875f13bdbbe9ede10ce00ac8de2bfa1b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceInstanceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleSqlDatabaseInstanceClone]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceClone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceClone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaba4e8d945af02be17c676a4918be2c198d2d5a900a4c1549a2c81152eb08f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database_version": "databaseVersion",
        "clone": "clone",
        "deletion_protection": "deletionProtection",
        "encryption_key_name": "encryptionKeyName",
        "id": "id",
        "instance_type": "instanceType",
        "maintenance_version": "maintenanceVersion",
        "master_instance_name": "masterInstanceName",
        "name": "name",
        "project": "project",
        "region": "region",
        "replica_configuration": "replicaConfiguration",
        "replica_names": "replicaNames",
        "replication_cluster": "replicationCluster",
        "restore_backup_context": "restoreBackupContext",
        "root_password": "rootPassword",
        "settings": "settings",
        "timeouts": "timeouts",
    },
)
class GoogleSqlDatabaseInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database_version: builtins.str,
        clone: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceClone, typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        maintenance_version: typing.Optional[builtins.str] = None,
        master_instance_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        replica_configuration: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceReplicaConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        replica_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_cluster: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceReplicationCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_backup_context: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceRestoreBackupContext", typing.Dict[builtins.str, typing.Any]]] = None,
        root_password: typing.Optional[builtins.str] = None,
        settings: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database_version: The MySQL, PostgreSQL or SQL Server (beta) version to use. Supported values include MYSQL_5_6, MYSQL_5_7, MYSQL_8_0, MYSQL_8_4, POSTGRES_9_6, POSTGRES_10, POSTGRES_11, POSTGRES_12, POSTGRES_13, POSTGRES_14, POSTGRES_15, POSTGRES_16, POSTGRES_17, SQLSERVER_2017_STANDARD, SQLSERVER_2017_ENTERPRISE, SQLSERVER_2017_EXPRESS, SQLSERVER_2017_WEB. Database Version Policies includes an up-to-date reference of supported versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#database_version GoogleSqlDatabaseInstance#database_version}
        :param clone: clone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#clone GoogleSqlDatabaseInstance#clone}
        :param deletion_protection: Used to block Terraform from deleting a SQL Instance. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#deletion_protection GoogleSqlDatabaseInstance#deletion_protection}
        :param encryption_key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#encryption_key_name GoogleSqlDatabaseInstance#encryption_key_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#id GoogleSqlDatabaseInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_type: The type of the instance. The valid values are:- 'SQL_INSTANCE_TYPE_UNSPECIFIED', 'CLOUD_SQL_INSTANCE', 'ON_PREMISES_INSTANCE' and 'READ_REPLICA_INSTANCE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#instance_type GoogleSqlDatabaseInstance#instance_type}
        :param maintenance_version: Maintenance version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#maintenance_version GoogleSqlDatabaseInstance#maintenance_version}
        :param master_instance_name: The name of the instance that will act as the master in the replication setup. Note, this requires the master to have binary_log_enabled set, as well as existing backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#master_instance_name GoogleSqlDatabaseInstance#master_instance_name}
        :param name: The name of the instance. If the name is left blank, Terraform will randomly generate one when the instance is first created. This is done because after a name is used, it cannot be reused for up to one week. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#name GoogleSqlDatabaseInstance#name}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#project GoogleSqlDatabaseInstance#project}
        :param region: The region the instance will sit in. Note, Cloud SQL is not available in all regions. A valid region must be provided to use this resource. If a region is not provided in the resource definition, the provider region will be used instead, but this will be an apply-time error for instances if the provider region is not supported with Cloud SQL. If you choose not to provide the region argument for this resource, make sure you understand this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#region GoogleSqlDatabaseInstance#region}
        :param replica_configuration: replica_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#replica_configuration GoogleSqlDatabaseInstance#replica_configuration}
        :param replica_names: The replicas of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#replica_names GoogleSqlDatabaseInstance#replica_names}
        :param replication_cluster: replication_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#replication_cluster GoogleSqlDatabaseInstance#replication_cluster}
        :param restore_backup_context: restore_backup_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#restore_backup_context GoogleSqlDatabaseInstance#restore_backup_context}
        :param root_password: Initial root password. Required for MS SQL Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#root_password GoogleSqlDatabaseInstance#root_password}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#settings GoogleSqlDatabaseInstance#settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#timeouts GoogleSqlDatabaseInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(clone, dict):
            clone = GoogleSqlDatabaseInstanceClone(**clone)
        if isinstance(replica_configuration, dict):
            replica_configuration = GoogleSqlDatabaseInstanceReplicaConfiguration(**replica_configuration)
        if isinstance(replication_cluster, dict):
            replication_cluster = GoogleSqlDatabaseInstanceReplicationCluster(**replication_cluster)
        if isinstance(restore_backup_context, dict):
            restore_backup_context = GoogleSqlDatabaseInstanceRestoreBackupContext(**restore_backup_context)
        if isinstance(settings, dict):
            settings = GoogleSqlDatabaseInstanceSettings(**settings)
        if isinstance(timeouts, dict):
            timeouts = GoogleSqlDatabaseInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f600e2ea121d674af9ff825e156fa89bda56ea9dc93cdb40aa28efd921cad84)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database_version", value=database_version, expected_type=type_hints["database_version"])
            check_type(argname="argument clone", value=clone, expected_type=type_hints["clone"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument encryption_key_name", value=encryption_key_name, expected_type=type_hints["encryption_key_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument maintenance_version", value=maintenance_version, expected_type=type_hints["maintenance_version"])
            check_type(argname="argument master_instance_name", value=master_instance_name, expected_type=type_hints["master_instance_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument replica_configuration", value=replica_configuration, expected_type=type_hints["replica_configuration"])
            check_type(argname="argument replica_names", value=replica_names, expected_type=type_hints["replica_names"])
            check_type(argname="argument replication_cluster", value=replication_cluster, expected_type=type_hints["replication_cluster"])
            check_type(argname="argument restore_backup_context", value=restore_backup_context, expected_type=type_hints["restore_backup_context"])
            check_type(argname="argument root_password", value=root_password, expected_type=type_hints["root_password"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_version": database_version,
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
        if clone is not None:
            self._values["clone"] = clone
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if encryption_key_name is not None:
            self._values["encryption_key_name"] = encryption_key_name
        if id is not None:
            self._values["id"] = id
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if maintenance_version is not None:
            self._values["maintenance_version"] = maintenance_version
        if master_instance_name is not None:
            self._values["master_instance_name"] = master_instance_name
        if name is not None:
            self._values["name"] = name
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if replica_configuration is not None:
            self._values["replica_configuration"] = replica_configuration
        if replica_names is not None:
            self._values["replica_names"] = replica_names
        if replication_cluster is not None:
            self._values["replication_cluster"] = replication_cluster
        if restore_backup_context is not None:
            self._values["restore_backup_context"] = restore_backup_context
        if root_password is not None:
            self._values["root_password"] = root_password
        if settings is not None:
            self._values["settings"] = settings
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
    def database_version(self) -> builtins.str:
        '''The MySQL, PostgreSQL or SQL Server (beta) version to use.

        Supported values include MYSQL_5_6, MYSQL_5_7, MYSQL_8_0, MYSQL_8_4, POSTGRES_9_6, POSTGRES_10, POSTGRES_11, POSTGRES_12, POSTGRES_13, POSTGRES_14, POSTGRES_15, POSTGRES_16, POSTGRES_17, SQLSERVER_2017_STANDARD, SQLSERVER_2017_ENTERPRISE, SQLSERVER_2017_EXPRESS, SQLSERVER_2017_WEB. Database Version Policies includes an up-to-date reference of supported versions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#database_version GoogleSqlDatabaseInstance#database_version}
        '''
        result = self._values.get("database_version")
        assert result is not None, "Required property 'database_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def clone(self) -> typing.Optional[GoogleSqlDatabaseInstanceClone]:
        '''clone block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#clone GoogleSqlDatabaseInstance#clone}
        '''
        result = self._values.get("clone")
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceClone], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Used to block Terraform from deleting a SQL Instance. Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#deletion_protection GoogleSqlDatabaseInstance#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#encryption_key_name GoogleSqlDatabaseInstance#encryption_key_name}.'''
        result = self._values.get("encryption_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#id GoogleSqlDatabaseInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The type of the instance. The valid values are:- 'SQL_INSTANCE_TYPE_UNSPECIFIED', 'CLOUD_SQL_INSTANCE', 'ON_PREMISES_INSTANCE' and 'READ_REPLICA_INSTANCE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#instance_type GoogleSqlDatabaseInstance#instance_type}
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_version(self) -> typing.Optional[builtins.str]:
        '''Maintenance version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#maintenance_version GoogleSqlDatabaseInstance#maintenance_version}
        '''
        result = self._values.get("maintenance_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_instance_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance that will act as the master in the replication setup.

        Note, this requires the master to have binary_log_enabled set, as well as existing backups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#master_instance_name GoogleSqlDatabaseInstance#master_instance_name}
        '''
        result = self._values.get("master_instance_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance.

        If the name is left blank, Terraform will randomly generate one when the instance is first created. This is done because after a name is used, it cannot be reused for up to one week.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#name GoogleSqlDatabaseInstance#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#project GoogleSqlDatabaseInstance#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region the instance will sit in.

        Note, Cloud SQL is not available in all regions. A valid region must be provided to use this resource. If a region is not provided in the resource definition, the provider region will be used instead, but this will be an apply-time error for instances if the provider region is not supported with Cloud SQL. If you choose not to provide the region argument for this resource, make sure you understand this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#region GoogleSqlDatabaseInstance#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_configuration(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceReplicaConfiguration"]:
        '''replica_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#replica_configuration GoogleSqlDatabaseInstance#replica_configuration}
        '''
        result = self._values.get("replica_configuration")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceReplicaConfiguration"], result)

    @builtins.property
    def replica_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The replicas of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#replica_names GoogleSqlDatabaseInstance#replica_names}
        '''
        result = self._values.get("replica_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def replication_cluster(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceReplicationCluster"]:
        '''replication_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#replication_cluster GoogleSqlDatabaseInstance#replication_cluster}
        '''
        result = self._values.get("replication_cluster")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceReplicationCluster"], result)

    @builtins.property
    def restore_backup_context(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceRestoreBackupContext"]:
        '''restore_backup_context block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#restore_backup_context GoogleSqlDatabaseInstance#restore_backup_context}
        '''
        result = self._values.get("restore_backup_context")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceRestoreBackupContext"], result)

    @builtins.property
    def root_password(self) -> typing.Optional[builtins.str]:
        '''Initial root password. Required for MS SQL Server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#root_password GoogleSqlDatabaseInstance#root_password}
        '''
        result = self._values.get("root_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def settings(self) -> typing.Optional["GoogleSqlDatabaseInstanceSettings"]:
        '''settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#settings GoogleSqlDatabaseInstance#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettings"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleSqlDatabaseInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#timeouts GoogleSqlDatabaseInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceDnsNames",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleSqlDatabaseInstanceDnsNames:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceDnsNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceDnsNamesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceDnsNamesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__375a444e845915d4b9f185406bd00dd56badb5196c12969a8e480bd5fdafd59b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSqlDatabaseInstanceDnsNamesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2595eb5626312178374dd89745280bbb899d419294c3d2766c0f1ce7326b2b6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSqlDatabaseInstanceDnsNamesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefbbbb642a64afdf7ed72be15d93233cca3cace62d3f747b20375fc21783891)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ea01f53a9aa444d4983f7f19a073f67ec6d8cf74f90abf3e118b001d4f86bc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22a291a74e095fd76abfbd8dbeab0e0ef4dc52c9278836ed89c534d2890ce630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceDnsNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceDnsNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7998ceca82e98aa57e157a01cda9320af207682a966b37d349bd42e1a81f118a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionType"))

    @builtins.property
    @jsii.member(jsii_name="dnsScope")
    def dns_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsScope"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleSqlDatabaseInstanceDnsNames]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceDnsNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceDnsNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487f24a0af6e8e8d0b8bb49fb637dcef8556252a9287a9b83fa5146fe282d68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceIpAddress",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleSqlDatabaseInstanceIpAddress:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceIpAddressList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceIpAddressList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61cee7fdded9fe7eb072a8d29ef7219da9e00152dd6bfd16d40994d476eec0ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSqlDatabaseInstanceIpAddressOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638ef37e7f9581241e7dd933421b4f04751d477faf6fda8602e5d023e65c7abd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSqlDatabaseInstanceIpAddressOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0761a3b49585813a346002907303ba2f3b15ee1ade9b4e047ad0949f52a60efb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9a0c6348da5a8d4a6d7f36e2554e36e727cf71161f519713ce41511e95d6d03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af4a42463b9b8f9f20ee4f86125b13dbbeb602e52ab4cee9e0e30061108f5042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceIpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceIpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6510c9f94aec1e8ea1eca20a0e4fe4401c2aa24b96170d8e2de2ce6cb2301c70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="timeToRetire")
    def time_to_retire(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeToRetire"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleSqlDatabaseInstanceIpAddress]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceIpAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceIpAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc98ee0dd6e252f33037f7a81d3e1409235a494d2c12e16f3ebba73fd63b715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceReplicaConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "ca_certificate": "caCertificate",
        "cascadable_replica": "cascadableReplica",
        "client_certificate": "clientCertificate",
        "client_key": "clientKey",
        "connect_retry_interval": "connectRetryInterval",
        "dump_file_path": "dumpFilePath",
        "failover_target": "failoverTarget",
        "master_heartbeat_period": "masterHeartbeatPeriod",
        "password": "password",
        "ssl_cipher": "sslCipher",
        "username": "username",
        "verify_server_certificate": "verifyServerCertificate",
    },
)
class GoogleSqlDatabaseInstanceReplicaConfiguration:
    def __init__(
        self,
        *,
        ca_certificate: typing.Optional[builtins.str] = None,
        cascadable_replica: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
        connect_retry_interval: typing.Optional[jsii.Number] = None,
        dump_file_path: typing.Optional[builtins.str] = None,
        failover_target: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        master_heartbeat_period: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        ssl_cipher: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
        verify_server_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param ca_certificate: PEM representation of the trusted CA's x509 certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ca_certificate GoogleSqlDatabaseInstance#ca_certificate}
        :param cascadable_replica: Specifies if a SQL Server replica is a cascadable replica. A cascadable replica is a SQL Server cross region replica that supports replica(s) under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#cascadable_replica GoogleSqlDatabaseInstance#cascadable_replica}
        :param client_certificate: PEM representation of the replica's x509 certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#client_certificate GoogleSqlDatabaseInstance#client_certificate}
        :param client_key: PEM representation of the replica's private key. The corresponding public key in encoded in the client_certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#client_key GoogleSqlDatabaseInstance#client_key}
        :param connect_retry_interval: The number of seconds between connect retries. MySQL's default is 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#connect_retry_interval GoogleSqlDatabaseInstance#connect_retry_interval}
        :param dump_file_path: Path to a SQL file in Google Cloud Storage from which replica instances are created. Format is gs://bucket/filename. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#dump_file_path GoogleSqlDatabaseInstance#dump_file_path}
        :param failover_target: Specifies if the replica is the failover target. If the field is set to true the replica will be designated as a failover replica. If the master instance fails, the replica instance will be promoted as the new master instance. Not supported for Postgres Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#failover_target GoogleSqlDatabaseInstance#failover_target}
        :param master_heartbeat_period: Time in ms between replication heartbeats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#master_heartbeat_period GoogleSqlDatabaseInstance#master_heartbeat_period}
        :param password: Password for the replication connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#password GoogleSqlDatabaseInstance#password}
        :param ssl_cipher: Permissible ciphers for use in SSL encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ssl_cipher GoogleSqlDatabaseInstance#ssl_cipher}
        :param username: Username for replication connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#username GoogleSqlDatabaseInstance#username}
        :param verify_server_certificate: True if the master's common name value is checked during the SSL handshake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#verify_server_certificate GoogleSqlDatabaseInstance#verify_server_certificate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00cf683ec0cc9fd1eb613222734d1841c1fafba35a40f62e12144273e09d5a74)
            check_type(argname="argument ca_certificate", value=ca_certificate, expected_type=type_hints["ca_certificate"])
            check_type(argname="argument cascadable_replica", value=cascadable_replica, expected_type=type_hints["cascadable_replica"])
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument client_key", value=client_key, expected_type=type_hints["client_key"])
            check_type(argname="argument connect_retry_interval", value=connect_retry_interval, expected_type=type_hints["connect_retry_interval"])
            check_type(argname="argument dump_file_path", value=dump_file_path, expected_type=type_hints["dump_file_path"])
            check_type(argname="argument failover_target", value=failover_target, expected_type=type_hints["failover_target"])
            check_type(argname="argument master_heartbeat_period", value=master_heartbeat_period, expected_type=type_hints["master_heartbeat_period"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument ssl_cipher", value=ssl_cipher, expected_type=type_hints["ssl_cipher"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument verify_server_certificate", value=verify_server_certificate, expected_type=type_hints["verify_server_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ca_certificate is not None:
            self._values["ca_certificate"] = ca_certificate
        if cascadable_replica is not None:
            self._values["cascadable_replica"] = cascadable_replica
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if client_key is not None:
            self._values["client_key"] = client_key
        if connect_retry_interval is not None:
            self._values["connect_retry_interval"] = connect_retry_interval
        if dump_file_path is not None:
            self._values["dump_file_path"] = dump_file_path
        if failover_target is not None:
            self._values["failover_target"] = failover_target
        if master_heartbeat_period is not None:
            self._values["master_heartbeat_period"] = master_heartbeat_period
        if password is not None:
            self._values["password"] = password
        if ssl_cipher is not None:
            self._values["ssl_cipher"] = ssl_cipher
        if username is not None:
            self._values["username"] = username
        if verify_server_certificate is not None:
            self._values["verify_server_certificate"] = verify_server_certificate

    @builtins.property
    def ca_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM representation of the trusted CA's x509 certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ca_certificate GoogleSqlDatabaseInstance#ca_certificate}
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cascadable_replica(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if a SQL Server replica is a cascadable replica.

        A cascadable replica is a SQL Server cross region replica that supports replica(s) under it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#cascadable_replica GoogleSqlDatabaseInstance#cascadable_replica}
        '''
        result = self._values.get("cascadable_replica")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM representation of the replica's x509 certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#client_certificate GoogleSqlDatabaseInstance#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''PEM representation of the replica's private key. The corresponding public key in encoded in the client_certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#client_key GoogleSqlDatabaseInstance#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect_retry_interval(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds between connect retries. MySQL's default is 60 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#connect_retry_interval GoogleSqlDatabaseInstance#connect_retry_interval}
        '''
        result = self._values.get("connect_retry_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dump_file_path(self) -> typing.Optional[builtins.str]:
        '''Path to a SQL file in Google Cloud Storage from which replica instances are created. Format is gs://bucket/filename.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#dump_file_path GoogleSqlDatabaseInstance#dump_file_path}
        '''
        result = self._values.get("dump_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failover_target(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the replica is the failover target.

        If the field is set to true the replica will be designated as a failover replica. If the master instance fails, the replica instance will be promoted as the new master instance. Not supported for Postgres

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#failover_target GoogleSqlDatabaseInstance#failover_target}
        '''
        result = self._values.get("failover_target")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def master_heartbeat_period(self) -> typing.Optional[jsii.Number]:
        '''Time in ms between replication heartbeats.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#master_heartbeat_period GoogleSqlDatabaseInstance#master_heartbeat_period}
        '''
        result = self._values.get("master_heartbeat_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the replication connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#password GoogleSqlDatabaseInstance#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_cipher(self) -> typing.Optional[builtins.str]:
        '''Permissible ciphers for use in SSL encryption.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ssl_cipher GoogleSqlDatabaseInstance#ssl_cipher}
        '''
        result = self._values.get("ssl_cipher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for replication connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#username GoogleSqlDatabaseInstance#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_server_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the master's common name value is checked during the SSL handshake.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#verify_server_certificate GoogleSqlDatabaseInstance#verify_server_certificate}
        '''
        result = self._values.get("verify_server_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceReplicaConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceReplicaConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceReplicaConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8f4fcfba219bc4a57271bec2b318a8102bd9dc0fb076a618bb8fafa9e233580)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCaCertificate")
    def reset_ca_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCertificate", []))

    @jsii.member(jsii_name="resetCascadableReplica")
    def reset_cascadable_replica(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCascadableReplica", []))

    @jsii.member(jsii_name="resetClientCertificate")
    def reset_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificate", []))

    @jsii.member(jsii_name="resetClientKey")
    def reset_client_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientKey", []))

    @jsii.member(jsii_name="resetConnectRetryInterval")
    def reset_connect_retry_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectRetryInterval", []))

    @jsii.member(jsii_name="resetDumpFilePath")
    def reset_dump_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDumpFilePath", []))

    @jsii.member(jsii_name="resetFailoverTarget")
    def reset_failover_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverTarget", []))

    @jsii.member(jsii_name="resetMasterHeartbeatPeriod")
    def reset_master_heartbeat_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterHeartbeatPeriod", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetSslCipher")
    def reset_ssl_cipher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslCipher", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetVerifyServerCertificate")
    def reset_verify_server_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyServerCertificate", []))

    @builtins.property
    @jsii.member(jsii_name="caCertificateInput")
    def ca_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="cascadableReplicaInput")
    def cascadable_replica_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cascadableReplicaInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateInput")
    def client_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="clientKeyInput")
    def client_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="connectRetryIntervalInput")
    def connect_retry_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectRetryIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="dumpFilePathInput")
    def dump_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dumpFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverTargetInput")
    def failover_target_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failoverTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="masterHeartbeatPeriodInput")
    def master_heartbeat_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "masterHeartbeatPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="sslCipherInput")
    def ssl_cipher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslCipherInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyServerCertificateInput")
    def verify_server_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyServerCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertificate")
    def ca_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertificate"))

    @ca_certificate.setter
    def ca_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652faf9a0725c40d7f66e8a8567742861de568c57c5c4d4815808a697c025392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cascadableReplica")
    def cascadable_replica(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cascadableReplica"))

    @cascadable_replica.setter
    def cascadable_replica(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2ccba4e603444ce457a24b245aef6057c8969727aec3aaf6ee46e433427758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cascadableReplica", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d858133e5dfe2d6f272c9b0667467054cf7cc80479635d0f24110b1d0ccc0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712cd2ca69324f881306e76482e97a907b9b2cdd27846465afb9a6d849677bce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectRetryInterval")
    def connect_retry_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectRetryInterval"))

    @connect_retry_interval.setter
    def connect_retry_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c7774f4d381364f81647166e8022017735e110b74dc106ab966086516b7ccc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectRetryInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dumpFilePath")
    def dump_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dumpFilePath"))

    @dump_file_path.setter
    def dump_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b50fc9b94bbe45b2d7fd250d2bbef151db43a4aad8455ffaf129dcb308c842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dumpFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failoverTarget")
    def failover_target(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failoverTarget"))

    @failover_target.setter
    def failover_target(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0580952aee12a18509ce18cff482e23ae9874b382d57ebfc5f3e9c8b4fb3bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterHeartbeatPeriod")
    def master_heartbeat_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "masterHeartbeatPeriod"))

    @master_heartbeat_period.setter
    def master_heartbeat_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5229e54f30a31f2c8f1b7f3dc575ab0fff76916efe1ed11ca8097686de4e9ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterHeartbeatPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75da1a53cb6fed6670250f654aebb52a14add73e3c485bd559d25d38f8517fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCipher")
    def ssl_cipher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCipher"))

    @ssl_cipher.setter
    def ssl_cipher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded03b3733a73db0e22733ed4a499c92f034f3a28c19be5dd8e155347bed33d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCipher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60720d1c89ea82896a2adccd26d66ef1a5439e7af6c13487e9cca90fd1e600b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verifyServerCertificate")
    def verify_server_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyServerCertificate"))

    @verify_server_certificate.setter
    def verify_server_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99593ce61863f5496755bc5ef88624a6009506371845d7297d8a4cd5e42575d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyServerCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceReplicaConfiguration]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceReplicaConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceReplicaConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61386cfaeba901b7384924d5526548c4ccba3450ad5802f3e94747571d078d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceReplicationCluster",
    jsii_struct_bases=[],
    name_mapping={"failover_dr_replica_name": "failoverDrReplicaName"},
)
class GoogleSqlDatabaseInstanceReplicationCluster:
    def __init__(
        self,
        *,
        failover_dr_replica_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param failover_dr_replica_name: If the instance is a primary instance, then this field identifies the disaster recovery (DR) replica. The standard format of this field is "your-project:your-instance". You can also set this field to "your-instance", but cloud SQL backend will convert it to the aforementioned standard format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#failover_dr_replica_name GoogleSqlDatabaseInstance#failover_dr_replica_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9cd3cf7941f5f730a934d6937d50c0ee0909e21479a414d0d74ee37da8e78a9)
            check_type(argname="argument failover_dr_replica_name", value=failover_dr_replica_name, expected_type=type_hints["failover_dr_replica_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failover_dr_replica_name is not None:
            self._values["failover_dr_replica_name"] = failover_dr_replica_name

    @builtins.property
    def failover_dr_replica_name(self) -> typing.Optional[builtins.str]:
        '''If the instance is a primary instance, then this field identifies the disaster recovery (DR) replica.

        The standard format of this field is "your-project:your-instance". You can also set this field to "your-instance", but cloud SQL backend will convert it to the aforementioned standard format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#failover_dr_replica_name GoogleSqlDatabaseInstance#failover_dr_replica_name}
        '''
        result = self._values.get("failover_dr_replica_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceReplicationCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceReplicationClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceReplicationClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81273dcaf390870f876ba77da06915e73ce49475bd69f290a0f6358a04b0a3cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFailoverDrReplicaName")
    def reset_failover_dr_replica_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverDrReplicaName", []))

    @builtins.property
    @jsii.member(jsii_name="drReplica")
    def dr_replica(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "drReplica"))

    @builtins.property
    @jsii.member(jsii_name="failoverDrReplicaNameInput")
    def failover_dr_replica_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failoverDrReplicaNameInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverDrReplicaName")
    def failover_dr_replica_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failoverDrReplicaName"))

    @failover_dr_replica_name.setter
    def failover_dr_replica_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7832e32e08b45f439a84c96d67f52d314d9a2e95e62f6996bb8b297bff30d99b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverDrReplicaName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceReplicationCluster]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceReplicationCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceReplicationCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d803b8f6817c45b4e141ed870f1fbbf904fe857341cbed8edf20d56df00ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceRestoreBackupContext",
    jsii_struct_bases=[],
    name_mapping={
        "backup_run_id": "backupRunId",
        "instance_id": "instanceId",
        "project": "project",
    },
)
class GoogleSqlDatabaseInstanceRestoreBackupContext:
    def __init__(
        self,
        *,
        backup_run_id: jsii.Number,
        instance_id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backup_run_id: The ID of the backup run to restore from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#backup_run_id GoogleSqlDatabaseInstance#backup_run_id}
        :param instance_id: The ID of the instance that the backup was taken from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#instance_id GoogleSqlDatabaseInstance#instance_id}
        :param project: The full project ID of the source instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#project GoogleSqlDatabaseInstance#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4415f533fac97d43e41c278370c8d97fde579904fe0ce0d62adf173cdb6760)
            check_type(argname="argument backup_run_id", value=backup_run_id, expected_type=type_hints["backup_run_id"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_run_id": backup_run_id,
        }
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if project is not None:
            self._values["project"] = project

    @builtins.property
    def backup_run_id(self) -> jsii.Number:
        '''The ID of the backup run to restore from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#backup_run_id GoogleSqlDatabaseInstance#backup_run_id}
        '''
        result = self._values.get("backup_run_id")
        assert result is not None, "Required property 'backup_run_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the instance that the backup was taken from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#instance_id GoogleSqlDatabaseInstance#instance_id}
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The full project ID of the source instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#project GoogleSqlDatabaseInstance#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceRestoreBackupContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceRestoreBackupContextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceRestoreBackupContextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f86bafdd5deb24853efdb7a46332815da3997f33f783a46bbae0dba712b8d24d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceId")
    def reset_instance_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @builtins.property
    @jsii.member(jsii_name="backupRunIdInput")
    def backup_run_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupRunIdInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRunId")
    def backup_run_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupRunId"))

    @backup_run_id.setter
    def backup_run_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328d9689814fabf14c7485508171c769d62468417a40c8b30380b2cfee466c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRunId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310e2651cb673b2fa20eb7e6796d204c088b7d6bf64a446536ae4c72f24f140e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cd6cf15cf331614453701cccf9fb2e4f12ebea5f706b9288afcafbde16919d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceRestoreBackupContext]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceRestoreBackupContext], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceRestoreBackupContext],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11aa1cbccbe4ba0812d24514741132ed37c754c1e272b9ee7288e55b2c6c5938)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceServerCaCert",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleSqlDatabaseInstanceServerCaCert:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceServerCaCert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceServerCaCertList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceServerCaCertList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__793f5cf10da62da577f99a7dbf2c486699ad7297099d9360dc45e397ee4a19fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSqlDatabaseInstanceServerCaCertOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6650da84959af8d630b1b12fd217e9545a26f411c004724fcf0328c0a87f4fc7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSqlDatabaseInstanceServerCaCertOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd48a8664af1e4bb36c5e3e2b410f8a0b0737bb33d4eadddc90b76e50d31093)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05d11b0110f3fb7edf7d39226b5dec88b16f1ae7c2899761c782d79dd2909c16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__470c31e5981df7f9df99235224d56dbe349ac736a94f36d41fc315119d4baa4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceServerCaCertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceServerCaCertOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1bcd201b5d733b6580216a37911ce7637f43b4f7b16cab6a189f02163228aff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cert"))

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonName"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="expirationTime")
    def expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationTime"))

    @builtins.property
    @jsii.member(jsii_name="sha1Fingerprint")
    def sha1_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha1Fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleSqlDatabaseInstanceServerCaCert]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceServerCaCert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceServerCaCert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec6e7d267c5c9bd1bc1db2fade2aa194e83464647b10033a417a402c9e4af4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettings",
    jsii_struct_bases=[],
    name_mapping={
        "tier": "tier",
        "activation_policy": "activationPolicy",
        "active_directory_config": "activeDirectoryConfig",
        "advanced_machine_features": "advancedMachineFeatures",
        "availability_type": "availabilityType",
        "backup_configuration": "backupConfiguration",
        "collation": "collation",
        "connection_pool_config": "connectionPoolConfig",
        "connector_enforcement": "connectorEnforcement",
        "database_flags": "databaseFlags",
        "data_cache_config": "dataCacheConfig",
        "data_disk_provisioned_iops": "dataDiskProvisionedIops",
        "data_disk_provisioned_throughput": "dataDiskProvisionedThroughput",
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "deny_maintenance_period": "denyMaintenancePeriod",
        "disk_autoresize": "diskAutoresize",
        "disk_autoresize_limit": "diskAutoresizeLimit",
        "disk_size": "diskSize",
        "disk_type": "diskType",
        "edition": "edition",
        "enable_dataplex_integration": "enableDataplexIntegration",
        "enable_google_ml_integration": "enableGoogleMlIntegration",
        "insights_config": "insightsConfig",
        "ip_configuration": "ipConfiguration",
        "location_preference": "locationPreference",
        "maintenance_window": "maintenanceWindow",
        "password_validation_policy": "passwordValidationPolicy",
        "pricing_plan": "pricingPlan",
        "retain_backups_on_delete": "retainBackupsOnDelete",
        "sql_server_audit_config": "sqlServerAuditConfig",
        "time_zone": "timeZone",
        "user_labels": "userLabels",
    },
)
class GoogleSqlDatabaseInstanceSettings:
    def __init__(
        self,
        *,
        tier: builtins.str,
        activation_policy: typing.Optional[builtins.str] = None,
        active_directory_config: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_machine_features: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        availability_type: typing.Optional[builtins.str] = None,
        backup_configuration: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsBackupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        collation: typing.Optional[builtins.str] = None,
        connection_pool_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connector_enforcement: typing.Optional[builtins.str] = None,
        database_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSqlDatabaseInstanceSettingsDatabaseFlags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_cache_config: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsDataCacheConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        data_disk_provisioned_iops: typing.Optional[jsii.Number] = None,
        data_disk_provisioned_throughput: typing.Optional[jsii.Number] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deny_maintenance_period: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_autoresize: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_autoresize_limit: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        enable_dataplex_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_google_ml_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        insights_config: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsInsightsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_configuration: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsIpConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        location_preference: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsLocationPreference", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_window: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        password_validation_policy: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        retain_backups_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sql_server_audit_config: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param tier: The machine type to use. See tiers for more details and supported versions. Postgres supports only shared-core machine types, and custom machine types such as db-custom-2-13312. See the Custom Machine Type Documentation to learn about specifying custom machine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#tier GoogleSqlDatabaseInstance#tier}
        :param activation_policy: This specifies when the instance should be active. Can be either ALWAYS, NEVER or ON_DEMAND. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#activation_policy GoogleSqlDatabaseInstance#activation_policy}
        :param active_directory_config: active_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#active_directory_config GoogleSqlDatabaseInstance#active_directory_config}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#advanced_machine_features GoogleSqlDatabaseInstance#advanced_machine_features}
        :param availability_type: The availability type of the Cloud SQL instance, high availability (REGIONAL) or single zone (ZONAL). For all instances, ensure that settings.backup_configuration.enabled is set to true. For MySQL instances, ensure that settings.backup_configuration.binary_log_enabled is set to true. For Postgres instances, ensure that settings.backup_configuration.point_in_time_recovery_enabled is set to true. Defaults to ZONAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#availability_type GoogleSqlDatabaseInstance#availability_type}
        :param backup_configuration: backup_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#backup_configuration GoogleSqlDatabaseInstance#backup_configuration}
        :param collation: The name of server instance collation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#collation GoogleSqlDatabaseInstance#collation}
        :param connection_pool_config: connection_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#connection_pool_config GoogleSqlDatabaseInstance#connection_pool_config}
        :param connector_enforcement: Enables the enforcement of Cloud SQL Auth Proxy or Cloud SQL connectors for all the connections. If enabled, all the direct connections are rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#connector_enforcement GoogleSqlDatabaseInstance#connector_enforcement}
        :param database_flags: database_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#database_flags GoogleSqlDatabaseInstance#database_flags}
        :param data_cache_config: data_cache_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_cache_config GoogleSqlDatabaseInstance#data_cache_config}
        :param data_disk_provisioned_iops: Provisioned number of I/O operations per second for the data disk. This field is only used for HYPERDISK_BALANCED disk types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_disk_provisioned_iops GoogleSqlDatabaseInstance#data_disk_provisioned_iops}
        :param data_disk_provisioned_throughput: Provisioned throughput measured in MiB per second for the data disk. This field is only used for HYPERDISK_BALANCED disk types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_disk_provisioned_throughput GoogleSqlDatabaseInstance#data_disk_provisioned_throughput}
        :param deletion_protection_enabled: Configuration to protect against accidental instance deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#deletion_protection_enabled GoogleSqlDatabaseInstance#deletion_protection_enabled}
        :param deny_maintenance_period: deny_maintenance_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#deny_maintenance_period GoogleSqlDatabaseInstance#deny_maintenance_period}
        :param disk_autoresize: Enables auto-resizing of the storage size. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_autoresize GoogleSqlDatabaseInstance#disk_autoresize}
        :param disk_autoresize_limit: The maximum size, in GB, to which storage capacity can be automatically increased. The default value is 0, which specifies that there is no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_autoresize_limit GoogleSqlDatabaseInstance#disk_autoresize_limit}
        :param disk_size: The size of data disk, in GB. Size of a running instance cannot be reduced but can be increased. The minimum value is 10GB for PD_SSD, PD_HDD and 20GB for HYPERDISK_BALANCED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_size GoogleSqlDatabaseInstance#disk_size}
        :param disk_type: The type of supported data disk is tier dependent and can be PD_SSD or PD_HDD or HYPERDISK_BALANCED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_type GoogleSqlDatabaseInstance#disk_type}
        :param edition: The edition of the instance, can be ENTERPRISE or ENTERPRISE_PLUS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#edition GoogleSqlDatabaseInstance#edition}
        :param enable_dataplex_integration: Enables Dataplex Integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_dataplex_integration GoogleSqlDatabaseInstance#enable_dataplex_integration}
        :param enable_google_ml_integration: Enables Vertex AI Integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_google_ml_integration GoogleSqlDatabaseInstance#enable_google_ml_integration}
        :param insights_config: insights_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#insights_config GoogleSqlDatabaseInstance#insights_config}
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ip_configuration GoogleSqlDatabaseInstance#ip_configuration}
        :param location_preference: location_preference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#location_preference GoogleSqlDatabaseInstance#location_preference}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#maintenance_window GoogleSqlDatabaseInstance#maintenance_window}
        :param password_validation_policy: password_validation_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#password_validation_policy GoogleSqlDatabaseInstance#password_validation_policy}
        :param pricing_plan: Pricing plan for this instance, can only be PER_USE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#pricing_plan GoogleSqlDatabaseInstance#pricing_plan}
        :param retain_backups_on_delete: When this parameter is set to true, Cloud SQL retains backups of the instance even after the instance is deleted. The ON_DEMAND backup will be retained until customer deletes the backup or the project. The AUTOMATED backup will be retained based on the backups retention setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retain_backups_on_delete GoogleSqlDatabaseInstance#retain_backups_on_delete}
        :param sql_server_audit_config: sql_server_audit_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#sql_server_audit_config GoogleSqlDatabaseInstance#sql_server_audit_config}
        :param time_zone: The time_zone to be used by the database engine (supported only for SQL Server), in SQL Server timezone format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#time_zone GoogleSqlDatabaseInstance#time_zone}
        :param user_labels: A set of key/value user label pairs to assign to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#user_labels GoogleSqlDatabaseInstance#user_labels}
        '''
        if isinstance(active_directory_config, dict):
            active_directory_config = GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig(**active_directory_config)
        if isinstance(advanced_machine_features, dict):
            advanced_machine_features = GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures(**advanced_machine_features)
        if isinstance(backup_configuration, dict):
            backup_configuration = GoogleSqlDatabaseInstanceSettingsBackupConfiguration(**backup_configuration)
        if isinstance(data_cache_config, dict):
            data_cache_config = GoogleSqlDatabaseInstanceSettingsDataCacheConfig(**data_cache_config)
        if isinstance(deny_maintenance_period, dict):
            deny_maintenance_period = GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod(**deny_maintenance_period)
        if isinstance(insights_config, dict):
            insights_config = GoogleSqlDatabaseInstanceSettingsInsightsConfig(**insights_config)
        if isinstance(ip_configuration, dict):
            ip_configuration = GoogleSqlDatabaseInstanceSettingsIpConfiguration(**ip_configuration)
        if isinstance(location_preference, dict):
            location_preference = GoogleSqlDatabaseInstanceSettingsLocationPreference(**location_preference)
        if isinstance(maintenance_window, dict):
            maintenance_window = GoogleSqlDatabaseInstanceSettingsMaintenanceWindow(**maintenance_window)
        if isinstance(password_validation_policy, dict):
            password_validation_policy = GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy(**password_validation_policy)
        if isinstance(sql_server_audit_config, dict):
            sql_server_audit_config = GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig(**sql_server_audit_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe9a873e6c71d473adccc7b6681aae1a8ebb21b4d767b2ed57831f9c181ae3d)
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument activation_policy", value=activation_policy, expected_type=type_hints["activation_policy"])
            check_type(argname="argument active_directory_config", value=active_directory_config, expected_type=type_hints["active_directory_config"])
            check_type(argname="argument advanced_machine_features", value=advanced_machine_features, expected_type=type_hints["advanced_machine_features"])
            check_type(argname="argument availability_type", value=availability_type, expected_type=type_hints["availability_type"])
            check_type(argname="argument backup_configuration", value=backup_configuration, expected_type=type_hints["backup_configuration"])
            check_type(argname="argument collation", value=collation, expected_type=type_hints["collation"])
            check_type(argname="argument connection_pool_config", value=connection_pool_config, expected_type=type_hints["connection_pool_config"])
            check_type(argname="argument connector_enforcement", value=connector_enforcement, expected_type=type_hints["connector_enforcement"])
            check_type(argname="argument database_flags", value=database_flags, expected_type=type_hints["database_flags"])
            check_type(argname="argument data_cache_config", value=data_cache_config, expected_type=type_hints["data_cache_config"])
            check_type(argname="argument data_disk_provisioned_iops", value=data_disk_provisioned_iops, expected_type=type_hints["data_disk_provisioned_iops"])
            check_type(argname="argument data_disk_provisioned_throughput", value=data_disk_provisioned_throughput, expected_type=type_hints["data_disk_provisioned_throughput"])
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument deny_maintenance_period", value=deny_maintenance_period, expected_type=type_hints["deny_maintenance_period"])
            check_type(argname="argument disk_autoresize", value=disk_autoresize, expected_type=type_hints["disk_autoresize"])
            check_type(argname="argument disk_autoresize_limit", value=disk_autoresize_limit, expected_type=type_hints["disk_autoresize_limit"])
            check_type(argname="argument disk_size", value=disk_size, expected_type=type_hints["disk_size"])
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument enable_dataplex_integration", value=enable_dataplex_integration, expected_type=type_hints["enable_dataplex_integration"])
            check_type(argname="argument enable_google_ml_integration", value=enable_google_ml_integration, expected_type=type_hints["enable_google_ml_integration"])
            check_type(argname="argument insights_config", value=insights_config, expected_type=type_hints["insights_config"])
            check_type(argname="argument ip_configuration", value=ip_configuration, expected_type=type_hints["ip_configuration"])
            check_type(argname="argument location_preference", value=location_preference, expected_type=type_hints["location_preference"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument password_validation_policy", value=password_validation_policy, expected_type=type_hints["password_validation_policy"])
            check_type(argname="argument pricing_plan", value=pricing_plan, expected_type=type_hints["pricing_plan"])
            check_type(argname="argument retain_backups_on_delete", value=retain_backups_on_delete, expected_type=type_hints["retain_backups_on_delete"])
            check_type(argname="argument sql_server_audit_config", value=sql_server_audit_config, expected_type=type_hints["sql_server_audit_config"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument user_labels", value=user_labels, expected_type=type_hints["user_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tier": tier,
        }
        if activation_policy is not None:
            self._values["activation_policy"] = activation_policy
        if active_directory_config is not None:
            self._values["active_directory_config"] = active_directory_config
        if advanced_machine_features is not None:
            self._values["advanced_machine_features"] = advanced_machine_features
        if availability_type is not None:
            self._values["availability_type"] = availability_type
        if backup_configuration is not None:
            self._values["backup_configuration"] = backup_configuration
        if collation is not None:
            self._values["collation"] = collation
        if connection_pool_config is not None:
            self._values["connection_pool_config"] = connection_pool_config
        if connector_enforcement is not None:
            self._values["connector_enforcement"] = connector_enforcement
        if database_flags is not None:
            self._values["database_flags"] = database_flags
        if data_cache_config is not None:
            self._values["data_cache_config"] = data_cache_config
        if data_disk_provisioned_iops is not None:
            self._values["data_disk_provisioned_iops"] = data_disk_provisioned_iops
        if data_disk_provisioned_throughput is not None:
            self._values["data_disk_provisioned_throughput"] = data_disk_provisioned_throughput
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if deny_maintenance_period is not None:
            self._values["deny_maintenance_period"] = deny_maintenance_period
        if disk_autoresize is not None:
            self._values["disk_autoresize"] = disk_autoresize
        if disk_autoresize_limit is not None:
            self._values["disk_autoresize_limit"] = disk_autoresize_limit
        if disk_size is not None:
            self._values["disk_size"] = disk_size
        if disk_type is not None:
            self._values["disk_type"] = disk_type
        if edition is not None:
            self._values["edition"] = edition
        if enable_dataplex_integration is not None:
            self._values["enable_dataplex_integration"] = enable_dataplex_integration
        if enable_google_ml_integration is not None:
            self._values["enable_google_ml_integration"] = enable_google_ml_integration
        if insights_config is not None:
            self._values["insights_config"] = insights_config
        if ip_configuration is not None:
            self._values["ip_configuration"] = ip_configuration
        if location_preference is not None:
            self._values["location_preference"] = location_preference
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if password_validation_policy is not None:
            self._values["password_validation_policy"] = password_validation_policy
        if pricing_plan is not None:
            self._values["pricing_plan"] = pricing_plan
        if retain_backups_on_delete is not None:
            self._values["retain_backups_on_delete"] = retain_backups_on_delete
        if sql_server_audit_config is not None:
            self._values["sql_server_audit_config"] = sql_server_audit_config
        if time_zone is not None:
            self._values["time_zone"] = time_zone
        if user_labels is not None:
            self._values["user_labels"] = user_labels

    @builtins.property
    def tier(self) -> builtins.str:
        '''The machine type to use.

        See tiers for more details and supported versions. Postgres supports only shared-core machine types, and custom machine types such as db-custom-2-13312. See the Custom Machine Type Documentation to learn about specifying custom machine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#tier GoogleSqlDatabaseInstance#tier}
        '''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def activation_policy(self) -> typing.Optional[builtins.str]:
        '''This specifies when the instance should be active. Can be either ALWAYS, NEVER or ON_DEMAND.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#activation_policy GoogleSqlDatabaseInstance#activation_policy}
        '''
        result = self._values.get("activation_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def active_directory_config(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig"]:
        '''active_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#active_directory_config GoogleSqlDatabaseInstance#active_directory_config}
        '''
        result = self._values.get("active_directory_config")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig"], result)

    @builtins.property
    def advanced_machine_features(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures"]:
        '''advanced_machine_features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#advanced_machine_features GoogleSqlDatabaseInstance#advanced_machine_features}
        '''
        result = self._values.get("advanced_machine_features")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures"], result)

    @builtins.property
    def availability_type(self) -> typing.Optional[builtins.str]:
        '''The availability type of the Cloud SQL instance, high availability (REGIONAL) or single zone (ZONAL).

        For all instances, ensure that
        settings.backup_configuration.enabled is set to true.
        For MySQL instances, ensure that settings.backup_configuration.binary_log_enabled is set to true.
        For Postgres instances, ensure that settings.backup_configuration.point_in_time_recovery_enabled
        is set to true. Defaults to ZONAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#availability_type GoogleSqlDatabaseInstance#availability_type}
        '''
        result = self._values.get("availability_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_configuration(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsBackupConfiguration"]:
        '''backup_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#backup_configuration GoogleSqlDatabaseInstance#backup_configuration}
        '''
        result = self._values.get("backup_configuration")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsBackupConfiguration"], result)

    @builtins.property
    def collation(self) -> typing.Optional[builtins.str]:
        '''The name of server instance collation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#collation GoogleSqlDatabaseInstance#collation}
        '''
        result = self._values.get("collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_pool_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig"]]]:
        '''connection_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#connection_pool_config GoogleSqlDatabaseInstance#connection_pool_config}
        '''
        result = self._values.get("connection_pool_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig"]]], result)

    @builtins.property
    def connector_enforcement(self) -> typing.Optional[builtins.str]:
        '''Enables the enforcement of Cloud SQL Auth Proxy or Cloud SQL connectors for all the connections.

        If enabled, all the direct connections are rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#connector_enforcement GoogleSqlDatabaseInstance#connector_enforcement}
        '''
        result = self._values.get("connector_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_flags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsDatabaseFlags"]]]:
        '''database_flags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#database_flags GoogleSqlDatabaseInstance#database_flags}
        '''
        result = self._values.get("database_flags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsDatabaseFlags"]]], result)

    @builtins.property
    def data_cache_config(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsDataCacheConfig"]:
        '''data_cache_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_cache_config GoogleSqlDatabaseInstance#data_cache_config}
        '''
        result = self._values.get("data_cache_config")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsDataCacheConfig"], result)

    @builtins.property
    def data_disk_provisioned_iops(self) -> typing.Optional[jsii.Number]:
        '''Provisioned number of I/O operations per second for the data disk.

        This field is only used for HYPERDISK_BALANCED disk types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_disk_provisioned_iops GoogleSqlDatabaseInstance#data_disk_provisioned_iops}
        '''
        result = self._values.get("data_disk_provisioned_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_disk_provisioned_throughput(self) -> typing.Optional[jsii.Number]:
        '''Provisioned throughput measured in MiB per second for the data disk.

        This field is only used for HYPERDISK_BALANCED disk types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_disk_provisioned_throughput GoogleSqlDatabaseInstance#data_disk_provisioned_throughput}
        '''
        result = self._values.get("data_disk_provisioned_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Configuration to protect against accidental instance deletion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#deletion_protection_enabled GoogleSqlDatabaseInstance#deletion_protection_enabled}
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deny_maintenance_period(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod"]:
        '''deny_maintenance_period block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#deny_maintenance_period GoogleSqlDatabaseInstance#deny_maintenance_period}
        '''
        result = self._values.get("deny_maintenance_period")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod"], result)

    @builtins.property
    def disk_autoresize(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables auto-resizing of the storage size. Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_autoresize GoogleSqlDatabaseInstance#disk_autoresize}
        '''
        result = self._values.get("disk_autoresize")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disk_autoresize_limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum size, in GB, to which storage capacity can be automatically increased.

        The default value is 0, which specifies that there is no limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_autoresize_limit GoogleSqlDatabaseInstance#disk_autoresize_limit}
        '''
        result = self._values.get("disk_autoresize_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        '''The size of data disk, in GB.

        Size of a running instance cannot be reduced but can be increased. The minimum value is 10GB for PD_SSD, PD_HDD and 20GB for HYPERDISK_BALANCED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_size GoogleSqlDatabaseInstance#disk_size}
        '''
        result = self._values.get("disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''The type of supported data disk is tier dependent and can be PD_SSD or PD_HDD or HYPERDISK_BALANCED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disk_type GoogleSqlDatabaseInstance#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''The edition of the instance, can be ENTERPRISE or ENTERPRISE_PLUS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#edition GoogleSqlDatabaseInstance#edition}
        '''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_dataplex_integration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Dataplex Integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_dataplex_integration GoogleSqlDatabaseInstance#enable_dataplex_integration}
        '''
        result = self._values.get("enable_dataplex_integration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_google_ml_integration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Vertex AI Integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_google_ml_integration GoogleSqlDatabaseInstance#enable_google_ml_integration}
        '''
        result = self._values.get("enable_google_ml_integration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def insights_config(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsInsightsConfig"]:
        '''insights_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#insights_config GoogleSqlDatabaseInstance#insights_config}
        '''
        result = self._values.get("insights_config")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsInsightsConfig"], result)

    @builtins.property
    def ip_configuration(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsIpConfiguration"]:
        '''ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ip_configuration GoogleSqlDatabaseInstance#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsIpConfiguration"], result)

    @builtins.property
    def location_preference(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsLocationPreference"]:
        '''location_preference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#location_preference GoogleSqlDatabaseInstance#location_preference}
        '''
        result = self._values.get("location_preference")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsLocationPreference"], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#maintenance_window GoogleSqlDatabaseInstance#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsMaintenanceWindow"], result)

    @builtins.property
    def password_validation_policy(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy"]:
        '''password_validation_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#password_validation_policy GoogleSqlDatabaseInstance#password_validation_policy}
        '''
        result = self._values.get("password_validation_policy")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy"], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''Pricing plan for this instance, can only be PER_USE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#pricing_plan GoogleSqlDatabaseInstance#pricing_plan}
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retain_backups_on_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When this parameter is set to true, Cloud SQL retains backups of the instance even after the instance is deleted.

        The ON_DEMAND backup will be retained until customer deletes the backup or the project. The AUTOMATED backup will be retained based on the backups retention setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retain_backups_on_delete GoogleSqlDatabaseInstance#retain_backups_on_delete}
        '''
        result = self._values.get("retain_backups_on_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sql_server_audit_config(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig"]:
        '''sql_server_audit_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#sql_server_audit_config GoogleSqlDatabaseInstance#sql_server_audit_config}
        '''
        result = self._values.get("sql_server_audit_config")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time_zone to be used by the database engine (supported only for SQL Server), in SQL Server timezone format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#time_zone GoogleSqlDatabaseInstance#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value user label pairs to assign to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#user_labels GoogleSqlDatabaseInstance#user_labels}
        '''
        result = self._values.get("user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain"},
)
class GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig:
    def __init__(self, *, domain: builtins.str) -> None:
        '''
        :param domain: Domain name of the Active Directory for SQL Server (e.g., mydomain.com). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#domain GoogleSqlDatabaseInstance#domain}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c65ba761c500b804303cab634ed923e3a8c8460a5a4354bf8213110f6d4bb7)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
        }

    @builtins.property
    def domain(self) -> builtins.str:
        '''Domain name of the Active Directory for SQL Server (e.g., mydomain.com).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#domain GoogleSqlDatabaseInstance#domain}
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66a2c46dad7dadcdb5de90a90275300a27586a9a0e6eac9a9c56df98b9888817)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ca271111d665ee752e569ea03977b25d69544d1ad864aae08b62dcc75d8948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220cd5be0d75bee528768fe3d71482aa4a2c40fec1fac7e460ca2cfb738c707f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures",
    jsii_struct_bases=[],
    name_mapping={"threads_per_core": "threadsPerCore"},
)
class GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures:
    def __init__(
        self,
        *,
        threads_per_core: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param threads_per_core: The number of threads per physical core. Can be 1 or 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#threads_per_core GoogleSqlDatabaseInstance#threads_per_core}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378b996dbea28edcbe58ecc4e1525399396c5dd283d39d80f14e382dd042fbaa)
            check_type(argname="argument threads_per_core", value=threads_per_core, expected_type=type_hints["threads_per_core"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if threads_per_core is not None:
            self._values["threads_per_core"] = threads_per_core

    @builtins.property
    def threads_per_core(self) -> typing.Optional[jsii.Number]:
        '''The number of threads per physical core. Can be 1 or 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#threads_per_core GoogleSqlDatabaseInstance#threads_per_core}
        '''
        result = self._values.get("threads_per_core")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9d2d7ddc532e988e69aced30f9ceeaf816eae76a80976381fd07e29540a27b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetThreadsPerCore")
    def reset_threads_per_core(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreadsPerCore", []))

    @builtins.property
    @jsii.member(jsii_name="threadsPerCoreInput")
    def threads_per_core_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "threadsPerCoreInput"))

    @builtins.property
    @jsii.member(jsii_name="threadsPerCore")
    def threads_per_core(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threadsPerCore"))

    @threads_per_core.setter
    def threads_per_core(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1496c4094f0f1050e2686e921e6a607b9d8c3229605304b79edebc1cbc545c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threadsPerCore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a572dd2478ebb418294c645c5f4d4a1735d651c832c3e866e3b25310707d383c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsBackupConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "backup_retention_settings": "backupRetentionSettings",
        "binary_log_enabled": "binaryLogEnabled",
        "enabled": "enabled",
        "location": "location",
        "point_in_time_recovery_enabled": "pointInTimeRecoveryEnabled",
        "start_time": "startTime",
        "transaction_log_retention_days": "transactionLogRetentionDays",
    },
)
class GoogleSqlDatabaseInstanceSettingsBackupConfiguration:
    def __init__(
        self,
        *,
        backup_retention_settings: typing.Optional[typing.Union["GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        binary_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        start_time: typing.Optional[builtins.str] = None,
        transaction_log_retention_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_retention_settings: backup_retention_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#backup_retention_settings GoogleSqlDatabaseInstance#backup_retention_settings}
        :param binary_log_enabled: True if binary logging is enabled. If settings.backup_configuration.enabled is false, this must be as well. Can only be used with MySQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#binary_log_enabled GoogleSqlDatabaseInstance#binary_log_enabled}
        :param enabled: True if backup configuration is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enabled GoogleSqlDatabaseInstance#enabled}
        :param location: Location of the backup configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#location GoogleSqlDatabaseInstance#location}
        :param point_in_time_recovery_enabled: True if Point-in-time recovery is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#point_in_time_recovery_enabled GoogleSqlDatabaseInstance#point_in_time_recovery_enabled}
        :param start_time: HH:MM format time indicating when backup configuration starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#start_time GoogleSqlDatabaseInstance#start_time}
        :param transaction_log_retention_days: The number of days of transaction logs we retain for point in time restore, from 1-7. (For PostgreSQL Enterprise Plus instances, from 1 to 35.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#transaction_log_retention_days GoogleSqlDatabaseInstance#transaction_log_retention_days}
        '''
        if isinstance(backup_retention_settings, dict):
            backup_retention_settings = GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings(**backup_retention_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf613a580205d21b96bca5147b0022316cf820500c8cbf8a900613b742b6f9f2)
            check_type(argname="argument backup_retention_settings", value=backup_retention_settings, expected_type=type_hints["backup_retention_settings"])
            check_type(argname="argument binary_log_enabled", value=binary_log_enabled, expected_type=type_hints["binary_log_enabled"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument point_in_time_recovery_enabled", value=point_in_time_recovery_enabled, expected_type=type_hints["point_in_time_recovery_enabled"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument transaction_log_retention_days", value=transaction_log_retention_days, expected_type=type_hints["transaction_log_retention_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backup_retention_settings is not None:
            self._values["backup_retention_settings"] = backup_retention_settings
        if binary_log_enabled is not None:
            self._values["binary_log_enabled"] = binary_log_enabled
        if enabled is not None:
            self._values["enabled"] = enabled
        if location is not None:
            self._values["location"] = location
        if point_in_time_recovery_enabled is not None:
            self._values["point_in_time_recovery_enabled"] = point_in_time_recovery_enabled
        if start_time is not None:
            self._values["start_time"] = start_time
        if transaction_log_retention_days is not None:
            self._values["transaction_log_retention_days"] = transaction_log_retention_days

    @builtins.property
    def backup_retention_settings(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings"]:
        '''backup_retention_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#backup_retention_settings GoogleSqlDatabaseInstance#backup_retention_settings}
        '''
        result = self._values.get("backup_retention_settings")
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings"], result)

    @builtins.property
    def binary_log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if binary logging is enabled.

        If settings.backup_configuration.enabled is false, this must be as well. Can only be used with MySQL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#binary_log_enabled GoogleSqlDatabaseInstance#binary_log_enabled}
        '''
        result = self._values.get("binary_log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if backup configuration is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enabled GoogleSqlDatabaseInstance#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Location of the backup configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#location GoogleSqlDatabaseInstance#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def point_in_time_recovery_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if Point-in-time recovery is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#point_in_time_recovery_enabled GoogleSqlDatabaseInstance#point_in_time_recovery_enabled}
        '''
        result = self._values.get("point_in_time_recovery_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''HH:MM format time indicating when backup configuration starts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#start_time GoogleSqlDatabaseInstance#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transaction_log_retention_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days of transaction logs we retain for point in time restore, from 1-7.

        (For PostgreSQL Enterprise Plus instances, from 1 to 35.)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#transaction_log_retention_days GoogleSqlDatabaseInstance#transaction_log_retention_days}
        '''
        result = self._values.get("transaction_log_retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsBackupConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings",
    jsii_struct_bases=[],
    name_mapping={
        "retained_backups": "retainedBackups",
        "retention_unit": "retentionUnit",
    },
)
class GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings:
    def __init__(
        self,
        *,
        retained_backups: jsii.Number,
        retention_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param retained_backups: Number of backups to retain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retained_backups GoogleSqlDatabaseInstance#retained_backups}
        :param retention_unit: The unit that 'retainedBackups' represents. Defaults to COUNT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retention_unit GoogleSqlDatabaseInstance#retention_unit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a6f1425b459a8488649311f50719d465e7ebafd4f6f8954a3edfa59c429313)
            check_type(argname="argument retained_backups", value=retained_backups, expected_type=type_hints["retained_backups"])
            check_type(argname="argument retention_unit", value=retention_unit, expected_type=type_hints["retention_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "retained_backups": retained_backups,
        }
        if retention_unit is not None:
            self._values["retention_unit"] = retention_unit

    @builtins.property
    def retained_backups(self) -> jsii.Number:
        '''Number of backups to retain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retained_backups GoogleSqlDatabaseInstance#retained_backups}
        '''
        result = self._values.get("retained_backups")
        assert result is not None, "Required property 'retained_backups' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def retention_unit(self) -> typing.Optional[builtins.str]:
        '''The unit that 'retainedBackups' represents. Defaults to COUNT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retention_unit GoogleSqlDatabaseInstance#retention_unit}
        '''
        result = self._values.get("retention_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__187f11ea187fbe58b4bed629e2afb9d85554e642bf5ca16b4e0991729f798e45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRetentionUnit")
    def reset_retention_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionUnit", []))

    @builtins.property
    @jsii.member(jsii_name="retainedBackupsInput")
    def retained_backups_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retainedBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionUnitInput")
    def retention_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="retainedBackups")
    def retained_backups(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retainedBackups"))

    @retained_backups.setter
    def retained_backups(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cfd4b1bc459d5f2150b0174a0a4c26cd11367bbd3f28efb7dbd0efc44405bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainedBackups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionUnit")
    def retention_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionUnit"))

    @retention_unit.setter
    def retention_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86afc20916496dfc6237f0b9eb756624ce63d7c76c8c668a5ae2280e178d0ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f6889c8cd239101a18a1954d51705e373944eecc71012e20392d467f0aa312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceSettingsBackupConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsBackupConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cd8c173fb9000028e7e93937fdebfbddddaa734f70a508840fd8d856d40c371)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBackupRetentionSettings")
    def put_backup_retention_settings(
        self,
        *,
        retained_backups: jsii.Number,
        retention_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param retained_backups: Number of backups to retain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retained_backups GoogleSqlDatabaseInstance#retained_backups}
        :param retention_unit: The unit that 'retainedBackups' represents. Defaults to COUNT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retention_unit GoogleSqlDatabaseInstance#retention_unit}
        '''
        value = GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings(
            retained_backups=retained_backups, retention_unit=retention_unit
        )

        return typing.cast(None, jsii.invoke(self, "putBackupRetentionSettings", [value]))

    @jsii.member(jsii_name="resetBackupRetentionSettings")
    def reset_backup_retention_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupRetentionSettings", []))

    @jsii.member(jsii_name="resetBinaryLogEnabled")
    def reset_binary_log_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryLogEnabled", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetPointInTimeRecoveryEnabled")
    def reset_point_in_time_recovery_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPointInTimeRecoveryEnabled", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetTransactionLogRetentionDays")
    def reset_transaction_log_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransactionLogRetentionDays", []))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionSettings")
    def backup_retention_settings(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsOutputReference:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsOutputReference, jsii.get(self, "backupRetentionSettings"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionSettingsInput")
    def backup_retention_settings_input(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings], jsii.get(self, "backupRetentionSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryLogEnabledInput")
    def binary_log_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "binaryLogEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRecoveryEnabledInput")
    def point_in_time_recovery_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pointInTimeRecoveryEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="transactionLogRetentionDaysInput")
    def transaction_log_retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "transactionLogRetentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryLogEnabled")
    def binary_log_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "binaryLogEnabled"))

    @binary_log_enabled.setter
    def binary_log_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92a419708f8dfb39e39bbc52a6eefa2872846d6ba4aed78d59dad5c47522aa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryLogEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857883008f044387432c4cc9299a826feb4ae7cfc6e446774fc7e476b448add5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbed8723cab260c2f9720e9a3ea5f9a77711a8a8becb1e311af3c95d5ebf1e5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRecoveryEnabled")
    def point_in_time_recovery_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pointInTimeRecoveryEnabled"))

    @point_in_time_recovery_enabled.setter
    def point_in_time_recovery_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089fb626993e4bb2d0cbeddba91a496f2b04a79578ad258c016719419d69c3cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTimeRecoveryEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97d49a4a5ed2e5a427e16c9be05435a49f9bea708235d1b99f251e16dbd157da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transactionLogRetentionDays")
    def transaction_log_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "transactionLogRetentionDays"))

    @transaction_log_retention_days.setter
    def transaction_log_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605f54ad4c9643a63aca4861fd90f159d579345891eebd056a71981b9b2e4bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionLogRetentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfiguration]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7512d0409f3d807c97ed1b038f86cfb2ac579c103840873f1c392261dc9cbd3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connection_pooling_enabled": "connectionPoolingEnabled",
        "flags": "flags",
    },
)
class GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig:
    def __init__(
        self,
        *,
        connection_pooling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection_pooling_enabled: Whether Managed Connection Pool is enabled for this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#connection_pooling_enabled GoogleSqlDatabaseInstance#connection_pooling_enabled}
        :param flags: flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#flags GoogleSqlDatabaseInstance#flags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fdb7d7fe4edb1a2b998c6d6f00680786437624880ee204c0b1aa5b8e5b02ee5)
            check_type(argname="argument connection_pooling_enabled", value=connection_pooling_enabled, expected_type=type_hints["connection_pooling_enabled"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_pooling_enabled is not None:
            self._values["connection_pooling_enabled"] = connection_pooling_enabled
        if flags is not None:
            self._values["flags"] = flags

    @builtins.property
    def connection_pooling_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Managed Connection Pool is enabled for this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#connection_pooling_enabled GoogleSqlDatabaseInstance#connection_pooling_enabled}
        '''
        result = self._values.get("connection_pooling_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def flags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags"]]]:
        '''flags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#flags GoogleSqlDatabaseInstance#flags}
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Name of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#name GoogleSqlDatabaseInstance#name}
        :param value: Value of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#value GoogleSqlDatabaseInstance#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc434bf1be1dc4bc133f071a022be1f9a78eed60072d0e977873c7ffbb8ca2e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#name GoogleSqlDatabaseInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#value GoogleSqlDatabaseInstance#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__165f396520789d4f88a1abb89f69e1467deb86442d84f646129492c3530ffeba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4105def92cef6e1734896d127ebe9f4a15dccf5ad1b9332f6033001c5ccb2ae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506980258e9ef9e838c8e9f9ded36a5ae57872e5881cbda4a0428c98a6e1cded)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a15204f7f27bb7114c63a93ce3eebe0dfa065337a6ac4a7ce0758e10d5ce0d6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3acb794f991d784fcc54c8ad4a0320ee5804d7457205c88cdce6984bd0e8656e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d628bd88c63afa0e8b6dfb44f9b2cab4b38126572134e7b4c145323a0c3954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e4a7d40c5787c94255a630cc2cbf43f13e53121543c08d4b08d3fcc578a6336)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f9f3560b238b0fe8ae59a820f269bb8565f253b3d9a40c0dd0eb0be3e6c696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c73acf000861d10aeee6b0d2425cac2eea4edb94fe0a6a6c69e0efc45965e01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19918adde965cecdbd30e85a655738c942099abb43725a58b497ff31e6ab8ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f4de74c4bc9a332dce1cdddcdc8409f81abef440b4af18d3823363d02248de6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12ae40c83b290be62c528a2cfaff21c77550183e68c11db368657d854064695)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b51f9d980689a59a95799ae57875d8b0a389c35fcada543d28294ba9fac71e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__478c34933daa87ee75948166815c577f942dc5407915d206e409d75293e9cd58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d26172f868516c1f4a110e45cc11277e4ecb869d28032fa3b5f4bfce29ac2600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6368ed780f5deb474c45fa2bdeab5728da23b69e26d27614ca225ff9dc40461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e59f09fb0501a79fd8359b0caacce3ca38fa8c3e74e45bd94ca5eae40bffa45f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFlags")
    def put_flags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67e9c4dc6eede1830cf71c0438a4a4bad1dded49a8c6962c886ab004b424faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFlags", [value]))

    @jsii.member(jsii_name="resetConnectionPoolingEnabled")
    def reset_connection_pooling_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionPoolingEnabled", []))

    @jsii.member(jsii_name="resetFlags")
    def reset_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlags", []))

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlagsList:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlagsList, jsii.get(self, "flags"))

    @builtins.property
    @jsii.member(jsii_name="connectionPoolingEnabledInput")
    def connection_pooling_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "connectionPoolingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="flagsInput")
    def flags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]], jsii.get(self, "flagsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionPoolingEnabled")
    def connection_pooling_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "connectionPoolingEnabled"))

    @connection_pooling_enabled.setter
    def connection_pooling_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33817dbbb942e70eb5c36f0efdc537962ae5eb1d0d2e06f053d42d6322de009b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionPoolingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609f0dc648057567cecd99b3824541b6f02fd1111b0fac2405589dff0b830ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsDataCacheConfig",
    jsii_struct_bases=[],
    name_mapping={"data_cache_enabled": "dataCacheEnabled"},
)
class GoogleSqlDatabaseInstanceSettingsDataCacheConfig:
    def __init__(
        self,
        *,
        data_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param data_cache_enabled: Whether data cache is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_cache_enabled GoogleSqlDatabaseInstance#data_cache_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8343dfd654d4306803c4f092ef007b4c9f77cb84c151693eb689b3984dfb5cd1)
            check_type(argname="argument data_cache_enabled", value=data_cache_enabled, expected_type=type_hints["data_cache_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_cache_enabled is not None:
            self._values["data_cache_enabled"] = data_cache_enabled

    @builtins.property
    def data_cache_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether data cache is enabled for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_cache_enabled GoogleSqlDatabaseInstance#data_cache_enabled}
        '''
        result = self._values.get("data_cache_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsDataCacheConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsDataCacheConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsDataCacheConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe3b1a4f431f14b2554cfac75f75520299e63a69b93427581bd2aa25acbb06bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataCacheEnabled")
    def reset_data_cache_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCacheEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="dataCacheEnabledInput")
    def data_cache_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dataCacheEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCacheEnabled")
    def data_cache_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dataCacheEnabled"))

    @data_cache_enabled.setter
    def data_cache_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3d7e6da798cb5ab0ffe19db1abc46a4a3b70d7566050eaefd42af82e86685d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataCacheEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsDataCacheConfig]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsDataCacheConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsDataCacheConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf14e57cf4214fb10df4dcdf33f33347122f1f6143712228719e1b6939a717a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsDatabaseFlags",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleSqlDatabaseInstanceSettingsDatabaseFlags:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Name of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#name GoogleSqlDatabaseInstance#name}
        :param value: Value of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#value GoogleSqlDatabaseInstance#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a093853260d71f67b3e4dcb1eda9fedb77a8af75546480a911d37aa07e1abc9e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#name GoogleSqlDatabaseInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#value GoogleSqlDatabaseInstance#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsDatabaseFlags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsDatabaseFlagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsDatabaseFlagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__150d0fb2df26dc46d7f8ae3cca9b00207463a9c075094f88d4a4ecd0c49d04d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSqlDatabaseInstanceSettingsDatabaseFlagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e568ac6a3438db5c1b3eada3f2a69108a3f2b171c9ee8a1c7566051358b6137f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSqlDatabaseInstanceSettingsDatabaseFlagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9053f1adeff3a175035d0f690f3110d0cc7147528f76530e2b9573e374dbf7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd9770c2f843824ec027ad456a05f3bb1455ce5cc77f45f69b55974926c9035f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfaa8adcc0cc70e5f41f2bdebc931f7a5b264ce268f32f625d8ff40b5688b7cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsDatabaseFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsDatabaseFlags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsDatabaseFlags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ddc727e88ff1848ea7c7f9ab13a7a41f581a4b913d873cbdbec8569e0bc377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceSettingsDatabaseFlagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsDatabaseFlagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6f4808ca0774308a836e82567f39738fbfb2f79b6c5d0fb553b6a5b394d5b9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6fcdc821909c14c2129e12f810e075a2891288a59789725b4129df3be6eaaf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a55c70377ab3e29cf07c8e6328cb24a20f4accdd888e79d9822af1decfc4275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsDatabaseFlags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsDatabaseFlags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsDatabaseFlags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2475a82a164374b47dd1b9b875a33829adc6fc132debc4aa3aaf92b3e2a468ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod",
    jsii_struct_bases=[],
    name_mapping={"end_date": "endDate", "start_date": "startDate", "time": "time"},
)
class GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod:
    def __init__(
        self,
        *,
        end_date: builtins.str,
        start_date: builtins.str,
        time: builtins.str,
    ) -> None:
        '''
        :param end_date: End date before which maintenance will not take place. The date is in format yyyy-mm-dd i.e., 2020-11-01, or mm-dd, i.e., 11-01 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#end_date GoogleSqlDatabaseInstance#end_date}
        :param start_date: Start date after which maintenance will not take place. The date is in format yyyy-mm-dd i.e., 2020-11-01, or mm-dd, i.e., 11-01 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#start_date GoogleSqlDatabaseInstance#start_date}
        :param time: Time in UTC when the "deny maintenance period" starts on start_date and ends on end_date. The time is in format: HH:mm:SS, i.e., 00:00:00 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#time GoogleSqlDatabaseInstance#time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af8ba156714a80aaa98057b1b1375e2354f01f70c59ce8d9c022457dc7c8ede)
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_date": end_date,
            "start_date": start_date,
            "time": time,
        }

    @builtins.property
    def end_date(self) -> builtins.str:
        '''End date before which maintenance will not take place.

        The date is in format yyyy-mm-dd i.e., 2020-11-01, or mm-dd, i.e., 11-01

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#end_date GoogleSqlDatabaseInstance#end_date}
        '''
        result = self._values.get("end_date")
        assert result is not None, "Required property 'end_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_date(self) -> builtins.str:
        '''Start date after which maintenance will not take place.

        The date is in format yyyy-mm-dd i.e., 2020-11-01, or mm-dd, i.e., 11-01

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#start_date GoogleSqlDatabaseInstance#start_date}
        '''
        result = self._values.get("start_date")
        assert result is not None, "Required property 'start_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time(self) -> builtins.str:
        '''Time in UTC when the "deny maintenance period" starts on start_date and ends on end_date.

        The time is in format: HH:mm:SS, i.e., 00:00:00

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#time GoogleSqlDatabaseInstance#time}
        '''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9cac10f55b9024680b46d7f836126d168e9f32dc599e1d285b59d0740864308)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endDate"))

    @end_date.setter
    def end_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df3505e077753924c13bddb8bb6d8ced54860e679f95f48ed2e9d64f5de11b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startDate"))

    @start_date.setter
    def start_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5137c9ec63900c1332fce4503d651463617be065728793164d3ae04b5ce0ca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b33b67c3f1a0ec7113600e4484600369da0ae6e2c03da55c7f7bcf923634287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e067efa1cc6da685aa3ed40820d3cef91997a72d2d1183f0277fd65d6b1cf32d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsInsightsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "query_insights_enabled": "queryInsightsEnabled",
        "query_plans_per_minute": "queryPlansPerMinute",
        "query_string_length": "queryStringLength",
        "record_application_tags": "recordApplicationTags",
        "record_client_address": "recordClientAddress",
    },
)
class GoogleSqlDatabaseInstanceSettingsInsightsConfig:
    def __init__(
        self,
        *,
        query_insights_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_plans_per_minute: typing.Optional[jsii.Number] = None,
        query_string_length: typing.Optional[jsii.Number] = None,
        record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param query_insights_enabled: True if Query Insights feature is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#query_insights_enabled GoogleSqlDatabaseInstance#query_insights_enabled}
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. Between 0 and 20. Default to 5. For Enterprise Plus instances, from 0 to 200. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#query_plans_per_minute GoogleSqlDatabaseInstance#query_plans_per_minute}
        :param query_string_length: Maximum query length stored in bytes. Between 256 and 4500. Default to 1024. For Enterprise Plus instances, from 1 to 1048576. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#query_string_length GoogleSqlDatabaseInstance#query_string_length}
        :param record_application_tags: True if Query Insights will record application tags from query when enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#record_application_tags GoogleSqlDatabaseInstance#record_application_tags}
        :param record_client_address: True if Query Insights will record client address when enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#record_client_address GoogleSqlDatabaseInstance#record_client_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb454ffedcfba27aa3eb147fa041858d8ec39d79af5533137a357af7651e2867)
            check_type(argname="argument query_insights_enabled", value=query_insights_enabled, expected_type=type_hints["query_insights_enabled"])
            check_type(argname="argument query_plans_per_minute", value=query_plans_per_minute, expected_type=type_hints["query_plans_per_minute"])
            check_type(argname="argument query_string_length", value=query_string_length, expected_type=type_hints["query_string_length"])
            check_type(argname="argument record_application_tags", value=record_application_tags, expected_type=type_hints["record_application_tags"])
            check_type(argname="argument record_client_address", value=record_client_address, expected_type=type_hints["record_client_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if query_insights_enabled is not None:
            self._values["query_insights_enabled"] = query_insights_enabled
        if query_plans_per_minute is not None:
            self._values["query_plans_per_minute"] = query_plans_per_minute
        if query_string_length is not None:
            self._values["query_string_length"] = query_string_length
        if record_application_tags is not None:
            self._values["record_application_tags"] = record_application_tags
        if record_client_address is not None:
            self._values["record_client_address"] = record_client_address

    @builtins.property
    def query_insights_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if Query Insights feature is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#query_insights_enabled GoogleSqlDatabaseInstance#query_insights_enabled}
        '''
        result = self._values.get("query_insights_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_plans_per_minute(self) -> typing.Optional[jsii.Number]:
        '''Number of query execution plans captured by Insights per minute for all queries combined.

        Between 0 and 20. Default to 5. For Enterprise Plus instances, from 0 to 200.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#query_plans_per_minute GoogleSqlDatabaseInstance#query_plans_per_minute}
        '''
        result = self._values.get("query_plans_per_minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def query_string_length(self) -> typing.Optional[jsii.Number]:
        '''Maximum query length stored in bytes.

        Between 256 and 4500. Default to 1024. For Enterprise Plus instances, from 1 to 1048576.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#query_string_length GoogleSqlDatabaseInstance#query_string_length}
        '''
        result = self._values.get("query_string_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def record_application_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if Query Insights will record application tags from query when enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#record_application_tags GoogleSqlDatabaseInstance#record_application_tags}
        '''
        result = self._values.get("record_application_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def record_client_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if Query Insights will record client address when enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#record_client_address GoogleSqlDatabaseInstance#record_client_address}
        '''
        result = self._values.get("record_client_address")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsInsightsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsInsightsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsInsightsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6c77864d562093e1cd7b1651d5b9a1457ab5f81d7dc426f0443ae7b7ff6f09a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQueryInsightsEnabled")
    def reset_query_insights_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryInsightsEnabled", []))

    @jsii.member(jsii_name="resetQueryPlansPerMinute")
    def reset_query_plans_per_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryPlansPerMinute", []))

    @jsii.member(jsii_name="resetQueryStringLength")
    def reset_query_string_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringLength", []))

    @jsii.member(jsii_name="resetRecordApplicationTags")
    def reset_record_application_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordApplicationTags", []))

    @jsii.member(jsii_name="resetRecordClientAddress")
    def reset_record_client_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordClientAddress", []))

    @builtins.property
    @jsii.member(jsii_name="queryInsightsEnabledInput")
    def query_insights_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "queryInsightsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="queryPlansPerMinuteInput")
    def query_plans_per_minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryPlansPerMinuteInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringLengthInput")
    def query_string_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryStringLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="recordApplicationTagsInput")
    def record_application_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "recordApplicationTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="recordClientAddressInput")
    def record_client_address_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "recordClientAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInsightsEnabled")
    def query_insights_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "queryInsightsEnabled"))

    @query_insights_enabled.setter
    def query_insights_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6774db75daf3b69d7274ac7a591909d1c5119d149791b245b9cc6f9be856c8e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryInsightsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryPlansPerMinute")
    def query_plans_per_minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryPlansPerMinute"))

    @query_plans_per_minute.setter
    def query_plans_per_minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58c8d9e5c9bdda2be7d2077a8b7f01b86311dd6606f22c31f6a843141716e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryPlansPerMinute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringLength")
    def query_string_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryStringLength"))

    @query_string_length.setter
    def query_string_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29b4cb8d78092549faccb97a1e7299ef93b6a7c7b83b2f2e39152c3db805715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordApplicationTags")
    def record_application_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "recordApplicationTags"))

    @record_application_tags.setter
    def record_application_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__877d6f4680423dc4b484db9d67e4996e1ec3ec7963c23706248e800507f068e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordApplicationTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordClientAddress")
    def record_client_address(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "recordClientAddress"))

    @record_client_address.setter
    def record_client_address(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e745128f40817eb9399e18d4a59b6161cef40a67ba6c453541de340a781c2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordClientAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsInsightsConfig]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsInsightsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsInsightsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a856dc853c9c34e9f70cce6a208fdc5a8ed79b326bdc98ff76babb3adf418cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "allocated_ip_range": "allocatedIpRange",
        "authorized_networks": "authorizedNetworks",
        "custom_subject_alternative_names": "customSubjectAlternativeNames",
        "enable_private_path_for_google_cloud_services": "enablePrivatePathForGoogleCloudServices",
        "ipv4_enabled": "ipv4Enabled",
        "private_network": "privateNetwork",
        "psc_config": "pscConfig",
        "server_ca_mode": "serverCaMode",
        "server_ca_pool": "serverCaPool",
        "ssl_mode": "sslMode",
    },
)
class GoogleSqlDatabaseInstanceSettingsIpConfiguration:
    def __init__(
        self,
        *,
        allocated_ip_range: typing.Optional[builtins.str] = None,
        authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_private_path_for_google_cloud_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ipv4_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_network: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        server_ca_mode: typing.Optional[builtins.str] = None,
        server_ca_pool: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocated_ip_range: The name of the allocated ip range for the private ip CloudSQL instance. For example: "google-managed-services-default". If set, the instance ip will be created in the allocated range. The range name must comply with RFC 1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#allocated_ip_range GoogleSqlDatabaseInstance#allocated_ip_range}
        :param authorized_networks: authorized_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#authorized_networks GoogleSqlDatabaseInstance#authorized_networks}
        :param custom_subject_alternative_names: The custom subject alternative names for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#custom_subject_alternative_names GoogleSqlDatabaseInstance#custom_subject_alternative_names}
        :param enable_private_path_for_google_cloud_services: Whether Google Cloud services such as BigQuery are allowed to access data in this Cloud SQL instance over a private IP connection. SQLSERVER database type is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_private_path_for_google_cloud_services GoogleSqlDatabaseInstance#enable_private_path_for_google_cloud_services}
        :param ipv4_enabled: Whether this Cloud SQL instance should be assigned a public IPV4 address. At least ipv4_enabled must be enabled or a private_network must be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ipv4_enabled GoogleSqlDatabaseInstance#ipv4_enabled}
        :param private_network: The VPC network from which the Cloud SQL instance is accessible for private IP. For example, projects/myProject/global/networks/default. Specifying a network enables private IP. At least ipv4_enabled must be enabled or a private_network must be configured. This setting can be updated, but it cannot be removed after it is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#private_network GoogleSqlDatabaseInstance#private_network}
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#psc_config GoogleSqlDatabaseInstance#psc_config}
        :param server_ca_mode: Specify how the server certificate's Certificate Authority is hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#server_ca_mode GoogleSqlDatabaseInstance#server_ca_mode}
        :param server_ca_pool: The resource name of the server CA pool for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#server_ca_pool GoogleSqlDatabaseInstance#server_ca_pool}
        :param ssl_mode: Specify how SSL connection should be enforced in DB connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ssl_mode GoogleSqlDatabaseInstance#ssl_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1daccc9c20c831ceddfe147142938378c93bff9dbfa12eda21b9149579bd3b)
            check_type(argname="argument allocated_ip_range", value=allocated_ip_range, expected_type=type_hints["allocated_ip_range"])
            check_type(argname="argument authorized_networks", value=authorized_networks, expected_type=type_hints["authorized_networks"])
            check_type(argname="argument custom_subject_alternative_names", value=custom_subject_alternative_names, expected_type=type_hints["custom_subject_alternative_names"])
            check_type(argname="argument enable_private_path_for_google_cloud_services", value=enable_private_path_for_google_cloud_services, expected_type=type_hints["enable_private_path_for_google_cloud_services"])
            check_type(argname="argument ipv4_enabled", value=ipv4_enabled, expected_type=type_hints["ipv4_enabled"])
            check_type(argname="argument private_network", value=private_network, expected_type=type_hints["private_network"])
            check_type(argname="argument psc_config", value=psc_config, expected_type=type_hints["psc_config"])
            check_type(argname="argument server_ca_mode", value=server_ca_mode, expected_type=type_hints["server_ca_mode"])
            check_type(argname="argument server_ca_pool", value=server_ca_pool, expected_type=type_hints["server_ca_pool"])
            check_type(argname="argument ssl_mode", value=ssl_mode, expected_type=type_hints["ssl_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_ip_range is not None:
            self._values["allocated_ip_range"] = allocated_ip_range
        if authorized_networks is not None:
            self._values["authorized_networks"] = authorized_networks
        if custom_subject_alternative_names is not None:
            self._values["custom_subject_alternative_names"] = custom_subject_alternative_names
        if enable_private_path_for_google_cloud_services is not None:
            self._values["enable_private_path_for_google_cloud_services"] = enable_private_path_for_google_cloud_services
        if ipv4_enabled is not None:
            self._values["ipv4_enabled"] = ipv4_enabled
        if private_network is not None:
            self._values["private_network"] = private_network
        if psc_config is not None:
            self._values["psc_config"] = psc_config
        if server_ca_mode is not None:
            self._values["server_ca_mode"] = server_ca_mode
        if server_ca_pool is not None:
            self._values["server_ca_pool"] = server_ca_pool
        if ssl_mode is not None:
            self._values["ssl_mode"] = ssl_mode

    @builtins.property
    def allocated_ip_range(self) -> typing.Optional[builtins.str]:
        '''The name of the allocated ip range for the private ip CloudSQL instance.

        For example: "google-managed-services-default". If set, the instance ip will be created in the allocated range. The range name must comply with RFC 1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#allocated_ip_range GoogleSqlDatabaseInstance#allocated_ip_range}
        '''
        result = self._values.get("allocated_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorized_networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks"]]]:
        '''authorized_networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#authorized_networks GoogleSqlDatabaseInstance#authorized_networks}
        '''
        result = self._values.get("authorized_networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks"]]], result)

    @builtins.property
    def custom_subject_alternative_names(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The custom subject alternative names for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#custom_subject_alternative_names GoogleSqlDatabaseInstance#custom_subject_alternative_names}
        '''
        result = self._values.get("custom_subject_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_private_path_for_google_cloud_services(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Google Cloud services such as BigQuery are allowed to access data in this Cloud SQL instance over a private IP connection.

        SQLSERVER database type is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_private_path_for_google_cloud_services GoogleSqlDatabaseInstance#enable_private_path_for_google_cloud_services}
        '''
        result = self._values.get("enable_private_path_for_google_cloud_services")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ipv4_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this Cloud SQL instance should be assigned a public IPV4 address.

        At least ipv4_enabled must be enabled or a private_network must be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ipv4_enabled GoogleSqlDatabaseInstance#ipv4_enabled}
        '''
        result = self._values.get("ipv4_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_network(self) -> typing.Optional[builtins.str]:
        '''The VPC network from which the Cloud SQL instance is accessible for private IP.

        For example, projects/myProject/global/networks/default. Specifying a network enables private IP. At least ipv4_enabled must be enabled or a private_network must be configured. This setting can be updated, but it cannot be removed after it is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#private_network GoogleSqlDatabaseInstance#private_network}
        '''
        result = self._values.get("private_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig"]]]:
        '''psc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#psc_config GoogleSqlDatabaseInstance#psc_config}
        '''
        result = self._values.get("psc_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig"]]], result)

    @builtins.property
    def server_ca_mode(self) -> typing.Optional[builtins.str]:
        '''Specify how the server certificate's Certificate Authority is hosted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#server_ca_mode GoogleSqlDatabaseInstance#server_ca_mode}
        '''
        result = self._values.get("server_ca_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_ca_pool(self) -> typing.Optional[builtins.str]:
        '''The resource name of the server CA pool for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#server_ca_pool GoogleSqlDatabaseInstance#server_ca_pool}
        '''
        result = self._values.get("server_ca_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        '''Specify how SSL connection should be enforced in DB connections.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ssl_mode GoogleSqlDatabaseInstance#ssl_mode}
        '''
        result = self._values.get("ssl_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "expiration_time": "expirationTime",
        "name": "name",
    },
)
class GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks:
    def __init__(
        self,
        *,
        value: builtins.str,
        expiration_time: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#value GoogleSqlDatabaseInstance#value}.
        :param expiration_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#expiration_time GoogleSqlDatabaseInstance#expiration_time}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#name GoogleSqlDatabaseInstance#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99715386d56f8d42ec1b55d4a939ac03da764dfface076026828a40baa3d4376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument expiration_time", value=expiration_time, expected_type=type_hints["expiration_time"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if expiration_time is not None:
            self._values["expiration_time"] = expiration_time
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#value GoogleSqlDatabaseInstance#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#expiration_time GoogleSqlDatabaseInstance#expiration_time}.'''
        result = self._values.get("expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#name GoogleSqlDatabaseInstance#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be081cab968ddc30e1760f4f4cd67d0f4fc3d8d89985a23f35d5443900aa8ed1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52443188b35b199b76544861e887c7474d3341b7233d04e9e142b5fee5a03524)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57bca9478c27b8cdeef38c4471bcfe0cf741a18fbbdfb15f63158654ab428c1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ac31aa7aebcbd696916cf6b91fea58ca3983f19f6309d67624cda6ff6a462f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a5fdc8d1d53abd513d399c255eab00751c5a12246c29d043ab659ca3715842a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5235e2bfb508f0f8d7f08fac4baab50b0b41431dc17052c7d39466f8c604bd89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43fe2b03b3195d128941930cee963bf87f1ca77fe280cc09a695b6a39697bef8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExpirationTime")
    def reset_expiration_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationTime", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="expirationTimeInput")
    def expiration_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationTime")
    def expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationTime"))

    @expiration_time.setter
    def expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0130d2c2d6e0b1774f24153d53c120768863e60cd52471bec52412ec208f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce107946d0a469366d356327921059a47bd6d6e0bf281cefc6772cd8f4a3cec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed732d042ca06db5d6ed387d8d973b97ebf0fc6350a2bbbf0162507de9dc6b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9ad08d7f712bafe8441c30cdf53de40f8796793db8ac53c3c82cb21674affa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceSettingsIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaa89dd5bc890ea2b0fe002a55a7fc98eb7fc6ec5dbaa97bfa94e13fb0800ec1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizedNetworks")
    def put_authorized_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a6baebddd19161ef1278bce888ea7607c495a7f4e469a8a0452bfd3fe66872d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthorizedNetworks", [value]))

    @jsii.member(jsii_name="putPscConfig")
    def put_psc_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3199b7b92b60f8c8467d3ca4eb9a98004faacaba6ae02b8fd7fd1ceef066bd9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPscConfig", [value]))

    @jsii.member(jsii_name="resetAllocatedIpRange")
    def reset_allocated_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedIpRange", []))

    @jsii.member(jsii_name="resetAuthorizedNetworks")
    def reset_authorized_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizedNetworks", []))

    @jsii.member(jsii_name="resetCustomSubjectAlternativeNames")
    def reset_custom_subject_alternative_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomSubjectAlternativeNames", []))

    @jsii.member(jsii_name="resetEnablePrivatePathForGoogleCloudServices")
    def reset_enable_private_path_for_google_cloud_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePrivatePathForGoogleCloudServices", []))

    @jsii.member(jsii_name="resetIpv4Enabled")
    def reset_ipv4_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4Enabled", []))

    @jsii.member(jsii_name="resetPrivateNetwork")
    def reset_private_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateNetwork", []))

    @jsii.member(jsii_name="resetPscConfig")
    def reset_psc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscConfig", []))

    @jsii.member(jsii_name="resetServerCaMode")
    def reset_server_ca_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerCaMode", []))

    @jsii.member(jsii_name="resetServerCaPool")
    def reset_server_ca_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerCaPool", []))

    @jsii.member(jsii_name="resetSslMode")
    def reset_ssl_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslMode", []))

    @builtins.property
    @jsii.member(jsii_name="authorizedNetworks")
    def authorized_networks(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksList:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksList, jsii.get(self, "authorizedNetworks"))

    @builtins.property
    @jsii.member(jsii_name="pscConfig")
    def psc_config(
        self,
    ) -> "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigList":
        return typing.cast("GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigList", jsii.get(self, "pscConfig"))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpRangeInput")
    def allocated_ip_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allocatedIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedNetworksInput")
    def authorized_networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]], jsii.get(self, "authorizedNetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="customSubjectAlternativeNamesInput")
    def custom_subject_alternative_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customSubjectAlternativeNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePrivatePathForGoogleCloudServicesInput")
    def enable_private_path_for_google_cloud_services_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePrivatePathForGoogleCloudServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4EnabledInput")
    def ipv4_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipv4EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="privateNetworkInput")
    def private_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="pscConfigInput")
    def psc_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig"]]], jsii.get(self, "pscConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serverCaModeInput")
    def server_ca_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverCaModeInput"))

    @builtins.property
    @jsii.member(jsii_name="serverCaPoolInput")
    def server_ca_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverCaPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="sslModeInput")
    def ssl_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslModeInput"))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpRange")
    def allocated_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allocatedIpRange"))

    @allocated_ip_range.setter
    def allocated_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f46bef173bb462231b8c1841d372d634167a020f8f9e46c81911be12041b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocatedIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customSubjectAlternativeNames")
    def custom_subject_alternative_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customSubjectAlternativeNames"))

    @custom_subject_alternative_names.setter
    def custom_subject_alternative_names(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e582e35bf6868d3774018149cbe94a84871fd63b52ac1da86e415662f2ce29ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customSubjectAlternativeNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePrivatePathForGoogleCloudServices")
    def enable_private_path_for_google_cloud_services(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePrivatePathForGoogleCloudServices"))

    @enable_private_path_for_google_cloud_services.setter
    def enable_private_path_for_google_cloud_services(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822b773ef664744ca464cfd13e9b8aa8914fe0e11317f271dc2e1868174e805b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivatePathForGoogleCloudServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv4Enabled")
    def ipv4_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipv4Enabled"))

    @ipv4_enabled.setter
    def ipv4_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c1d0b6ece9c3f3ae897af290e151d4c97ac57f4eb3a830d53ff06ab293ae49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateNetwork")
    def private_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateNetwork"))

    @private_network.setter
    def private_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db894bc6bd2cdb7048bd5e13aea9dd8d580e7f1ea07b12563723e2dcbaaf582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverCaMode")
    def server_ca_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverCaMode"))

    @server_ca_mode.setter
    def server_ca_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78fb9720669680f68ab2aefdf6e7ec7a8044361c57b3497137bce97e4918f108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCaMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverCaPool")
    def server_ca_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverCaPool"))

    @server_ca_pool.setter
    def server_ca_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__193570d5e053914d17333f243e349b7a3fb9ca882fc521bd8265fd89e9303522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCaPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslMode")
    def ssl_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslMode"))

    @ssl_mode.setter
    def ssl_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3363c6e1ad88fa9ae45a09084bc7b5381f6060b348359eaab98ea0b2e344ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsIpConfiguration]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsIpConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsIpConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844880cff83c86f4e5be3b25cacb1d89e1ef9a05355355e103bb1d6525785e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_consumer_projects": "allowedConsumerProjects",
        "psc_auto_connections": "pscAutoConnections",
        "psc_enabled": "pscEnabled",
    },
)
class GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig:
    def __init__(
        self,
        *,
        allowed_consumer_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_consumer_projects: List of consumer projects that are allow-listed for PSC connections to this instance. This instance can be connected to with PSC from any network in these projects. Each consumer project in this list may be represented by a project number (numeric) or by a project id (alphanumeric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#allowed_consumer_projects GoogleSqlDatabaseInstance#allowed_consumer_projects}
        :param psc_auto_connections: psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#psc_auto_connections GoogleSqlDatabaseInstance#psc_auto_connections}
        :param psc_enabled: Whether PSC connectivity is enabled for this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#psc_enabled GoogleSqlDatabaseInstance#psc_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3177f9d5e531abd325a0882875f59dcf23cbe84a3c247ae1bd8b08d80f3de1b1)
            check_type(argname="argument allowed_consumer_projects", value=allowed_consumer_projects, expected_type=type_hints["allowed_consumer_projects"])
            check_type(argname="argument psc_auto_connections", value=psc_auto_connections, expected_type=type_hints["psc_auto_connections"])
            check_type(argname="argument psc_enabled", value=psc_enabled, expected_type=type_hints["psc_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_consumer_projects is not None:
            self._values["allowed_consumer_projects"] = allowed_consumer_projects
        if psc_auto_connections is not None:
            self._values["psc_auto_connections"] = psc_auto_connections
        if psc_enabled is not None:
            self._values["psc_enabled"] = psc_enabled

    @builtins.property
    def allowed_consumer_projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of consumer projects that are allow-listed for PSC connections to this instance.

        This instance can be connected to with PSC from any network in these projects. Each consumer project in this list may be represented by a project number (numeric) or by a project id (alphanumeric).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#allowed_consumer_projects GoogleSqlDatabaseInstance#allowed_consumer_projects}
        '''
        result = self._values.get("allowed_consumer_projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def psc_auto_connections(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections"]]]:
        '''psc_auto_connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#psc_auto_connections GoogleSqlDatabaseInstance#psc_auto_connections}
        '''
        result = self._values.get("psc_auto_connections")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections"]]], result)

    @builtins.property
    def psc_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether PSC connectivity is enabled for this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#psc_enabled GoogleSqlDatabaseInstance#psc_enabled}
        '''
        result = self._values.get("psc_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2374aaa831b86fd437cea31453a561d732223ab3bd903ec74e404b13df6e6fd6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d6ac65851efafdf297a7a5f18721d366f81b9f9e4654c2a7f3cd177e256c21)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8171e29104ca6838f0632f124182e96729c1845e76af6de9b34ac1b31c3962)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93d74025e5d12831c5e67e124adc36ec2cde2d6148ccd504071ff1b72aa46de1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfa1132db9477fea22f3a421c366b87df94d5d1a4a7b836c951167ddb0f891f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e752d753925076afda99edcd217e893637aea8bb2646b4dac284853513938e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66797db70e918a2aa71ffdde62b674f3102d1f51a202e36849dca4e7c4c9e5b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPscAutoConnections")
    def put_psc_auto_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ae619efb4e17e25f275e6bf6cd8099558587e553429d69ae8c603013b5f1b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPscAutoConnections", [value]))

    @jsii.member(jsii_name="resetAllowedConsumerProjects")
    def reset_allowed_consumer_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedConsumerProjects", []))

    @jsii.member(jsii_name="resetPscAutoConnections")
    def reset_psc_auto_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscAutoConnections", []))

    @jsii.member(jsii_name="resetPscEnabled")
    def reset_psc_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="pscAutoConnections")
    def psc_auto_connections(
        self,
    ) -> "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsList":
        return typing.cast("GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsList", jsii.get(self, "pscAutoConnections"))

    @builtins.property
    @jsii.member(jsii_name="allowedConsumerProjectsInput")
    def allowed_consumer_projects_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedConsumerProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="pscAutoConnectionsInput")
    def psc_auto_connections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections"]]], jsii.get(self, "pscAutoConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="pscEnabledInput")
    def psc_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pscEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedConsumerProjects")
    def allowed_consumer_projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedConsumerProjects"))

    @allowed_consumer_projects.setter
    def allowed_consumer_projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0efae9ad81f99741789388c1bc65921256e52e2806798e8aa0e98f724047ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedConsumerProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pscEnabled")
    def psc_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pscEnabled"))

    @psc_enabled.setter
    def psc_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e406276b7ec31392a63ec1e77d3044743aed6add185519e755f272e5e698611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pscEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe587ac7f1a092898a66fa817b887cbc544f18d72ed3d45543301721512c5fbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_network": "consumerNetwork",
        "consumer_service_project_id": "consumerServiceProjectId",
    },
)
class GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections:
    def __init__(
        self,
        *,
        consumer_network: builtins.str,
        consumer_service_project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_network: The consumer network of this consumer endpoint. This must be a resource path that includes both the host project and the network name. The consumer host project of this network might be different from the consumer service project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#consumer_network GoogleSqlDatabaseInstance#consumer_network}
        :param consumer_service_project_id: The project ID of consumer service project of this consumer endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#consumer_service_project_id GoogleSqlDatabaseInstance#consumer_service_project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afdbc90d49d00684cee71fca228098205574f849b379d4fd013d671c802f5522)
            check_type(argname="argument consumer_network", value=consumer_network, expected_type=type_hints["consumer_network"])
            check_type(argname="argument consumer_service_project_id", value=consumer_service_project_id, expected_type=type_hints["consumer_service_project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_network": consumer_network,
        }
        if consumer_service_project_id is not None:
            self._values["consumer_service_project_id"] = consumer_service_project_id

    @builtins.property
    def consumer_network(self) -> builtins.str:
        '''The consumer network of this consumer endpoint.

        This must be a resource path that includes both the host project and the network name. The consumer host project of this network might be different from the consumer service project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#consumer_network GoogleSqlDatabaseInstance#consumer_network}
        '''
        result = self._values.get("consumer_network")
        assert result is not None, "Required property 'consumer_network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_service_project_id(self) -> typing.Optional[builtins.str]:
        '''The project ID of consumer service project of this consumer endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#consumer_service_project_id GoogleSqlDatabaseInstance#consumer_service_project_id}
        '''
        result = self._values.get("consumer_service_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__978a5ffd3fbeaaaf75cae9f7f6319b94d5058571cfa1b87391e53102678cd3eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8264da5a4b41ff5f483f1d12ce0e6ceee45d613db16fe213c839f0e7cf61a610)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c49677812fc4577243fbc568a9fc1aab79d5e3bd34599e2ef2570c2f999ca4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65f8298fd91d3ebe14f6e0ff7a8054b29365db2d15abe93bdb4b0203f52777f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18ea1f1e1aeac44a08f0c85424e443e7c74c8e0b219ee42f476112bf16c16cc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7e8d5e9f120ec877aa29390819c3ab72e437ff042a724a5a846a20911bfd84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa10413a061b2e4bd4a4eed3501c866b2d3226b60c6faf41a3dcffd6b83f1a9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConsumerServiceProjectId")
    def reset_consumer_service_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerServiceProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="consumerNetworkInput")
    def consumer_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerServiceProjectIdInput")
    def consumer_service_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerServiceProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerNetwork")
    def consumer_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerNetwork"))

    @consumer_network.setter
    def consumer_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97809894ac26b96e713e68c349e9a0026ca30af11fdb20385d338ef10fb647d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerServiceProjectId")
    def consumer_service_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerServiceProjectId"))

    @consumer_service_project_id.setter
    def consumer_service_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c52b5992b33ef097a0e6baa1b7995b79cecacef97036f9f0f88dfe4741eab6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerServiceProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4595d182557a67ea649e2db70b6459d2e5a1b2629933a6e665ab47f6e759754e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsLocationPreference",
    jsii_struct_bases=[],
    name_mapping={
        "follow_gae_application": "followGaeApplication",
        "secondary_zone": "secondaryZone",
        "zone": "zone",
    },
)
class GoogleSqlDatabaseInstanceSettingsLocationPreference:
    def __init__(
        self,
        *,
        follow_gae_application: typing.Optional[builtins.str] = None,
        secondary_zone: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param follow_gae_application: A Google App Engine application whose zone to remain in. Must be in the same region as this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#follow_gae_application GoogleSqlDatabaseInstance#follow_gae_application}
        :param secondary_zone: The preferred Compute Engine zone for the secondary/failover. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#secondary_zone GoogleSqlDatabaseInstance#secondary_zone}
        :param zone: The preferred compute engine zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#zone GoogleSqlDatabaseInstance#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067a947017c105aad37746c2e8b3b522d4e328cfc0404b9e5809c1b9563d93b4)
            check_type(argname="argument follow_gae_application", value=follow_gae_application, expected_type=type_hints["follow_gae_application"])
            check_type(argname="argument secondary_zone", value=secondary_zone, expected_type=type_hints["secondary_zone"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if follow_gae_application is not None:
            self._values["follow_gae_application"] = follow_gae_application
        if secondary_zone is not None:
            self._values["secondary_zone"] = secondary_zone
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def follow_gae_application(self) -> typing.Optional[builtins.str]:
        '''A Google App Engine application whose zone to remain in. Must be in the same region as this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#follow_gae_application GoogleSqlDatabaseInstance#follow_gae_application}
        '''
        result = self._values.get("follow_gae_application")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_zone(self) -> typing.Optional[builtins.str]:
        '''The preferred Compute Engine zone for the secondary/failover.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#secondary_zone GoogleSqlDatabaseInstance#secondary_zone}
        '''
        result = self._values.get("secondary_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The preferred compute engine zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#zone GoogleSqlDatabaseInstance#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsLocationPreference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsLocationPreferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsLocationPreferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecdc8898bf79b5b438c281f9de456c1fed15dd0907294731d1e8ca96eed35307)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFollowGaeApplication")
    def reset_follow_gae_application(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFollowGaeApplication", []))

    @jsii.member(jsii_name="resetSecondaryZone")
    def reset_secondary_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryZone", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="followGaeApplicationInput")
    def follow_gae_application_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "followGaeApplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryZoneInput")
    def secondary_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="followGaeApplication")
    def follow_gae_application(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "followGaeApplication"))

    @follow_gae_application.setter
    def follow_gae_application(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57496a367a1444935eeb76467eb6486016f65ac9edacc97da96da88ae0f91ac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "followGaeApplication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryZone")
    def secondary_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryZone"))

    @secondary_zone.setter
    def secondary_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b2f9daa70d93cde44da4bdbab9b30c51cf002c3e34c291693a51eccd215634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3286d752d3445519df7214c3b7b3fe69aa41ba769bfb0620e1e7e57f47b240f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsLocationPreference]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsLocationPreference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsLocationPreference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382281fd496170e1eda9f30621bb7937cbd60d33ff9be1a5f4e30ca4d18f2cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "hour": "hour", "update_track": "updateTrack"},
)
class GoogleSqlDatabaseInstanceSettingsMaintenanceWindow:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        hour: typing.Optional[jsii.Number] = None,
        update_track: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param day: Day of week (1-7), starting on Monday. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#day GoogleSqlDatabaseInstance#day}
        :param hour: Hour of day (0-23), ignored if day not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#hour GoogleSqlDatabaseInstance#hour}
        :param update_track: Receive updates after one week (canary) or after two weeks (stable) or after five weeks (week5) of notification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#update_track GoogleSqlDatabaseInstance#update_track}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d3338694a3ab5463f50bc16dbced5f8f8096926b1e445c0c88ab22d00177c4)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument update_track", value=update_track, expected_type=type_hints["update_track"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if hour is not None:
            self._values["hour"] = hour
        if update_track is not None:
            self._values["update_track"] = update_track

    @builtins.property
    def day(self) -> typing.Optional[jsii.Number]:
        '''Day of week (1-7), starting on Monday.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#day GoogleSqlDatabaseInstance#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hour(self) -> typing.Optional[jsii.Number]:
        '''Hour of day (0-23), ignored if day not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#hour GoogleSqlDatabaseInstance#hour}
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def update_track(self) -> typing.Optional[builtins.str]:
        '''Receive updates after one week (canary) or after two weeks (stable) or after five weeks (week5) of notification.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#update_track GoogleSqlDatabaseInstance#update_track}
        '''
        result = self._values.get("update_track")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b30bb8c026c4c158c5ef2652efa3c3fc7f5cd82f1abcd16bd97ed6a6063966d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDay")
    def reset_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDay", []))

    @jsii.member(jsii_name="resetHour")
    def reset_hour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHour", []))

    @jsii.member(jsii_name="resetUpdateTrack")
    def reset_update_track(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateTrack", []))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="hourInput")
    def hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourInput"))

    @builtins.property
    @jsii.member(jsii_name="updateTrackInput")
    def update_track_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateTrackInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39701518be00a6540cf644e1b461e6386ec3931e61d21844c2d3c52303b847c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hour")
    def hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hour"))

    @hour.setter
    def hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8aa64507f84b06e34bfc14f7d18cfb3da0bc9b1ada55c4c296874dbb8df597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateTrack")
    def update_track(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTrack"))

    @update_track.setter
    def update_track(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7297512926c514237720692d7f85278b82b4c8096950cd9cc711f4c3031df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateTrack", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsMaintenanceWindow]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd7a364a75a9d38e4199c33954faba6ddb2558bb363682941fef3dde4c08f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleSqlDatabaseInstanceSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35afc479ec1a1fa9cd96c1e7da82f1aa246f71f2494110506722cce892e70a6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveDirectoryConfig")
    def put_active_directory_config(self, *, domain: builtins.str) -> None:
        '''
        :param domain: Domain name of the Active Directory for SQL Server (e.g., mydomain.com). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#domain GoogleSqlDatabaseInstance#domain}
        '''
        value = GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig(domain=domain)

        return typing.cast(None, jsii.invoke(self, "putActiveDirectoryConfig", [value]))

    @jsii.member(jsii_name="putAdvancedMachineFeatures")
    def put_advanced_machine_features(
        self,
        *,
        threads_per_core: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param threads_per_core: The number of threads per physical core. Can be 1 or 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#threads_per_core GoogleSqlDatabaseInstance#threads_per_core}
        '''
        value = GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures(
            threads_per_core=threads_per_core
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedMachineFeatures", [value]))

    @jsii.member(jsii_name="putBackupConfiguration")
    def put_backup_configuration(
        self,
        *,
        backup_retention_settings: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        binary_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        start_time: typing.Optional[builtins.str] = None,
        transaction_log_retention_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_retention_settings: backup_retention_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#backup_retention_settings GoogleSqlDatabaseInstance#backup_retention_settings}
        :param binary_log_enabled: True if binary logging is enabled. If settings.backup_configuration.enabled is false, this must be as well. Can only be used with MySQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#binary_log_enabled GoogleSqlDatabaseInstance#binary_log_enabled}
        :param enabled: True if backup configuration is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enabled GoogleSqlDatabaseInstance#enabled}
        :param location: Location of the backup configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#location GoogleSqlDatabaseInstance#location}
        :param point_in_time_recovery_enabled: True if Point-in-time recovery is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#point_in_time_recovery_enabled GoogleSqlDatabaseInstance#point_in_time_recovery_enabled}
        :param start_time: HH:MM format time indicating when backup configuration starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#start_time GoogleSqlDatabaseInstance#start_time}
        :param transaction_log_retention_days: The number of days of transaction logs we retain for point in time restore, from 1-7. (For PostgreSQL Enterprise Plus instances, from 1 to 35.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#transaction_log_retention_days GoogleSqlDatabaseInstance#transaction_log_retention_days}
        '''
        value = GoogleSqlDatabaseInstanceSettingsBackupConfiguration(
            backup_retention_settings=backup_retention_settings,
            binary_log_enabled=binary_log_enabled,
            enabled=enabled,
            location=location,
            point_in_time_recovery_enabled=point_in_time_recovery_enabled,
            start_time=start_time,
            transaction_log_retention_days=transaction_log_retention_days,
        )

        return typing.cast(None, jsii.invoke(self, "putBackupConfiguration", [value]))

    @jsii.member(jsii_name="putConnectionPoolConfig")
    def put_connection_pool_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ca688a88e867011cf40301ff5203ab531ab3af57d56356ee0212c3c533c2ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnectionPoolConfig", [value]))

    @jsii.member(jsii_name="putDatabaseFlags")
    def put_database_flags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsDatabaseFlags, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fedc97331e13d8db49f1d61b26dba7fc82d97a7fd334d13decbf4958b03774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDatabaseFlags", [value]))

    @jsii.member(jsii_name="putDataCacheConfig")
    def put_data_cache_config(
        self,
        *,
        data_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param data_cache_enabled: Whether data cache is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#data_cache_enabled GoogleSqlDatabaseInstance#data_cache_enabled}
        '''
        value = GoogleSqlDatabaseInstanceSettingsDataCacheConfig(
            data_cache_enabled=data_cache_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putDataCacheConfig", [value]))

    @jsii.member(jsii_name="putDenyMaintenancePeriod")
    def put_deny_maintenance_period(
        self,
        *,
        end_date: builtins.str,
        start_date: builtins.str,
        time: builtins.str,
    ) -> None:
        '''
        :param end_date: End date before which maintenance will not take place. The date is in format yyyy-mm-dd i.e., 2020-11-01, or mm-dd, i.e., 11-01 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#end_date GoogleSqlDatabaseInstance#end_date}
        :param start_date: Start date after which maintenance will not take place. The date is in format yyyy-mm-dd i.e., 2020-11-01, or mm-dd, i.e., 11-01 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#start_date GoogleSqlDatabaseInstance#start_date}
        :param time: Time in UTC when the "deny maintenance period" starts on start_date and ends on end_date. The time is in format: HH:mm:SS, i.e., 00:00:00 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#time GoogleSqlDatabaseInstance#time}
        '''
        value = GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod(
            end_date=end_date, start_date=start_date, time=time
        )

        return typing.cast(None, jsii.invoke(self, "putDenyMaintenancePeriod", [value]))

    @jsii.member(jsii_name="putInsightsConfig")
    def put_insights_config(
        self,
        *,
        query_insights_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_plans_per_minute: typing.Optional[jsii.Number] = None,
        query_string_length: typing.Optional[jsii.Number] = None,
        record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param query_insights_enabled: True if Query Insights feature is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#query_insights_enabled GoogleSqlDatabaseInstance#query_insights_enabled}
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. Between 0 and 20. Default to 5. For Enterprise Plus instances, from 0 to 200. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#query_plans_per_minute GoogleSqlDatabaseInstance#query_plans_per_minute}
        :param query_string_length: Maximum query length stored in bytes. Between 256 and 4500. Default to 1024. For Enterprise Plus instances, from 1 to 1048576. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#query_string_length GoogleSqlDatabaseInstance#query_string_length}
        :param record_application_tags: True if Query Insights will record application tags from query when enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#record_application_tags GoogleSqlDatabaseInstance#record_application_tags}
        :param record_client_address: True if Query Insights will record client address when enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#record_client_address GoogleSqlDatabaseInstance#record_client_address}
        '''
        value = GoogleSqlDatabaseInstanceSettingsInsightsConfig(
            query_insights_enabled=query_insights_enabled,
            query_plans_per_minute=query_plans_per_minute,
            query_string_length=query_string_length,
            record_application_tags=record_application_tags,
            record_client_address=record_client_address,
        )

        return typing.cast(None, jsii.invoke(self, "putInsightsConfig", [value]))

    @jsii.member(jsii_name="putIpConfiguration")
    def put_ip_configuration(
        self,
        *,
        allocated_ip_range: typing.Optional[builtins.str] = None,
        authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_private_path_for_google_cloud_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ipv4_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_network: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
        server_ca_mode: typing.Optional[builtins.str] = None,
        server_ca_pool: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocated_ip_range: The name of the allocated ip range for the private ip CloudSQL instance. For example: "google-managed-services-default". If set, the instance ip will be created in the allocated range. The range name must comply with RFC 1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#allocated_ip_range GoogleSqlDatabaseInstance#allocated_ip_range}
        :param authorized_networks: authorized_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#authorized_networks GoogleSqlDatabaseInstance#authorized_networks}
        :param custom_subject_alternative_names: The custom subject alternative names for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#custom_subject_alternative_names GoogleSqlDatabaseInstance#custom_subject_alternative_names}
        :param enable_private_path_for_google_cloud_services: Whether Google Cloud services such as BigQuery are allowed to access data in this Cloud SQL instance over a private IP connection. SQLSERVER database type is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_private_path_for_google_cloud_services GoogleSqlDatabaseInstance#enable_private_path_for_google_cloud_services}
        :param ipv4_enabled: Whether this Cloud SQL instance should be assigned a public IPV4 address. At least ipv4_enabled must be enabled or a private_network must be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ipv4_enabled GoogleSqlDatabaseInstance#ipv4_enabled}
        :param private_network: The VPC network from which the Cloud SQL instance is accessible for private IP. For example, projects/myProject/global/networks/default. Specifying a network enables private IP. At least ipv4_enabled must be enabled or a private_network must be configured. This setting can be updated, but it cannot be removed after it is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#private_network GoogleSqlDatabaseInstance#private_network}
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#psc_config GoogleSqlDatabaseInstance#psc_config}
        :param server_ca_mode: Specify how the server certificate's Certificate Authority is hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#server_ca_mode GoogleSqlDatabaseInstance#server_ca_mode}
        :param server_ca_pool: The resource name of the server CA pool for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#server_ca_pool GoogleSqlDatabaseInstance#server_ca_pool}
        :param ssl_mode: Specify how SSL connection should be enforced in DB connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#ssl_mode GoogleSqlDatabaseInstance#ssl_mode}
        '''
        value = GoogleSqlDatabaseInstanceSettingsIpConfiguration(
            allocated_ip_range=allocated_ip_range,
            authorized_networks=authorized_networks,
            custom_subject_alternative_names=custom_subject_alternative_names,
            enable_private_path_for_google_cloud_services=enable_private_path_for_google_cloud_services,
            ipv4_enabled=ipv4_enabled,
            private_network=private_network,
            psc_config=psc_config,
            server_ca_mode=server_ca_mode,
            server_ca_pool=server_ca_pool,
            ssl_mode=ssl_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putIpConfiguration", [value]))

    @jsii.member(jsii_name="putLocationPreference")
    def put_location_preference(
        self,
        *,
        follow_gae_application: typing.Optional[builtins.str] = None,
        secondary_zone: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param follow_gae_application: A Google App Engine application whose zone to remain in. Must be in the same region as this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#follow_gae_application GoogleSqlDatabaseInstance#follow_gae_application}
        :param secondary_zone: The preferred Compute Engine zone for the secondary/failover. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#secondary_zone GoogleSqlDatabaseInstance#secondary_zone}
        :param zone: The preferred compute engine zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#zone GoogleSqlDatabaseInstance#zone}
        '''
        value = GoogleSqlDatabaseInstanceSettingsLocationPreference(
            follow_gae_application=follow_gae_application,
            secondary_zone=secondary_zone,
            zone=zone,
        )

        return typing.cast(None, jsii.invoke(self, "putLocationPreference", [value]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        hour: typing.Optional[jsii.Number] = None,
        update_track: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param day: Day of week (1-7), starting on Monday. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#day GoogleSqlDatabaseInstance#day}
        :param hour: Hour of day (0-23), ignored if day not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#hour GoogleSqlDatabaseInstance#hour}
        :param update_track: Receive updates after one week (canary) or after two weeks (stable) or after five weeks (week5) of notification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#update_track GoogleSqlDatabaseInstance#update_track}
        '''
        value = GoogleSqlDatabaseInstanceSettingsMaintenanceWindow(
            day=day, hour=hour, update_track=update_track
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="putPasswordValidationPolicy")
    def put_password_validation_policy(
        self,
        *,
        enable_password_policy: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        complexity: typing.Optional[builtins.str] = None,
        disallow_username_substring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        min_length: typing.Optional[jsii.Number] = None,
        password_change_interval: typing.Optional[builtins.str] = None,
        reuse_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable_password_policy: Whether the password policy is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_password_policy GoogleSqlDatabaseInstance#enable_password_policy}
        :param complexity: Password complexity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#complexity GoogleSqlDatabaseInstance#complexity}
        :param disallow_username_substring: Disallow username as a part of the password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disallow_username_substring GoogleSqlDatabaseInstance#disallow_username_substring}
        :param min_length: Minimum number of characters allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#min_length GoogleSqlDatabaseInstance#min_length}
        :param password_change_interval: Minimum interval after which the password can be changed. This flag is only supported for PostgresSQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#password_change_interval GoogleSqlDatabaseInstance#password_change_interval}
        :param reuse_interval: Number of previous passwords that cannot be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#reuse_interval GoogleSqlDatabaseInstance#reuse_interval}
        '''
        value = GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy(
            enable_password_policy=enable_password_policy,
            complexity=complexity,
            disallow_username_substring=disallow_username_substring,
            min_length=min_length,
            password_change_interval=password_change_interval,
            reuse_interval=reuse_interval,
        )

        return typing.cast(None, jsii.invoke(self, "putPasswordValidationPolicy", [value]))

    @jsii.member(jsii_name="putSqlServerAuditConfig")
    def put_sql_server_audit_config(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        retention_interval: typing.Optional[builtins.str] = None,
        upload_interval: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The name of the destination bucket (e.g., gs://mybucket). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#bucket GoogleSqlDatabaseInstance#bucket}
        :param retention_interval: How long to keep generated audit files. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retention_interval GoogleSqlDatabaseInstance#retention_interval}
        :param upload_interval: How often to upload generated audit files. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#upload_interval GoogleSqlDatabaseInstance#upload_interval}
        '''
        value = GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig(
            bucket=bucket,
            retention_interval=retention_interval,
            upload_interval=upload_interval,
        )

        return typing.cast(None, jsii.invoke(self, "putSqlServerAuditConfig", [value]))

    @jsii.member(jsii_name="resetActivationPolicy")
    def reset_activation_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActivationPolicy", []))

    @jsii.member(jsii_name="resetActiveDirectoryConfig")
    def reset_active_directory_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectoryConfig", []))

    @jsii.member(jsii_name="resetAdvancedMachineFeatures")
    def reset_advanced_machine_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedMachineFeatures", []))

    @jsii.member(jsii_name="resetAvailabilityType")
    def reset_availability_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityType", []))

    @jsii.member(jsii_name="resetBackupConfiguration")
    def reset_backup_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupConfiguration", []))

    @jsii.member(jsii_name="resetCollation")
    def reset_collation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollation", []))

    @jsii.member(jsii_name="resetConnectionPoolConfig")
    def reset_connection_pool_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionPoolConfig", []))

    @jsii.member(jsii_name="resetConnectorEnforcement")
    def reset_connector_enforcement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectorEnforcement", []))

    @jsii.member(jsii_name="resetDatabaseFlags")
    def reset_database_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseFlags", []))

    @jsii.member(jsii_name="resetDataCacheConfig")
    def reset_data_cache_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCacheConfig", []))

    @jsii.member(jsii_name="resetDataDiskProvisionedIops")
    def reset_data_disk_provisioned_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDiskProvisionedIops", []))

    @jsii.member(jsii_name="resetDataDiskProvisionedThroughput")
    def reset_data_disk_provisioned_throughput(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDiskProvisionedThroughput", []))

    @jsii.member(jsii_name="resetDeletionProtectionEnabled")
    def reset_deletion_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtectionEnabled", []))

    @jsii.member(jsii_name="resetDenyMaintenancePeriod")
    def reset_deny_maintenance_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyMaintenancePeriod", []))

    @jsii.member(jsii_name="resetDiskAutoresize")
    def reset_disk_autoresize(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskAutoresize", []))

    @jsii.member(jsii_name="resetDiskAutoresizeLimit")
    def reset_disk_autoresize_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskAutoresizeLimit", []))

    @jsii.member(jsii_name="resetDiskSize")
    def reset_disk_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSize", []))

    @jsii.member(jsii_name="resetDiskType")
    def reset_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskType", []))

    @jsii.member(jsii_name="resetEdition")
    def reset_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdition", []))

    @jsii.member(jsii_name="resetEnableDataplexIntegration")
    def reset_enable_dataplex_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDataplexIntegration", []))

    @jsii.member(jsii_name="resetEnableGoogleMlIntegration")
    def reset_enable_google_ml_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableGoogleMlIntegration", []))

    @jsii.member(jsii_name="resetInsightsConfig")
    def reset_insights_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsightsConfig", []))

    @jsii.member(jsii_name="resetIpConfiguration")
    def reset_ip_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpConfiguration", []))

    @jsii.member(jsii_name="resetLocationPreference")
    def reset_location_preference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationPreference", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetPasswordValidationPolicy")
    def reset_password_validation_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordValidationPolicy", []))

    @jsii.member(jsii_name="resetPricingPlan")
    def reset_pricing_plan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPricingPlan", []))

    @jsii.member(jsii_name="resetRetainBackupsOnDelete")
    def reset_retain_backups_on_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainBackupsOnDelete", []))

    @jsii.member(jsii_name="resetSqlServerAuditConfig")
    def reset_sql_server_audit_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlServerAuditConfig", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @jsii.member(jsii_name="resetUserLabels")
    def reset_user_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserLabels", []))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryConfig")
    def active_directory_config(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfigOutputReference:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfigOutputReference, jsii.get(self, "activeDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedMachineFeatures")
    def advanced_machine_features(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeaturesOutputReference:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeaturesOutputReference, jsii.get(self, "advancedMachineFeatures"))

    @builtins.property
    @jsii.member(jsii_name="backupConfiguration")
    def backup_configuration(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsBackupConfigurationOutputReference:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsBackupConfigurationOutputReference, jsii.get(self, "backupConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="connectionPoolConfig")
    def connection_pool_config(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigList:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigList, jsii.get(self, "connectionPoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="databaseFlags")
    def database_flags(self) -> GoogleSqlDatabaseInstanceSettingsDatabaseFlagsList:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsDatabaseFlagsList, jsii.get(self, "databaseFlags"))

    @builtins.property
    @jsii.member(jsii_name="dataCacheConfig")
    def data_cache_config(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsDataCacheConfigOutputReference:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsDataCacheConfigOutputReference, jsii.get(self, "dataCacheConfig"))

    @builtins.property
    @jsii.member(jsii_name="denyMaintenancePeriod")
    def deny_maintenance_period(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriodOutputReference:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriodOutputReference, jsii.get(self, "denyMaintenancePeriod"))

    @builtins.property
    @jsii.member(jsii_name="insightsConfig")
    def insights_config(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsInsightsConfigOutputReference:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsInsightsConfigOutputReference, jsii.get(self, "insightsConfig"))

    @builtins.property
    @jsii.member(jsii_name="ipConfiguration")
    def ip_configuration(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsIpConfigurationOutputReference:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsIpConfigurationOutputReference, jsii.get(self, "ipConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="locationPreference")
    def location_preference(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsLocationPreferenceOutputReference:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsLocationPreferenceOutputReference, jsii.get(self, "locationPreference"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> GoogleSqlDatabaseInstanceSettingsMaintenanceWindowOutputReference:
        return typing.cast(GoogleSqlDatabaseInstanceSettingsMaintenanceWindowOutputReference, jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="passwordValidationPolicy")
    def password_validation_policy(
        self,
    ) -> "GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicyOutputReference":
        return typing.cast("GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicyOutputReference", jsii.get(self, "passwordValidationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="sqlServerAuditConfig")
    def sql_server_audit_config(
        self,
    ) -> "GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfigOutputReference":
        return typing.cast("GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfigOutputReference", jsii.get(self, "sqlServerAuditConfig"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="activationPolicyInput")
    def activation_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryConfigInput")
    def active_directory_config_input(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig], jsii.get(self, "activeDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedMachineFeaturesInput")
    def advanced_machine_features_input(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures], jsii.get(self, "advancedMachineFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityTypeInput")
    def availability_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="backupConfigurationInput")
    def backup_configuration_input(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfiguration]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfiguration], jsii.get(self, "backupConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="collationInput")
    def collation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collationInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionPoolConfigInput")
    def connection_pool_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig]]], jsii.get(self, "connectionPoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorEnforcementInput")
    def connector_enforcement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorEnforcementInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseFlagsInput")
    def database_flags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsDatabaseFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsDatabaseFlags]]], jsii.get(self, "databaseFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCacheConfigInput")
    def data_cache_config_input(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsDataCacheConfig]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsDataCacheConfig], jsii.get(self, "dataCacheConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskProvisionedIopsInput")
    def data_disk_provisioned_iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataDiskProvisionedIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskProvisionedThroughputInput")
    def data_disk_provisioned_throughput_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataDiskProvisionedThroughputInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionEnabledInput")
    def deletion_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="denyMaintenancePeriodInput")
    def deny_maintenance_period_input(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod], jsii.get(self, "denyMaintenancePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="diskAutoresizeInput")
    def disk_autoresize_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "diskAutoresizeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskAutoresizeLimitInput")
    def disk_autoresize_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskAutoresizeLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeInput")
    def disk_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="editionInput")
    def edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableDataplexIntegrationInput")
    def enable_dataplex_integration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableDataplexIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableGoogleMlIntegrationInput")
    def enable_google_ml_integration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableGoogleMlIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsConfigInput")
    def insights_config_input(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsInsightsConfig]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsInsightsConfig], jsii.get(self, "insightsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsIpConfiguration]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsIpConfiguration], jsii.get(self, "ipConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="locationPreferenceInput")
    def location_preference_input(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsLocationPreference]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsLocationPreference], jsii.get(self, "locationPreferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsMaintenanceWindow]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsMaintenanceWindow], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordValidationPolicyInput")
    def password_validation_policy_input(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy"]:
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy"], jsii.get(self, "passwordValidationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="pricingPlanInput")
    def pricing_plan_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pricingPlanInput"))

    @builtins.property
    @jsii.member(jsii_name="retainBackupsOnDeleteInput")
    def retain_backups_on_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retainBackupsOnDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlServerAuditConfigInput")
    def sql_server_audit_config_input(
        self,
    ) -> typing.Optional["GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig"]:
        return typing.cast(typing.Optional["GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig"], jsii.get(self, "sqlServerAuditConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="userLabelsInput")
    def user_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "userLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="activationPolicy")
    def activation_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activationPolicy"))

    @activation_policy.setter
    def activation_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d555ab686be6af40997b1cc6c1f19fb1941128e9ee25b2261bb491aaf2545d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityType")
    def availability_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityType"))

    @availability_type.setter
    def availability_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402ea70c8f77fdcef0c21f4f37d3a45720e72094bacddb0739a62ed0968f60e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collation")
    def collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collation"))

    @collation.setter
    def collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ebff72a8bece43139a6841ca39120b8846eba7c9a6828cf3c32cb8f72b54d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorEnforcement")
    def connector_enforcement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorEnforcement"))

    @connector_enforcement.setter
    def connector_enforcement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c22ad20b1335f9839763108bda870474be676356e2ea1d71ded3c9bd34c7f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDiskProvisionedIops")
    def data_disk_provisioned_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataDiskProvisionedIops"))

    @data_disk_provisioned_iops.setter
    def data_disk_provisioned_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80fedaaf9f847eb4750b2047c20e81438c0df0823d772fc80831d01d9a16321d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDiskProvisionedIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDiskProvisionedThroughput")
    def data_disk_provisioned_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataDiskProvisionedThroughput"))

    @data_disk_provisioned_throughput.setter
    def data_disk_provisioned_throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc8ddec72e3bf253b60c1faf73c3fee54823f587ec2c58c7447cc626367af4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDiskProvisionedThroughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionEnabled")
    def deletion_protection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtectionEnabled"))

    @deletion_protection_enabled.setter
    def deletion_protection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecbec54f29cef253cf5de81288d214fd3aefe0da67c57febaa303dfd37638507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskAutoresize")
    def disk_autoresize(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "diskAutoresize"))

    @disk_autoresize.setter
    def disk_autoresize(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd814771282532c6e4674bb5844db41850f9aeac22dc1a0ecaa1e0fc5610759c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskAutoresize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskAutoresizeLimit")
    def disk_autoresize_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskAutoresizeLimit"))

    @disk_autoresize_limit.setter
    def disk_autoresize_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f2f2925a1bef97e1c7cfd8e365f62d4469d12b668944543ded2b307e404621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskAutoresizeLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSize")
    def disk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSize"))

    @disk_size.setter
    def disk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de713b27a6e47ec4f1380eafb62c82e32e195871b274d6fe7a4af3e14d732358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad948fbf3551734f0cf945524746e58bc4869076a5f594f280e1c5b36e5c0aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7523cb9076cf478bbd21cfb21f143da77f508cee4a1771160ef0164c2610e90f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableDataplexIntegration")
    def enable_dataplex_integration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableDataplexIntegration"))

    @enable_dataplex_integration.setter
    def enable_dataplex_integration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06036297daed5400d0ac6509076d869bcccf0e201e5b37db3129c14ad14c2495)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDataplexIntegration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableGoogleMlIntegration")
    def enable_google_ml_integration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableGoogleMlIntegration"))

    @enable_google_ml_integration.setter
    def enable_google_ml_integration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2590ba95ecb6e1f30223514a077e63b47745c090e1bc637cd576841ed233ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableGoogleMlIntegration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pricingPlan")
    def pricing_plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pricingPlan"))

    @pricing_plan.setter
    def pricing_plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67eb80287a8fc3b16014d31a62bec3d9af82e958e85cfad40fc1490a8253697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pricingPlan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retainBackupsOnDelete")
    def retain_backups_on_delete(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retainBackupsOnDelete"))

    @retain_backups_on_delete.setter
    def retain_backups_on_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153e8c0feb6f8467b836c585c1de509cfd6d2596b0a9ac0190c514d55e514e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainBackupsOnDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c8a4bd6323ef28634f5665ab852377564ac54e4cd7f2cc31bc5a66159f72e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e589112e3f163c1e332c5f612f4eb8a17d81af743142595ab9795a2531806c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userLabels")
    def user_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "userLabels"))

    @user_labels.setter
    def user_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b1ea6f98b63e1e348035d88af011df253e43fd7c3923057e4057208bbbaae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleSqlDatabaseInstanceSettings]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c9aa21c894b5fb0d3bab8161773fb31559aa2dea84c92aaa3b4df215d66b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "enable_password_policy": "enablePasswordPolicy",
        "complexity": "complexity",
        "disallow_username_substring": "disallowUsernameSubstring",
        "min_length": "minLength",
        "password_change_interval": "passwordChangeInterval",
        "reuse_interval": "reuseInterval",
    },
)
class GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy:
    def __init__(
        self,
        *,
        enable_password_policy: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        complexity: typing.Optional[builtins.str] = None,
        disallow_username_substring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        min_length: typing.Optional[jsii.Number] = None,
        password_change_interval: typing.Optional[builtins.str] = None,
        reuse_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable_password_policy: Whether the password policy is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_password_policy GoogleSqlDatabaseInstance#enable_password_policy}
        :param complexity: Password complexity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#complexity GoogleSqlDatabaseInstance#complexity}
        :param disallow_username_substring: Disallow username as a part of the password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disallow_username_substring GoogleSqlDatabaseInstance#disallow_username_substring}
        :param min_length: Minimum number of characters allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#min_length GoogleSqlDatabaseInstance#min_length}
        :param password_change_interval: Minimum interval after which the password can be changed. This flag is only supported for PostgresSQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#password_change_interval GoogleSqlDatabaseInstance#password_change_interval}
        :param reuse_interval: Number of previous passwords that cannot be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#reuse_interval GoogleSqlDatabaseInstance#reuse_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b683ba5a541e198af03b2bdd79eea5e48f780c5754e42e38c5487bc1e96323)
            check_type(argname="argument enable_password_policy", value=enable_password_policy, expected_type=type_hints["enable_password_policy"])
            check_type(argname="argument complexity", value=complexity, expected_type=type_hints["complexity"])
            check_type(argname="argument disallow_username_substring", value=disallow_username_substring, expected_type=type_hints["disallow_username_substring"])
            check_type(argname="argument min_length", value=min_length, expected_type=type_hints["min_length"])
            check_type(argname="argument password_change_interval", value=password_change_interval, expected_type=type_hints["password_change_interval"])
            check_type(argname="argument reuse_interval", value=reuse_interval, expected_type=type_hints["reuse_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_password_policy": enable_password_policy,
        }
        if complexity is not None:
            self._values["complexity"] = complexity
        if disallow_username_substring is not None:
            self._values["disallow_username_substring"] = disallow_username_substring
        if min_length is not None:
            self._values["min_length"] = min_length
        if password_change_interval is not None:
            self._values["password_change_interval"] = password_change_interval
        if reuse_interval is not None:
            self._values["reuse_interval"] = reuse_interval

    @builtins.property
    def enable_password_policy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the password policy is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#enable_password_policy GoogleSqlDatabaseInstance#enable_password_policy}
        '''
        result = self._values.get("enable_password_policy")
        assert result is not None, "Required property 'enable_password_policy' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def complexity(self) -> typing.Optional[builtins.str]:
        '''Password complexity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#complexity GoogleSqlDatabaseInstance#complexity}
        '''
        result = self._values.get("complexity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disallow_username_substring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disallow username as a part of the password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#disallow_username_substring GoogleSqlDatabaseInstance#disallow_username_substring}
        '''
        result = self._values.get("disallow_username_substring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of characters allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#min_length GoogleSqlDatabaseInstance#min_length}
        '''
        result = self._values.get("min_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_change_interval(self) -> typing.Optional[builtins.str]:
        '''Minimum interval after which the password can be changed. This flag is only supported for PostgresSQL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#password_change_interval GoogleSqlDatabaseInstance#password_change_interval}
        '''
        result = self._values.get("password_change_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reuse_interval(self) -> typing.Optional[jsii.Number]:
        '''Number of previous passwords that cannot be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#reuse_interval GoogleSqlDatabaseInstance#reuse_interval}
        '''
        result = self._values.get("reuse_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdd8b888bb14703479b410c908a6d035d798c342a04f5865dfb6b4853d6c8141)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComplexity")
    def reset_complexity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComplexity", []))

    @jsii.member(jsii_name="resetDisallowUsernameSubstring")
    def reset_disallow_username_substring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisallowUsernameSubstring", []))

    @jsii.member(jsii_name="resetMinLength")
    def reset_min_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLength", []))

    @jsii.member(jsii_name="resetPasswordChangeInterval")
    def reset_password_change_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordChangeInterval", []))

    @jsii.member(jsii_name="resetReuseInterval")
    def reset_reuse_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReuseInterval", []))

    @builtins.property
    @jsii.member(jsii_name="complexityInput")
    def complexity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "complexityInput"))

    @builtins.property
    @jsii.member(jsii_name="disallowUsernameSubstringInput")
    def disallow_username_substring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disallowUsernameSubstringInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePasswordPolicyInput")
    def enable_password_policy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePasswordPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="minLengthInput")
    def min_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordChangeIntervalInput")
    def password_change_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordChangeIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="reuseIntervalInput")
    def reuse_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "reuseIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="complexity")
    def complexity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "complexity"))

    @complexity.setter
    def complexity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75aaf56e0b5ea7a464e4e9800a79f92c4c3df7745b4c2d1d8a80c811001213ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "complexity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disallowUsernameSubstring")
    def disallow_username_substring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disallowUsernameSubstring"))

    @disallow_username_substring.setter
    def disallow_username_substring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93018b3011d9e0d0e661279de20b5834264425d71a719630979773b9bfbcc725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disallowUsernameSubstring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePasswordPolicy")
    def enable_password_policy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePasswordPolicy"))

    @enable_password_policy.setter
    def enable_password_policy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88d35f06b6aa41c673bed481da907bfb6e4e02849b06ab2940c22003fd7553b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePasswordPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minLength")
    def min_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLength"))

    @min_length.setter
    def min_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2ef43ccb214bd5cb74e876b557b4b8c8bf4b1b933da54186562f70359b9f82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordChangeInterval")
    def password_change_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordChangeInterval"))

    @password_change_interval.setter
    def password_change_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61133f871e5b9f6b486b4deb0f6922c97960e080988035cae2a74f0591f8ce33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordChangeInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reuseInterval")
    def reuse_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reuseInterval"))

    @reuse_interval.setter
    def reuse_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082b6592e50350a212c766b1d179dc2d5817507eae5265bf1a5a816d8ac66279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reuseInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7a582cc8b51b9ae7a2e35add2c93cb6b4fa8900e05c3d83139bb540915f4cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "retention_interval": "retentionInterval",
        "upload_interval": "uploadInterval",
    },
)
class GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        retention_interval: typing.Optional[builtins.str] = None,
        upload_interval: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The name of the destination bucket (e.g., gs://mybucket). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#bucket GoogleSqlDatabaseInstance#bucket}
        :param retention_interval: How long to keep generated audit files. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retention_interval GoogleSqlDatabaseInstance#retention_interval}
        :param upload_interval: How often to upload generated audit files. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#upload_interval GoogleSqlDatabaseInstance#upload_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9502db5c2d40b20eec14fefb180f4da517a23314a946ed5155a9636277d47ed)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument retention_interval", value=retention_interval, expected_type=type_hints["retention_interval"])
            check_type(argname="argument upload_interval", value=upload_interval, expected_type=type_hints["upload_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if retention_interval is not None:
            self._values["retention_interval"] = retention_interval
        if upload_interval is not None:
            self._values["upload_interval"] = upload_interval

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''The name of the destination bucket (e.g., gs://mybucket).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#bucket GoogleSqlDatabaseInstance#bucket}
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_interval(self) -> typing.Optional[builtins.str]:
        '''How long to keep generated audit files.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s"..

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#retention_interval GoogleSqlDatabaseInstance#retention_interval}
        '''
        result = self._values.get("retention_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upload_interval(self) -> typing.Optional[builtins.str]:
        '''How often to upload generated audit files.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#upload_interval GoogleSqlDatabaseInstance#upload_interval}
        '''
        result = self._values.get("upload_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df5307c85a88a275e70860e678f401c2c948e034766f5bd4b158ec1cb924e0a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetRetentionInterval")
    def reset_retention_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionInterval", []))

    @jsii.member(jsii_name="resetUploadInterval")
    def reset_upload_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUploadInterval", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionIntervalInput")
    def retention_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="uploadIntervalInput")
    def upload_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uploadIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474379f127d605458171ba081db7fc2409c322f15ea7642c0ab264c3d21c99a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionInterval")
    def retention_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionInterval"))

    @retention_interval.setter
    def retention_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01409b39f985d5954f24500da9bdd512f84ddfb4fbc6c481d7e14f47ced0c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uploadInterval")
    def upload_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uploadInterval"))

    @upload_interval.setter
    def upload_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a094f7d86169ac8bbad9e6969fc41e6a507f59240e90a9729dcf2a05d83749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uploadInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig]:
        return typing.cast(typing.Optional[GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f4af05960b1ad8d78f1fdc6fbb1ac223014d5863175645b056d86a42cbe95f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleSqlDatabaseInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#create GoogleSqlDatabaseInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#delete GoogleSqlDatabaseInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#update GoogleSqlDatabaseInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2d85ecc9917c9391a930469296153c134f7b2785d6a396845f8e0ee246d4ca)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#create GoogleSqlDatabaseInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#delete GoogleSqlDatabaseInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_sql_database_instance#update GoogleSqlDatabaseInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleSqlDatabaseInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleSqlDatabaseInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleSqlDatabaseInstance.GoogleSqlDatabaseInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66bcb9b8ba2278d46eb78c78f26e8a482037a695a1f6a315491710965a107f8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__165268a1030c987561af903f01340c48b3f894d92241d5751ae21c7e0a9f11d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea8832679cc342c8ae52e38ca60a014e662d2c6fa29662122f40b90fac1332f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb84195ec99c988b01e40c706f3586866619c66a13280e583ebbdd751f03fc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a23d507cb1dc8d20c18c7a7a3e8106f1c5ec99359d05d7e33e70c902a3f389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleSqlDatabaseInstance",
    "GoogleSqlDatabaseInstanceClone",
    "GoogleSqlDatabaseInstanceCloneOutputReference",
    "GoogleSqlDatabaseInstanceConfig",
    "GoogleSqlDatabaseInstanceDnsNames",
    "GoogleSqlDatabaseInstanceDnsNamesList",
    "GoogleSqlDatabaseInstanceDnsNamesOutputReference",
    "GoogleSqlDatabaseInstanceIpAddress",
    "GoogleSqlDatabaseInstanceIpAddressList",
    "GoogleSqlDatabaseInstanceIpAddressOutputReference",
    "GoogleSqlDatabaseInstanceReplicaConfiguration",
    "GoogleSqlDatabaseInstanceReplicaConfigurationOutputReference",
    "GoogleSqlDatabaseInstanceReplicationCluster",
    "GoogleSqlDatabaseInstanceReplicationClusterOutputReference",
    "GoogleSqlDatabaseInstanceRestoreBackupContext",
    "GoogleSqlDatabaseInstanceRestoreBackupContextOutputReference",
    "GoogleSqlDatabaseInstanceServerCaCert",
    "GoogleSqlDatabaseInstanceServerCaCertList",
    "GoogleSqlDatabaseInstanceServerCaCertOutputReference",
    "GoogleSqlDatabaseInstanceSettings",
    "GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig",
    "GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfigOutputReference",
    "GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures",
    "GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeaturesOutputReference",
    "GoogleSqlDatabaseInstanceSettingsBackupConfiguration",
    "GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings",
    "GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsOutputReference",
    "GoogleSqlDatabaseInstanceSettingsBackupConfigurationOutputReference",
    "GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig",
    "GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags",
    "GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlagsList",
    "GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlagsOutputReference",
    "GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigList",
    "GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigOutputReference",
    "GoogleSqlDatabaseInstanceSettingsDataCacheConfig",
    "GoogleSqlDatabaseInstanceSettingsDataCacheConfigOutputReference",
    "GoogleSqlDatabaseInstanceSettingsDatabaseFlags",
    "GoogleSqlDatabaseInstanceSettingsDatabaseFlagsList",
    "GoogleSqlDatabaseInstanceSettingsDatabaseFlagsOutputReference",
    "GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod",
    "GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriodOutputReference",
    "GoogleSqlDatabaseInstanceSettingsInsightsConfig",
    "GoogleSqlDatabaseInstanceSettingsInsightsConfigOutputReference",
    "GoogleSqlDatabaseInstanceSettingsIpConfiguration",
    "GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks",
    "GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksList",
    "GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksOutputReference",
    "GoogleSqlDatabaseInstanceSettingsIpConfigurationOutputReference",
    "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig",
    "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigList",
    "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigOutputReference",
    "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections",
    "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsList",
    "GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsOutputReference",
    "GoogleSqlDatabaseInstanceSettingsLocationPreference",
    "GoogleSqlDatabaseInstanceSettingsLocationPreferenceOutputReference",
    "GoogleSqlDatabaseInstanceSettingsMaintenanceWindow",
    "GoogleSqlDatabaseInstanceSettingsMaintenanceWindowOutputReference",
    "GoogleSqlDatabaseInstanceSettingsOutputReference",
    "GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy",
    "GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicyOutputReference",
    "GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig",
    "GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfigOutputReference",
    "GoogleSqlDatabaseInstanceTimeouts",
    "GoogleSqlDatabaseInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e899509fad3e295eeec4ad1acf568ea78d89ae489d1bab40609f928e23961cc6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database_version: builtins.str,
    clone: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceClone, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    maintenance_version: typing.Optional[builtins.str] = None,
    master_instance_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    replica_configuration: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceReplicaConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    replica_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_cluster: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceReplicationCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_backup_context: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceRestoreBackupContext, typing.Dict[builtins.str, typing.Any]]] = None,
    root_password: typing.Optional[builtins.str] = None,
    settings: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__909d35caf3c7f5bc530162938e81191314371cd1bf49c25ebd15664c7d7102f4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97bd8841a0bc8b6b2e8b29cb97ea506718041e265fc37db0d22cc791af5e0a6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28757ccd2f2286eff3d68b870e91438ab37d2ddab9c67895122733d1ec0d6e95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b80a8b8f7be7334447d990450a13be5d177ff474baec8eab6154e5ad7c2412(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8fc728ef822d600bcaebfe2a91288022efd15efc258ac48ee45aaac9d79b034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471ff664a275100ebd99d4d261a339e0150f410853cf84a09bc3321083b5431d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14faa228e8481d5eb6aa751257231da03263565df3d512b095c62d3791bbd65c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5a80968b156f251ec2d79c9e57ac68748260fa191b8aa3be7b792c0d9fe863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a896ad0611b13fec4cb579eec09f4273b1adcd9a32f98c4ae0262486198f059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e614cb31201f3d2e9df59789d530720ccb1c46b81a97ad0dbee2247df6c4d1fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335d5c6c5e72095db61523561a486a65032009bf7707b81d56c7f77e5d464993(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9223af3fa74e8ebd868c767d76773bb8a41a4b7cd6c489bd52fcd4127b934123(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d56178431b0659f1608e5c6d5b9414ad48956f427e7eab518b78180a42711d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb72ec89b07468d03692ede1c1993050e50bbfaf82709fe288def5b6c7791b64(
    *,
    source_instance_name: builtins.str,
    allocated_ip_range: typing.Optional[builtins.str] = None,
    database_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    point_in_time: typing.Optional[builtins.str] = None,
    preferred_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b33408fe8e0e2d8ad8961f57530fa0d4cac2b7b9747a0e85b33bb21e4400135(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d832cee65e214efc0da2bfaccc222ffa5eb3128d8e6ccacd7474a01e6c49e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f01793f12f7eb7516ac96d9cc7ae439f0798c168ca7755f0d50372cd6a7ade2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65a03add023eef2a6be962077b9396539d747b89471e067fbe286fd3b31df5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62777194aac4f9ff2399f715fda3f42308bd6ccddaea0b6adfb3954fc1c38566(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031eb9fdac094d61e74a9046ebd5a40875f13bdbbe9ede10ce00ac8de2bfa1b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaba4e8d945af02be17c676a4918be2c198d2d5a900a4c1549a2c81152eb08f5(
    value: typing.Optional[GoogleSqlDatabaseInstanceClone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f600e2ea121d674af9ff825e156fa89bda56ea9dc93cdb40aa28efd921cad84(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database_version: builtins.str,
    clone: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceClone, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    maintenance_version: typing.Optional[builtins.str] = None,
    master_instance_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    replica_configuration: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceReplicaConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    replica_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_cluster: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceReplicationCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_backup_context: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceRestoreBackupContext, typing.Dict[builtins.str, typing.Any]]] = None,
    root_password: typing.Optional[builtins.str] = None,
    settings: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375a444e845915d4b9f185406bd00dd56badb5196c12969a8e480bd5fdafd59b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2595eb5626312178374dd89745280bbb899d419294c3d2766c0f1ce7326b2b6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefbbbb642a64afdf7ed72be15d93233cca3cace62d3f747b20375fc21783891(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea01f53a9aa444d4983f7f19a073f67ec6d8cf74f90abf3e118b001d4f86bc6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a291a74e095fd76abfbd8dbeab0e0ef4dc52c9278836ed89c534d2890ce630(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7998ceca82e98aa57e157a01cda9320af207682a966b37d349bd42e1a81f118a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487f24a0af6e8e8d0b8bb49fb637dcef8556252a9287a9b83fa5146fe282d68f(
    value: typing.Optional[GoogleSqlDatabaseInstanceDnsNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61cee7fdded9fe7eb072a8d29ef7219da9e00152dd6bfd16d40994d476eec0ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638ef37e7f9581241e7dd933421b4f04751d477faf6fda8602e5d023e65c7abd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0761a3b49585813a346002907303ba2f3b15ee1ade9b4e047ad0949f52a60efb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a0c6348da5a8d4a6d7f36e2554e36e727cf71161f519713ce41511e95d6d03(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4a42463b9b8f9f20ee4f86125b13dbbeb602e52ab4cee9e0e30061108f5042(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6510c9f94aec1e8ea1eca20a0e4fe4401c2aa24b96170d8e2de2ce6cb2301c70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc98ee0dd6e252f33037f7a81d3e1409235a494d2c12e16f3ebba73fd63b715(
    value: typing.Optional[GoogleSqlDatabaseInstanceIpAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00cf683ec0cc9fd1eb613222734d1841c1fafba35a40f62e12144273e09d5a74(
    *,
    ca_certificate: typing.Optional[builtins.str] = None,
    cascadable_replica: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
    connect_retry_interval: typing.Optional[jsii.Number] = None,
    dump_file_path: typing.Optional[builtins.str] = None,
    failover_target: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    master_heartbeat_period: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    ssl_cipher: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
    verify_server_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f4fcfba219bc4a57271bec2b318a8102bd9dc0fb076a618bb8fafa9e233580(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652faf9a0725c40d7f66e8a8567742861de568c57c5c4d4815808a697c025392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2ccba4e603444ce457a24b245aef6057c8969727aec3aaf6ee46e433427758(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d858133e5dfe2d6f272c9b0667467054cf7cc80479635d0f24110b1d0ccc0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712cd2ca69324f881306e76482e97a907b9b2cdd27846465afb9a6d849677bce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7774f4d381364f81647166e8022017735e110b74dc106ab966086516b7ccc8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b50fc9b94bbe45b2d7fd250d2bbef151db43a4aad8455ffaf129dcb308c842(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0580952aee12a18509ce18cff482e23ae9874b382d57ebfc5f3e9c8b4fb3bcd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5229e54f30a31f2c8f1b7f3dc575ab0fff76916efe1ed11ca8097686de4e9ea8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75da1a53cb6fed6670250f654aebb52a14add73e3c485bd559d25d38f8517fe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded03b3733a73db0e22733ed4a499c92f034f3a28c19be5dd8e155347bed33d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60720d1c89ea82896a2adccd26d66ef1a5439e7af6c13487e9cca90fd1e600b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99593ce61863f5496755bc5ef88624a6009506371845d7297d8a4cd5e42575d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61386cfaeba901b7384924d5526548c4ccba3450ad5802f3e94747571d078d0a(
    value: typing.Optional[GoogleSqlDatabaseInstanceReplicaConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9cd3cf7941f5f730a934d6937d50c0ee0909e21479a414d0d74ee37da8e78a9(
    *,
    failover_dr_replica_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81273dcaf390870f876ba77da06915e73ce49475bd69f290a0f6358a04b0a3cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7832e32e08b45f439a84c96d67f52d314d9a2e95e62f6996bb8b297bff30d99b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d803b8f6817c45b4e141ed870f1fbbf904fe857341cbed8edf20d56df00ee0(
    value: typing.Optional[GoogleSqlDatabaseInstanceReplicationCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4415f533fac97d43e41c278370c8d97fde579904fe0ce0d62adf173cdb6760(
    *,
    backup_run_id: jsii.Number,
    instance_id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86bafdd5deb24853efdb7a46332815da3997f33f783a46bbae0dba712b8d24d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328d9689814fabf14c7485508171c769d62468417a40c8b30380b2cfee466c1b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310e2651cb673b2fa20eb7e6796d204c088b7d6bf64a446536ae4c72f24f140e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cd6cf15cf331614453701cccf9fb2e4f12ebea5f706b9288afcafbde16919d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11aa1cbccbe4ba0812d24514741132ed37c754c1e272b9ee7288e55b2c6c5938(
    value: typing.Optional[GoogleSqlDatabaseInstanceRestoreBackupContext],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793f5cf10da62da577f99a7dbf2c486699ad7297099d9360dc45e397ee4a19fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6650da84959af8d630b1b12fd217e9545a26f411c004724fcf0328c0a87f4fc7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd48a8664af1e4bb36c5e3e2b410f8a0b0737bb33d4eadddc90b76e50d31093(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d11b0110f3fb7edf7d39226b5dec88b16f1ae7c2899761c782d79dd2909c16(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470c31e5981df7f9df99235224d56dbe349ac736a94f36d41fc315119d4baa4a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1bcd201b5d733b6580216a37911ce7637f43b4f7b16cab6a189f02163228aff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec6e7d267c5c9bd1bc1db2fade2aa194e83464647b10033a417a402c9e4af4e(
    value: typing.Optional[GoogleSqlDatabaseInstanceServerCaCert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe9a873e6c71d473adccc7b6681aae1a8ebb21b4d767b2ed57831f9c181ae3d(
    *,
    tier: builtins.str,
    activation_policy: typing.Optional[builtins.str] = None,
    active_directory_config: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_machine_features: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    availability_type: typing.Optional[builtins.str] = None,
    backup_configuration: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsBackupConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    collation: typing.Optional[builtins.str] = None,
    connection_pool_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connector_enforcement: typing.Optional[builtins.str] = None,
    database_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsDatabaseFlags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_cache_config: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsDataCacheConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    data_disk_provisioned_iops: typing.Optional[jsii.Number] = None,
    data_disk_provisioned_throughput: typing.Optional[jsii.Number] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deny_maintenance_period: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_autoresize: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_autoresize_limit: typing.Optional[jsii.Number] = None,
    disk_size: typing.Optional[jsii.Number] = None,
    disk_type: typing.Optional[builtins.str] = None,
    edition: typing.Optional[builtins.str] = None,
    enable_dataplex_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_google_ml_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    insights_config: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsInsightsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_configuration: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsIpConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    location_preference: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsLocationPreference, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_window: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    password_validation_policy: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    retain_backups_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sql_server_audit_config: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c65ba761c500b804303cab634ed923e3a8c8460a5a4354bf8213110f6d4bb7(
    *,
    domain: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a2c46dad7dadcdb5de90a90275300a27586a9a0e6eac9a9c56df98b9888817(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ca271111d665ee752e569ea03977b25d69544d1ad864aae08b62dcc75d8948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220cd5be0d75bee528768fe3d71482aa4a2c40fec1fac7e460ca2cfb738c707f(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsActiveDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378b996dbea28edcbe58ecc4e1525399396c5dd283d39d80f14e382dd042fbaa(
    *,
    threads_per_core: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d2d7ddc532e988e69aced30f9ceeaf816eae76a80976381fd07e29540a27b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1496c4094f0f1050e2686e921e6a607b9d8c3229605304b79edebc1cbc545c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a572dd2478ebb418294c645c5f4d4a1735d651c832c3e866e3b25310707d383c(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsAdvancedMachineFeatures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf613a580205d21b96bca5147b0022316cf820500c8cbf8a900613b742b6f9f2(
    *,
    backup_retention_settings: typing.Optional[typing.Union[GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    binary_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    start_time: typing.Optional[builtins.str] = None,
    transaction_log_retention_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a6f1425b459a8488649311f50719d465e7ebafd4f6f8954a3edfa59c429313(
    *,
    retained_backups: jsii.Number,
    retention_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187f11ea187fbe58b4bed629e2afb9d85554e642bf5ca16b4e0991729f798e45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cfd4b1bc459d5f2150b0174a0a4c26cd11367bbd3f28efb7dbd0efc44405bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86afc20916496dfc6237f0b9eb756624ce63d7c76c8c668a5ae2280e178d0ed4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f6889c8cd239101a18a1954d51705e373944eecc71012e20392d467f0aa312(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd8c173fb9000028e7e93937fdebfbddddaa734f70a508840fd8d856d40c371(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92a419708f8dfb39e39bbc52a6eefa2872846d6ba4aed78d59dad5c47522aa1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857883008f044387432c4cc9299a826feb4ae7cfc6e446774fc7e476b448add5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbed8723cab260c2f9720e9a3ea5f9a77711a8a8becb1e311af3c95d5ebf1e5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089fb626993e4bb2d0cbeddba91a496f2b04a79578ad258c016719419d69c3cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d49a4a5ed2e5a427e16c9be05435a49f9bea708235d1b99f251e16dbd157da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605f54ad4c9643a63aca4861fd90f159d579345891eebd056a71981b9b2e4bd8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7512d0409f3d807c97ed1b038f86cfb2ac579c103840873f1c392261dc9cbd3c(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsBackupConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fdb7d7fe4edb1a2b998c6d6f00680786437624880ee204c0b1aa5b8e5b02ee5(
    *,
    connection_pooling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc434bf1be1dc4bc133f071a022be1f9a78eed60072d0e977873c7ffbb8ca2e(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165f396520789d4f88a1abb89f69e1467deb86442d84f646129492c3530ffeba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4105def92cef6e1734896d127ebe9f4a15dccf5ad1b9332f6033001c5ccb2ae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506980258e9ef9e838c8e9f9ded36a5ae57872e5881cbda4a0428c98a6e1cded(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15204f7f27bb7114c63a93ce3eebe0dfa065337a6ac4a7ce0758e10d5ce0d6d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3acb794f991d784fcc54c8ad4a0320ee5804d7457205c88cdce6984bd0e8656e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d628bd88c63afa0e8b6dfb44f9b2cab4b38126572134e7b4c145323a0c3954(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4a7d40c5787c94255a630cc2cbf43f13e53121543c08d4b08d3fcc578a6336(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f9f3560b238b0fe8ae59a820f269bb8565f253b3d9a40c0dd0eb0be3e6c696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c73acf000861d10aeee6b0d2425cac2eea4edb94fe0a6a6c69e0efc45965e01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19918adde965cecdbd30e85a655738c942099abb43725a58b497ff31e6ab8ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4de74c4bc9a332dce1cdddcdc8409f81abef440b4af18d3823363d02248de6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12ae40c83b290be62c528a2cfaff21c77550183e68c11db368657d854064695(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b51f9d980689a59a95799ae57875d8b0a389c35fcada543d28294ba9fac71e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478c34933daa87ee75948166815c577f942dc5407915d206e409d75293e9cd58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26172f868516c1f4a110e45cc11277e4ecb869d28032fa3b5f4bfce29ac2600(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6368ed780f5deb474c45fa2bdeab5728da23b69e26d27614ca225ff9dc40461(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59f09fb0501a79fd8359b0caacce3ca38fa8c3e74e45bd94ca5eae40bffa45f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67e9c4dc6eede1830cf71c0438a4a4bad1dded49a8c6962c886ab004b424faf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfigFlags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33817dbbb942e70eb5c36f0efdc537962ae5eb1d0d2e06f053d42d6322de009b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609f0dc648057567cecd99b3824541b6f02fd1111b0fac2405589dff0b830ae0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8343dfd654d4306803c4f092ef007b4c9f77cb84c151693eb689b3984dfb5cd1(
    *,
    data_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3b1a4f431f14b2554cfac75f75520299e63a69b93427581bd2aa25acbb06bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3d7e6da798cb5ab0ffe19db1abc46a4a3b70d7566050eaefd42af82e86685d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf14e57cf4214fb10df4dcdf33f33347122f1f6143712228719e1b6939a717a0(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsDataCacheConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a093853260d71f67b3e4dcb1eda9fedb77a8af75546480a911d37aa07e1abc9e(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150d0fb2df26dc46d7f8ae3cca9b00207463a9c075094f88d4a4ecd0c49d04d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e568ac6a3438db5c1b3eada3f2a69108a3f2b171c9ee8a1c7566051358b6137f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9053f1adeff3a175035d0f690f3110d0cc7147528f76530e2b9573e374dbf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9770c2f843824ec027ad456a05f3bb1455ce5cc77f45f69b55974926c9035f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfaa8adcc0cc70e5f41f2bdebc931f7a5b264ce268f32f625d8ff40b5688b7cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ddc727e88ff1848ea7c7f9ab13a7a41f581a4b913d873cbdbec8569e0bc377(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsDatabaseFlags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f4808ca0774308a836e82567f39738fbfb2f79b6c5d0fb553b6a5b394d5b9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6fcdc821909c14c2129e12f810e075a2891288a59789725b4129df3be6eaaf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a55c70377ab3e29cf07c8e6328cb24a20f4accdd888e79d9822af1decfc4275(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2475a82a164374b47dd1b9b875a33829adc6fc132debc4aa3aaf92b3e2a468ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsDatabaseFlags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af8ba156714a80aaa98057b1b1375e2354f01f70c59ce8d9c022457dc7c8ede(
    *,
    end_date: builtins.str,
    start_date: builtins.str,
    time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cac10f55b9024680b46d7f836126d168e9f32dc599e1d285b59d0740864308(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df3505e077753924c13bddb8bb6d8ced54860e679f95f48ed2e9d64f5de11b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5137c9ec63900c1332fce4503d651463617be065728793164d3ae04b5ce0ca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b33b67c3f1a0ec7113600e4484600369da0ae6e2c03da55c7f7bcf923634287(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e067efa1cc6da685aa3ed40820d3cef91997a72d2d1183f0277fd65d6b1cf32d(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsDenyMaintenancePeriod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb454ffedcfba27aa3eb147fa041858d8ec39d79af5533137a357af7651e2867(
    *,
    query_insights_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_plans_per_minute: typing.Optional[jsii.Number] = None,
    query_string_length: typing.Optional[jsii.Number] = None,
    record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c77864d562093e1cd7b1651d5b9a1457ab5f81d7dc426f0443ae7b7ff6f09a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6774db75daf3b69d7274ac7a591909d1c5119d149791b245b9cc6f9be856c8e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58c8d9e5c9bdda2be7d2077a8b7f01b86311dd6606f22c31f6a843141716e84(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29b4cb8d78092549faccb97a1e7299ef93b6a7c7b83b2f2e39152c3db805715(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877d6f4680423dc4b484db9d67e4996e1ec3ec7963c23706248e800507f068e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e745128f40817eb9399e18d4a59b6161cef40a67ba6c453541de340a781c2c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a856dc853c9c34e9f70cce6a208fdc5a8ed79b326bdc98ff76babb3adf418cb(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsInsightsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1daccc9c20c831ceddfe147142938378c93bff9dbfa12eda21b9149579bd3b(
    *,
    allocated_ip_range: typing.Optional[builtins.str] = None,
    authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_private_path_for_google_cloud_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ipv4_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_network: typing.Optional[builtins.str] = None,
    psc_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    server_ca_mode: typing.Optional[builtins.str] = None,
    server_ca_pool: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99715386d56f8d42ec1b55d4a939ac03da764dfface076026828a40baa3d4376(
    *,
    value: builtins.str,
    expiration_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be081cab968ddc30e1760f4f4cd67d0f4fc3d8d89985a23f35d5443900aa8ed1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52443188b35b199b76544861e887c7474d3341b7233d04e9e142b5fee5a03524(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57bca9478c27b8cdeef38c4471bcfe0cf741a18fbbdfb15f63158654ab428c1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac31aa7aebcbd696916cf6b91fea58ca3983f19f6309d67624cda6ff6a462f8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5fdc8d1d53abd513d399c255eab00751c5a12246c29d043ab659ca3715842a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5235e2bfb508f0f8d7f08fac4baab50b0b41431dc17052c7d39466f8c604bd89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fe2b03b3195d128941930cee963bf87f1ca77fe280cc09a695b6a39697bef8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0130d2c2d6e0b1774f24153d53c120768863e60cd52471bec52412ec208f07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce107946d0a469366d356327921059a47bd6d6e0bf281cefc6772cd8f4a3cec3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed732d042ca06db5d6ed387d8d973b97ebf0fc6350a2bbbf0162507de9dc6b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9ad08d7f712bafe8441c30cdf53de40f8796793db8ac53c3c82cb21674affa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa89dd5bc890ea2b0fe002a55a7fc98eb7fc6ec5dbaa97bfa94e13fb0800ec1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6baebddd19161ef1278bce888ea7607c495a7f4e469a8a0452bfd3fe66872d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3199b7b92b60f8c8467d3ca4eb9a98004faacaba6ae02b8fd7fd1ceef066bd9f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f46bef173bb462231b8c1841d372d634167a020f8f9e46c81911be12041b0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e582e35bf6868d3774018149cbe94a84871fd63b52ac1da86e415662f2ce29ae(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822b773ef664744ca464cfd13e9b8aa8914fe0e11317f271dc2e1868174e805b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c1d0b6ece9c3f3ae897af290e151d4c97ac57f4eb3a830d53ff06ab293ae49(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db894bc6bd2cdb7048bd5e13aea9dd8d580e7f1ea07b12563723e2dcbaaf582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78fb9720669680f68ab2aefdf6e7ec7a8044361c57b3497137bce97e4918f108(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193570d5e053914d17333f243e349b7a3fb9ca882fc521bd8265fd89e9303522(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3363c6e1ad88fa9ae45a09084bc7b5381f6060b348359eaab98ea0b2e344ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844880cff83c86f4e5be3b25cacb1d89e1ef9a05355355e103bb1d6525785e0a(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsIpConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3177f9d5e531abd325a0882875f59dcf23cbe84a3c247ae1bd8b08d80f3de1b1(
    *,
    allowed_consumer_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]]] = None,
    psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2374aaa831b86fd437cea31453a561d732223ab3bd903ec74e404b13df6e6fd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d6ac65851efafdf297a7a5f18721d366f81b9f9e4654c2a7f3cd177e256c21(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8171e29104ca6838f0632f124182e96729c1845e76af6de9b34ac1b31c3962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d74025e5d12831c5e67e124adc36ec2cde2d6148ccd504071ff1b72aa46de1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa1132db9477fea22f3a421c366b87df94d5d1a4a7b836c951167ddb0f891f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e752d753925076afda99edcd217e893637aea8bb2646b4dac284853513938e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66797db70e918a2aa71ffdde62b674f3102d1f51a202e36849dca4e7c4c9e5b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ae619efb4e17e25f275e6bf6cd8099558587e553429d69ae8c603013b5f1b4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0efae9ad81f99741789388c1bc65921256e52e2806798e8aa0e98f724047ca1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e406276b7ec31392a63ec1e77d3044743aed6add185519e755f272e5e698611(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe587ac7f1a092898a66fa817b887cbc544f18d72ed3d45543301721512c5fbd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdbc90d49d00684cee71fca228098205574f849b379d4fd013d671c802f5522(
    *,
    consumer_network: builtins.str,
    consumer_service_project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978a5ffd3fbeaaaf75cae9f7f6319b94d5058571cfa1b87391e53102678cd3eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8264da5a4b41ff5f483f1d12ce0e6ceee45d613db16fe213c839f0e7cf61a610(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c49677812fc4577243fbc568a9fc1aab79d5e3bd34599e2ef2570c2f999ca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f8298fd91d3ebe14f6e0ff7a8054b29365db2d15abe93bdb4b0203f52777f5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ea1f1e1aeac44a08f0c85424e443e7c74c8e0b219ee42f476112bf16c16cc0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7e8d5e9f120ec877aa29390819c3ab72e437ff042a724a5a846a20911bfd84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa10413a061b2e4bd4a4eed3501c866b2d3226b60c6faf41a3dcffd6b83f1a9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97809894ac26b96e713e68c349e9a0026ca30af11fdb20385d338ef10fb647d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c52b5992b33ef097a0e6baa1b7995b79cecacef97036f9f0f88dfe4741eab6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4595d182557a67ea649e2db70b6459d2e5a1b2629933a6e665ab47f6e759754e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067a947017c105aad37746c2e8b3b522d4e328cfc0404b9e5809c1b9563d93b4(
    *,
    follow_gae_application: typing.Optional[builtins.str] = None,
    secondary_zone: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecdc8898bf79b5b438c281f9de456c1fed15dd0907294731d1e8ca96eed35307(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57496a367a1444935eeb76467eb6486016f65ac9edacc97da96da88ae0f91ac8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b2f9daa70d93cde44da4bdbab9b30c51cf002c3e34c291693a51eccd215634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3286d752d3445519df7214c3b7b3fe69aa41ba769bfb0620e1e7e57f47b240f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382281fd496170e1eda9f30621bb7937cbd60d33ff9be1a5f4e30ca4d18f2cf5(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsLocationPreference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d3338694a3ab5463f50bc16dbced5f8f8096926b1e445c0c88ab22d00177c4(
    *,
    day: typing.Optional[jsii.Number] = None,
    hour: typing.Optional[jsii.Number] = None,
    update_track: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30bb8c026c4c158c5ef2652efa3c3fc7f5cd82f1abcd16bd97ed6a6063966d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39701518be00a6540cf644e1b461e6386ec3931e61d21844c2d3c52303b847c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8aa64507f84b06e34bfc14f7d18cfb3da0bc9b1ada55c4c296874dbb8df597(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7297512926c514237720692d7f85278b82b4c8096950cd9cc711f4c3031df6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd7a364a75a9d38e4199c33954faba6ddb2558bb363682941fef3dde4c08f49(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35afc479ec1a1fa9cd96c1e7da82f1aa246f71f2494110506722cce892e70a6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ca688a88e867011cf40301ff5203ab531ab3af57d56356ee0212c3c533c2ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsConnectionPoolConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fedc97331e13d8db49f1d61b26dba7fc82d97a7fd334d13decbf4958b03774(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleSqlDatabaseInstanceSettingsDatabaseFlags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d555ab686be6af40997b1cc6c1f19fb1941128e9ee25b2261bb491aaf2545d3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402ea70c8f77fdcef0c21f4f37d3a45720e72094bacddb0739a62ed0968f60e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ebff72a8bece43139a6841ca39120b8846eba7c9a6828cf3c32cb8f72b54d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c22ad20b1335f9839763108bda870474be676356e2ea1d71ded3c9bd34c7f07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fedaaf9f847eb4750b2047c20e81438c0df0823d772fc80831d01d9a16321d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc8ddec72e3bf253b60c1faf73c3fee54823f587ec2c58c7447cc626367af4a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbec54f29cef253cf5de81288d214fd3aefe0da67c57febaa303dfd37638507(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd814771282532c6e4674bb5844db41850f9aeac22dc1a0ecaa1e0fc5610759c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f2f2925a1bef97e1c7cfd8e365f62d4469d12b668944543ded2b307e404621(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de713b27a6e47ec4f1380eafb62c82e32e195871b274d6fe7a4af3e14d732358(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad948fbf3551734f0cf945524746e58bc4869076a5f594f280e1c5b36e5c0aa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7523cb9076cf478bbd21cfb21f143da77f508cee4a1771160ef0164c2610e90f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06036297daed5400d0ac6509076d869bcccf0e201e5b37db3129c14ad14c2495(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2590ba95ecb6e1f30223514a077e63b47745c090e1bc637cd576841ed233ebc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67eb80287a8fc3b16014d31a62bec3d9af82e958e85cfad40fc1490a8253697(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153e8c0feb6f8467b836c585c1de509cfd6d2596b0a9ac0190c514d55e514e0b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c8a4bd6323ef28634f5665ab852377564ac54e4cd7f2cc31bc5a66159f72e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e589112e3f163c1e332c5f612f4eb8a17d81af743142595ab9795a2531806c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b1ea6f98b63e1e348035d88af011df253e43fd7c3923057e4057208bbbaae0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c9aa21c894b5fb0d3bab8161773fb31559aa2dea84c92aaa3b4df215d66b09(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b683ba5a541e198af03b2bdd79eea5e48f780c5754e42e38c5487bc1e96323(
    *,
    enable_password_policy: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    complexity: typing.Optional[builtins.str] = None,
    disallow_username_substring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    min_length: typing.Optional[jsii.Number] = None,
    password_change_interval: typing.Optional[builtins.str] = None,
    reuse_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd8b888bb14703479b410c908a6d035d798c342a04f5865dfb6b4853d6c8141(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75aaf56e0b5ea7a464e4e9800a79f92c4c3df7745b4c2d1d8a80c811001213ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93018b3011d9e0d0e661279de20b5834264425d71a719630979773b9bfbcc725(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88d35f06b6aa41c673bed481da907bfb6e4e02849b06ab2940c22003fd7553b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2ef43ccb214bd5cb74e876b557b4b8c8bf4b1b933da54186562f70359b9f82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61133f871e5b9f6b486b4deb0f6922c97960e080988035cae2a74f0591f8ce33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082b6592e50350a212c766b1d179dc2d5817507eae5265bf1a5a816d8ac66279(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7a582cc8b51b9ae7a2e35add2c93cb6b4fa8900e05c3d83139bb540915f4cd(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsPasswordValidationPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9502db5c2d40b20eec14fefb180f4da517a23314a946ed5155a9636277d47ed(
    *,
    bucket: typing.Optional[builtins.str] = None,
    retention_interval: typing.Optional[builtins.str] = None,
    upload_interval: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5307c85a88a275e70860e678f401c2c948e034766f5bd4b158ec1cb924e0a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474379f127d605458171ba081db7fc2409c322f15ea7642c0ab264c3d21c99a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01409b39f985d5954f24500da9bdd512f84ddfb4fbc6c481d7e14f47ced0c3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a094f7d86169ac8bbad9e6969fc41e6a507f59240e90a9729dcf2a05d83749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f4af05960b1ad8d78f1fdc6fbb1ac223014d5863175645b056d86a42cbe95f(
    value: typing.Optional[GoogleSqlDatabaseInstanceSettingsSqlServerAuditConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2d85ecc9917c9391a930469296153c134f7b2785d6a396845f8e0ee246d4ca(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66bcb9b8ba2278d46eb78c78f26e8a482037a695a1f6a315491710965a107f8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165268a1030c987561af903f01340c48b3f894d92241d5751ae21c7e0a9f11d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8832679cc342c8ae52e38ca60a014e662d2c6fa29662122f40b90fac1332f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb84195ec99c988b01e40c706f3586866619c66a13280e583ebbdd751f03fc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a23d507cb1dc8d20c18c7a7a3e8106f1c5ec99359d05d7e33e70c902a3f389(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleSqlDatabaseInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
