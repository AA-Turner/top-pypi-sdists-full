r'''
# `google_sql_database_instance`

Refer to the Terraform Registry for docs: [`google_sql_database_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance).
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


class SqlDatabaseInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance google_sql_database_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database_version: builtins.str,
        clone: typing.Optional[typing.Union["SqlDatabaseInstanceClone", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        maintenance_version: typing.Optional[builtins.str] = None,
        master_instance_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        replica_configuration: typing.Optional[typing.Union["SqlDatabaseInstanceReplicaConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        replica_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_cluster: typing.Optional[typing.Union["SqlDatabaseInstanceReplicationCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_backup_context: typing.Optional[typing.Union["SqlDatabaseInstanceRestoreBackupContext", typing.Dict[builtins.str, typing.Any]]] = None,
        root_password: typing.Optional[builtins.str] = None,
        settings: typing.Optional[typing.Union["SqlDatabaseInstanceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["SqlDatabaseInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance google_sql_database_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database_version: The MySQL, PostgreSQL or SQL Server (beta) version to use. Supported values include MYSQL_5_6, MYSQL_5_7, MYSQL_8_0, MYSQL_8_4, POSTGRES_9_6, POSTGRES_10, POSTGRES_11, POSTGRES_12, POSTGRES_13, POSTGRES_14, POSTGRES_15, POSTGRES_16, POSTGRES_17, SQLSERVER_2017_STANDARD, SQLSERVER_2017_ENTERPRISE, SQLSERVER_2017_EXPRESS, SQLSERVER_2017_WEB. Database Version Policies includes an up-to-date reference of supported versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#database_version SqlDatabaseInstance#database_version}
        :param clone: clone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#clone SqlDatabaseInstance#clone}
        :param deletion_protection: Used to block Terraform from deleting a SQL Instance. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#deletion_protection SqlDatabaseInstance#deletion_protection}
        :param encryption_key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#encryption_key_name SqlDatabaseInstance#encryption_key_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#id SqlDatabaseInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_type: The type of the instance. The valid values are:- 'SQL_INSTANCE_TYPE_UNSPECIFIED', 'CLOUD_SQL_INSTANCE', 'ON_PREMISES_INSTANCE' and 'READ_REPLICA_INSTANCE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#instance_type SqlDatabaseInstance#instance_type}
        :param maintenance_version: Maintenance version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#maintenance_version SqlDatabaseInstance#maintenance_version}
        :param master_instance_name: The name of the instance that will act as the master in the replication setup. Note, this requires the master to have binary_log_enabled set, as well as existing backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#master_instance_name SqlDatabaseInstance#master_instance_name}
        :param name: The name of the instance. If the name is left blank, Terraform will randomly generate one when the instance is first created. This is done because after a name is used, it cannot be reused for up to one week. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#name SqlDatabaseInstance#name}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#project SqlDatabaseInstance#project}
        :param region: The region the instance will sit in. Note, Cloud SQL is not available in all regions. A valid region must be provided to use this resource. If a region is not provided in the resource definition, the provider region will be used instead, but this will be an apply-time error for instances if the provider region is not supported with Cloud SQL. If you choose not to provide the region argument for this resource, make sure you understand this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#region SqlDatabaseInstance#region}
        :param replica_configuration: replica_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#replica_configuration SqlDatabaseInstance#replica_configuration}
        :param replica_names: The replicas of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#replica_names SqlDatabaseInstance#replica_names}
        :param replication_cluster: replication_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#replication_cluster SqlDatabaseInstance#replication_cluster}
        :param restore_backup_context: restore_backup_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#restore_backup_context SqlDatabaseInstance#restore_backup_context}
        :param root_password: Initial root password. Required for MS SQL Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#root_password SqlDatabaseInstance#root_password}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#settings SqlDatabaseInstance#settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#timeouts SqlDatabaseInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3bf1ac712a1c7cbe138519a7ed9482e4989d1c744d6981dec2442a5b0d9a4d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SqlDatabaseInstanceConfig(
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
        '''Generates CDKTF code for importing a SqlDatabaseInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SqlDatabaseInstance to import.
        :param import_from_id: The id of the existing SqlDatabaseInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SqlDatabaseInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25cd631e6e3821e1d1fe25b9eb858cc732b0aedafb1203d3849e4c6b6ec1fb1a)
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
        :param source_instance_name: The name of the instance from which the point in time should be restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#source_instance_name SqlDatabaseInstance#source_instance_name}
        :param allocated_ip_range: The name of the allocated ip range for the private ip CloudSQL instance. For example: "google-managed-services-default". If set, the cloned instance ip will be created in the allocated range. The range name must comply with `RFC 1035 <https://tools.ietf.org/html/rfc1035>`_. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#allocated_ip_range SqlDatabaseInstance#allocated_ip_range}
        :param database_names: (SQL Server only, use with point_in_time) clone only the specified databases from the source instance. Clone all databases if empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#database_names SqlDatabaseInstance#database_names}
        :param point_in_time: The timestamp of the point in time that should be restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#point_in_time SqlDatabaseInstance#point_in_time}
        :param preferred_zone: (Point-in-time recovery for PostgreSQL only) Clone to an instance in the specified zone. If no zone is specified, clone to the same zone as the source instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#preferred_zone SqlDatabaseInstance#preferred_zone}
        '''
        value = SqlDatabaseInstanceClone(
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
        :param ca_certificate: PEM representation of the trusted CA's x509 certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ca_certificate SqlDatabaseInstance#ca_certificate}
        :param cascadable_replica: Specifies if a SQL Server replica is a cascadable replica. A cascadable replica is a SQL Server cross region replica that supports replica(s) under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#cascadable_replica SqlDatabaseInstance#cascadable_replica}
        :param client_certificate: PEM representation of the replica's x509 certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#client_certificate SqlDatabaseInstance#client_certificate}
        :param client_key: PEM representation of the replica's private key. The corresponding public key in encoded in the client_certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#client_key SqlDatabaseInstance#client_key}
        :param connect_retry_interval: The number of seconds between connect retries. MySQL's default is 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#connect_retry_interval SqlDatabaseInstance#connect_retry_interval}
        :param dump_file_path: Path to a SQL file in Google Cloud Storage from which replica instances are created. Format is gs://bucket/filename. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#dump_file_path SqlDatabaseInstance#dump_file_path}
        :param failover_target: Specifies if the replica is the failover target. If the field is set to true the replica will be designated as a failover replica. If the master instance fails, the replica instance will be promoted as the new master instance. Not supported for Postgres Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#failover_target SqlDatabaseInstance#failover_target}
        :param master_heartbeat_period: Time in ms between replication heartbeats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#master_heartbeat_period SqlDatabaseInstance#master_heartbeat_period}
        :param password: Password for the replication connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#password SqlDatabaseInstance#password}
        :param ssl_cipher: Permissible ciphers for use in SSL encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ssl_cipher SqlDatabaseInstance#ssl_cipher}
        :param username: Username for replication connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#username SqlDatabaseInstance#username}
        :param verify_server_certificate: True if the master's common name value is checked during the SSL handshake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#verify_server_certificate SqlDatabaseInstance#verify_server_certificate}
        '''
        value = SqlDatabaseInstanceReplicaConfiguration(
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
        :param failover_dr_replica_name: If the instance is a primary instance, then this field identifies the disaster recovery (DR) replica. The standard format of this field is "your-project:your-instance". You can also set this field to "your-instance", but cloud SQL backend will convert it to the aforementioned standard format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#failover_dr_replica_name SqlDatabaseInstance#failover_dr_replica_name}
        '''
        value = SqlDatabaseInstanceReplicationCluster(
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
        :param backup_run_id: The ID of the backup run to restore from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#backup_run_id SqlDatabaseInstance#backup_run_id}
        :param instance_id: The ID of the instance that the backup was taken from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#instance_id SqlDatabaseInstance#instance_id}
        :param project: The full project ID of the source instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#project SqlDatabaseInstance#project}
        '''
        value = SqlDatabaseInstanceRestoreBackupContext(
            backup_run_id=backup_run_id, instance_id=instance_id, project=project
        )

        return typing.cast(None, jsii.invoke(self, "putRestoreBackupContext", [value]))

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        *,
        tier: builtins.str,
        activation_policy: typing.Optional[builtins.str] = None,
        active_directory_config: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsActiveDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_machine_features: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        availability_type: typing.Optional[builtins.str] = None,
        backup_configuration: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsBackupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        collation: typing.Optional[builtins.str] = None,
        connection_pool_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlDatabaseInstanceSettingsConnectionPoolConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connector_enforcement: typing.Optional[builtins.str] = None,
        database_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlDatabaseInstanceSettingsDatabaseFlags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_cache_config: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsDataCacheConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deny_maintenance_period: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsDenyMaintenancePeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_autoresize: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_autoresize_limit: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        enable_dataplex_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_google_ml_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        insights_config: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsInsightsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_configuration: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsIpConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        location_preference: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsLocationPreference", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_window: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        password_validation_policy: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsPasswordValidationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        retain_backups_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sql_server_audit_config: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsSqlServerAuditConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param tier: The machine type to use. See tiers for more details and supported versions. Postgres supports only shared-core machine types, and custom machine types such as db-custom-2-13312. See the Custom Machine Type Documentation to learn about specifying custom machine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#tier SqlDatabaseInstance#tier}
        :param activation_policy: This specifies when the instance should be active. Can be either ALWAYS, NEVER or ON_DEMAND. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#activation_policy SqlDatabaseInstance#activation_policy}
        :param active_directory_config: active_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#active_directory_config SqlDatabaseInstance#active_directory_config}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#advanced_machine_features SqlDatabaseInstance#advanced_machine_features}
        :param availability_type: The availability type of the Cloud SQL instance, high availability (REGIONAL) or single zone (ZONAL). For all instances, ensure that settings.backup_configuration.enabled is set to true. For MySQL instances, ensure that settings.backup_configuration.binary_log_enabled is set to true. For Postgres instances, ensure that settings.backup_configuration.point_in_time_recovery_enabled is set to true. Defaults to ZONAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#availability_type SqlDatabaseInstance#availability_type}
        :param backup_configuration: backup_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#backup_configuration SqlDatabaseInstance#backup_configuration}
        :param collation: The name of server instance collation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#collation SqlDatabaseInstance#collation}
        :param connection_pool_config: connection_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#connection_pool_config SqlDatabaseInstance#connection_pool_config}
        :param connector_enforcement: Enables the enforcement of Cloud SQL Auth Proxy or Cloud SQL connectors for all the connections. If enabled, all the direct connections are rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#connector_enforcement SqlDatabaseInstance#connector_enforcement}
        :param database_flags: database_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#database_flags SqlDatabaseInstance#database_flags}
        :param data_cache_config: data_cache_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#data_cache_config SqlDatabaseInstance#data_cache_config}
        :param deletion_protection_enabled: Configuration to protect against accidental instance deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#deletion_protection_enabled SqlDatabaseInstance#deletion_protection_enabled}
        :param deny_maintenance_period: deny_maintenance_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#deny_maintenance_period SqlDatabaseInstance#deny_maintenance_period}
        :param disk_autoresize: Enables auto-resizing of the storage size. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_autoresize SqlDatabaseInstance#disk_autoresize}
        :param disk_autoresize_limit: The maximum size, in GB, to which storage capacity can be automatically increased. The default value is 0, which specifies that there is no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_autoresize_limit SqlDatabaseInstance#disk_autoresize_limit}
        :param disk_size: The size of data disk, in GB. Size of a running instance cannot be reduced but can be increased. The minimum value is 10GB for PD_SSD, PD_HDD and 20GB for HYPERDISK_BALANCED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_size SqlDatabaseInstance#disk_size}
        :param disk_type: The type of supported data disk is tier dependent and can be PD_SSD or PD_HDD or HYPERDISK_BALANCED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_type SqlDatabaseInstance#disk_type}
        :param edition: The edition of the instance, can be ENTERPRISE or ENTERPRISE_PLUS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#edition SqlDatabaseInstance#edition}
        :param enable_dataplex_integration: Enables Dataplex Integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_dataplex_integration SqlDatabaseInstance#enable_dataplex_integration}
        :param enable_google_ml_integration: Enables Vertex AI Integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_google_ml_integration SqlDatabaseInstance#enable_google_ml_integration}
        :param insights_config: insights_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#insights_config SqlDatabaseInstance#insights_config}
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ip_configuration SqlDatabaseInstance#ip_configuration}
        :param location_preference: location_preference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#location_preference SqlDatabaseInstance#location_preference}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#maintenance_window SqlDatabaseInstance#maintenance_window}
        :param password_validation_policy: password_validation_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#password_validation_policy SqlDatabaseInstance#password_validation_policy}
        :param pricing_plan: Pricing plan for this instance, can only be PER_USE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#pricing_plan SqlDatabaseInstance#pricing_plan}
        :param retain_backups_on_delete: When this parameter is set to true, Cloud SQL retains backups of the instance even after the instance is deleted. The ON_DEMAND backup will be retained until customer deletes the backup or the project. The AUTOMATED backup will be retained based on the backups retention setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retain_backups_on_delete SqlDatabaseInstance#retain_backups_on_delete}
        :param sql_server_audit_config: sql_server_audit_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#sql_server_audit_config SqlDatabaseInstance#sql_server_audit_config}
        :param time_zone: The time_zone to be used by the database engine (supported only for SQL Server), in SQL Server timezone format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#time_zone SqlDatabaseInstance#time_zone}
        :param user_labels: A set of key/value user label pairs to assign to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#user_labels SqlDatabaseInstance#user_labels}
        '''
        value = SqlDatabaseInstanceSettings(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#create SqlDatabaseInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#delete SqlDatabaseInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#update SqlDatabaseInstance#update}.
        '''
        value = SqlDatabaseInstanceTimeouts(
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
    def clone(self) -> "SqlDatabaseInstanceCloneOutputReference":
        return typing.cast("SqlDatabaseInstanceCloneOutputReference", jsii.get(self, "clone"))

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
    def dns_names(self) -> "SqlDatabaseInstanceDnsNamesList":
        return typing.cast("SqlDatabaseInstanceDnsNamesList", jsii.get(self, "dnsNames"))

    @builtins.property
    @jsii.member(jsii_name="firstIpAddress")
    def first_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> "SqlDatabaseInstanceIpAddressList":
        return typing.cast("SqlDatabaseInstanceIpAddressList", jsii.get(self, "ipAddress"))

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
    ) -> "SqlDatabaseInstanceReplicaConfigurationOutputReference":
        return typing.cast("SqlDatabaseInstanceReplicaConfigurationOutputReference", jsii.get(self, "replicaConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="replicationCluster")
    def replication_cluster(
        self,
    ) -> "SqlDatabaseInstanceReplicationClusterOutputReference":
        return typing.cast("SqlDatabaseInstanceReplicationClusterOutputReference", jsii.get(self, "replicationCluster"))

    @builtins.property
    @jsii.member(jsii_name="restoreBackupContext")
    def restore_backup_context(
        self,
    ) -> "SqlDatabaseInstanceRestoreBackupContextOutputReference":
        return typing.cast("SqlDatabaseInstanceRestoreBackupContextOutputReference", jsii.get(self, "restoreBackupContext"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="serverCaCert")
    def server_ca_cert(self) -> "SqlDatabaseInstanceServerCaCertList":
        return typing.cast("SqlDatabaseInstanceServerCaCertList", jsii.get(self, "serverCaCert"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountEmailAddress")
    def service_account_email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountEmailAddress"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(self) -> "SqlDatabaseInstanceSettingsOutputReference":
        return typing.cast("SqlDatabaseInstanceSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SqlDatabaseInstanceTimeoutsOutputReference":
        return typing.cast("SqlDatabaseInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cloneInput")
    def clone_input(self) -> typing.Optional["SqlDatabaseInstanceClone"]:
        return typing.cast(typing.Optional["SqlDatabaseInstanceClone"], jsii.get(self, "cloneInput"))

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
    ) -> typing.Optional["SqlDatabaseInstanceReplicaConfiguration"]:
        return typing.cast(typing.Optional["SqlDatabaseInstanceReplicaConfiguration"], jsii.get(self, "replicaConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaNamesInput")
    def replica_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "replicaNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationClusterInput")
    def replication_cluster_input(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceReplicationCluster"]:
        return typing.cast(typing.Optional["SqlDatabaseInstanceReplicationCluster"], jsii.get(self, "replicationClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreBackupContextInput")
    def restore_backup_context_input(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceRestoreBackupContext"]:
        return typing.cast(typing.Optional["SqlDatabaseInstanceRestoreBackupContext"], jsii.get(self, "restoreBackupContextInput"))

    @builtins.property
    @jsii.member(jsii_name="rootPasswordInput")
    def root_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(self) -> typing.Optional["SqlDatabaseInstanceSettings"]:
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettings"], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SqlDatabaseInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SqlDatabaseInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseVersion")
    def database_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseVersion"))

    @database_version.setter
    def database_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36f71fbd551e901be0957e4d86495bb924d17b6f7987d4b324d40215a8a7974)
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
            type_hints = typing.get_type_hints(_typecheckingstub__285f8d9fd7abab2bcc721bc79996adf57025295eb7f0ff500380204f24763219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyName")
    def encryption_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKeyName"))

    @encryption_key_name.setter
    def encryption_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c765d5eab238f5d57251eba14ed7d6f901180a8128d1109d56ab6e59f0ccd5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d33319c414a9a36652e491e7b7c4315c27d7871c9e8a0379e089bbfc221a4b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42616e4620c3d602069086cf029213456f80be5b1c3dac166524a439428e0d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceVersion")
    def maintenance_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceVersion"))

    @maintenance_version.setter
    def maintenance_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4929e72c0605fd7c4ab0f378d3dd7ffd500b708c1e3d7faa0dc207f85c00c0c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterInstanceName")
    def master_instance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterInstanceName"))

    @master_instance_name.setter
    def master_instance_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddbf47ae16b53d58cc05abc5a18fc0431816cc90900268433cad49751117e577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterInstanceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fde7d5463af04abd53029aae824ff22c70340b3c04dd27db0c96c69cdc7d57e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3088e264c302a9074cc2feaf8ae9a19fd23508f23b2bdf9499fc03faeb229f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a944d29df4177231936dbe3509dc3fad556aa82d6a9d885d1d89b600ec9c62c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaNames")
    def replica_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "replicaNames"))

    @replica_names.setter
    def replica_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047552c008360797d8d223cc6599efe2a70e7d35130a6cc252cfdce168c98dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootPassword")
    def root_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootPassword"))

    @root_password.setter
    def root_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb79c6f86ac1a4c1789f3fc433e1de8c97410d31f35044e459f331bb54b39867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootPassword", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceClone",
    jsii_struct_bases=[],
    name_mapping={
        "source_instance_name": "sourceInstanceName",
        "allocated_ip_range": "allocatedIpRange",
        "database_names": "databaseNames",
        "point_in_time": "pointInTime",
        "preferred_zone": "preferredZone",
    },
)
class SqlDatabaseInstanceClone:
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
        :param source_instance_name: The name of the instance from which the point in time should be restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#source_instance_name SqlDatabaseInstance#source_instance_name}
        :param allocated_ip_range: The name of the allocated ip range for the private ip CloudSQL instance. For example: "google-managed-services-default". If set, the cloned instance ip will be created in the allocated range. The range name must comply with `RFC 1035 <https://tools.ietf.org/html/rfc1035>`_. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#allocated_ip_range SqlDatabaseInstance#allocated_ip_range}
        :param database_names: (SQL Server only, use with point_in_time) clone only the specified databases from the source instance. Clone all databases if empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#database_names SqlDatabaseInstance#database_names}
        :param point_in_time: The timestamp of the point in time that should be restored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#point_in_time SqlDatabaseInstance#point_in_time}
        :param preferred_zone: (Point-in-time recovery for PostgreSQL only) Clone to an instance in the specified zone. If no zone is specified, clone to the same zone as the source instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#preferred_zone SqlDatabaseInstance#preferred_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b44a200e038d655ed373067ea7967371892ef11ef977afc99a1e867e92794105)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#source_instance_name SqlDatabaseInstance#source_instance_name}
        '''
        result = self._values.get("source_instance_name")
        assert result is not None, "Required property 'source_instance_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allocated_ip_range(self) -> typing.Optional[builtins.str]:
        '''The name of the allocated ip range for the private ip CloudSQL instance.

        For example: "google-managed-services-default". If set, the cloned instance ip will be created in the allocated range. The range name must comply with `RFC 1035 <https://tools.ietf.org/html/rfc1035>`_. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#allocated_ip_range SqlDatabaseInstance#allocated_ip_range}
        '''
        result = self._values.get("allocated_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(SQL Server only, use with point_in_time) clone only the specified databases from the source instance.

        Clone all databases if empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#database_names SqlDatabaseInstance#database_names}
        '''
        result = self._values.get("database_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def point_in_time(self) -> typing.Optional[builtins.str]:
        '''The timestamp of the point in time that should be restored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#point_in_time SqlDatabaseInstance#point_in_time}
        '''
        result = self._values.get("point_in_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_zone(self) -> typing.Optional[builtins.str]:
        '''(Point-in-time recovery for PostgreSQL only) Clone to an instance in the specified zone.

        If no zone is specified, clone to the same zone as the source instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#preferred_zone SqlDatabaseInstance#preferred_zone}
        '''
        result = self._values.get("preferred_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceClone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceCloneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceCloneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6021d18ad7fcdb130a45c562398c5c383ca7d6a2bd14ef49d2c786221ad7d206)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f5ade42b83672fc3b813ca286c220e8dc18548a9dbd79448dac49ba60ed0a72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocatedIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseNames")
    def database_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "databaseNames"))

    @database_names.setter
    def database_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a713cb115600379a6a2f5d76b8a3cb493a804b16e23df6718591903eee76711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pointInTime")
    def point_in_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pointInTime"))

    @point_in_time.setter
    def point_in_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ded8d7fe2bbcd66a8b0103737e74268fbbd73d46eead68b5777bc0578e79f33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredZone")
    def preferred_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredZone"))

    @preferred_zone.setter
    def preferred_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c331b561177059dac99c078ca94c53ebaeced8d77cff8b6b90ba985df753da3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceName")
    def source_instance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceInstanceName"))

    @source_instance_name.setter
    def source_instance_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9edc2ec219472705981086b030c2451d94a077841e6f56fd7f30963dc54989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceInstanceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SqlDatabaseInstanceClone]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceClone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SqlDatabaseInstanceClone]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0265b88e7f802de6d330b85c2c64634dc8971c2655ca1cd71ef4ac2b74c5cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceConfig",
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
class SqlDatabaseInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        clone: typing.Optional[typing.Union[SqlDatabaseInstanceClone, typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        maintenance_version: typing.Optional[builtins.str] = None,
        master_instance_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        replica_configuration: typing.Optional[typing.Union["SqlDatabaseInstanceReplicaConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        replica_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_cluster: typing.Optional[typing.Union["SqlDatabaseInstanceReplicationCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_backup_context: typing.Optional[typing.Union["SqlDatabaseInstanceRestoreBackupContext", typing.Dict[builtins.str, typing.Any]]] = None,
        root_password: typing.Optional[builtins.str] = None,
        settings: typing.Optional[typing.Union["SqlDatabaseInstanceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["SqlDatabaseInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database_version: The MySQL, PostgreSQL or SQL Server (beta) version to use. Supported values include MYSQL_5_6, MYSQL_5_7, MYSQL_8_0, MYSQL_8_4, POSTGRES_9_6, POSTGRES_10, POSTGRES_11, POSTGRES_12, POSTGRES_13, POSTGRES_14, POSTGRES_15, POSTGRES_16, POSTGRES_17, SQLSERVER_2017_STANDARD, SQLSERVER_2017_ENTERPRISE, SQLSERVER_2017_EXPRESS, SQLSERVER_2017_WEB. Database Version Policies includes an up-to-date reference of supported versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#database_version SqlDatabaseInstance#database_version}
        :param clone: clone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#clone SqlDatabaseInstance#clone}
        :param deletion_protection: Used to block Terraform from deleting a SQL Instance. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#deletion_protection SqlDatabaseInstance#deletion_protection}
        :param encryption_key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#encryption_key_name SqlDatabaseInstance#encryption_key_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#id SqlDatabaseInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_type: The type of the instance. The valid values are:- 'SQL_INSTANCE_TYPE_UNSPECIFIED', 'CLOUD_SQL_INSTANCE', 'ON_PREMISES_INSTANCE' and 'READ_REPLICA_INSTANCE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#instance_type SqlDatabaseInstance#instance_type}
        :param maintenance_version: Maintenance version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#maintenance_version SqlDatabaseInstance#maintenance_version}
        :param master_instance_name: The name of the instance that will act as the master in the replication setup. Note, this requires the master to have binary_log_enabled set, as well as existing backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#master_instance_name SqlDatabaseInstance#master_instance_name}
        :param name: The name of the instance. If the name is left blank, Terraform will randomly generate one when the instance is first created. This is done because after a name is used, it cannot be reused for up to one week. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#name SqlDatabaseInstance#name}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#project SqlDatabaseInstance#project}
        :param region: The region the instance will sit in. Note, Cloud SQL is not available in all regions. A valid region must be provided to use this resource. If a region is not provided in the resource definition, the provider region will be used instead, but this will be an apply-time error for instances if the provider region is not supported with Cloud SQL. If you choose not to provide the region argument for this resource, make sure you understand this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#region SqlDatabaseInstance#region}
        :param replica_configuration: replica_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#replica_configuration SqlDatabaseInstance#replica_configuration}
        :param replica_names: The replicas of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#replica_names SqlDatabaseInstance#replica_names}
        :param replication_cluster: replication_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#replication_cluster SqlDatabaseInstance#replication_cluster}
        :param restore_backup_context: restore_backup_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#restore_backup_context SqlDatabaseInstance#restore_backup_context}
        :param root_password: Initial root password. Required for MS SQL Server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#root_password SqlDatabaseInstance#root_password}
        :param settings: settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#settings SqlDatabaseInstance#settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#timeouts SqlDatabaseInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(clone, dict):
            clone = SqlDatabaseInstanceClone(**clone)
        if isinstance(replica_configuration, dict):
            replica_configuration = SqlDatabaseInstanceReplicaConfiguration(**replica_configuration)
        if isinstance(replication_cluster, dict):
            replication_cluster = SqlDatabaseInstanceReplicationCluster(**replication_cluster)
        if isinstance(restore_backup_context, dict):
            restore_backup_context = SqlDatabaseInstanceRestoreBackupContext(**restore_backup_context)
        if isinstance(settings, dict):
            settings = SqlDatabaseInstanceSettings(**settings)
        if isinstance(timeouts, dict):
            timeouts = SqlDatabaseInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a7f54ffbe15d288113dab684fed8c4d7fcdca6badf25301c7d20f34a6b21d1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#database_version SqlDatabaseInstance#database_version}
        '''
        result = self._values.get("database_version")
        assert result is not None, "Required property 'database_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def clone(self) -> typing.Optional[SqlDatabaseInstanceClone]:
        '''clone block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#clone SqlDatabaseInstance#clone}
        '''
        result = self._values.get("clone")
        return typing.cast(typing.Optional[SqlDatabaseInstanceClone], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Used to block Terraform from deleting a SQL Instance. Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#deletion_protection SqlDatabaseInstance#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#encryption_key_name SqlDatabaseInstance#encryption_key_name}.'''
        result = self._values.get("encryption_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#id SqlDatabaseInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The type of the instance. The valid values are:- 'SQL_INSTANCE_TYPE_UNSPECIFIED', 'CLOUD_SQL_INSTANCE', 'ON_PREMISES_INSTANCE' and 'READ_REPLICA_INSTANCE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#instance_type SqlDatabaseInstance#instance_type}
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_version(self) -> typing.Optional[builtins.str]:
        '''Maintenance version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#maintenance_version SqlDatabaseInstance#maintenance_version}
        '''
        result = self._values.get("maintenance_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_instance_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance that will act as the master in the replication setup.

        Note, this requires the master to have binary_log_enabled set, as well as existing backups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#master_instance_name SqlDatabaseInstance#master_instance_name}
        '''
        result = self._values.get("master_instance_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance.

        If the name is left blank, Terraform will randomly generate one when the instance is first created. This is done because after a name is used, it cannot be reused for up to one week.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#name SqlDatabaseInstance#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#project SqlDatabaseInstance#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region the instance will sit in.

        Note, Cloud SQL is not available in all regions. A valid region must be provided to use this resource. If a region is not provided in the resource definition, the provider region will be used instead, but this will be an apply-time error for instances if the provider region is not supported with Cloud SQL. If you choose not to provide the region argument for this resource, make sure you understand this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#region SqlDatabaseInstance#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_configuration(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceReplicaConfiguration"]:
        '''replica_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#replica_configuration SqlDatabaseInstance#replica_configuration}
        '''
        result = self._values.get("replica_configuration")
        return typing.cast(typing.Optional["SqlDatabaseInstanceReplicaConfiguration"], result)

    @builtins.property
    def replica_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The replicas of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#replica_names SqlDatabaseInstance#replica_names}
        '''
        result = self._values.get("replica_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def replication_cluster(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceReplicationCluster"]:
        '''replication_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#replication_cluster SqlDatabaseInstance#replication_cluster}
        '''
        result = self._values.get("replication_cluster")
        return typing.cast(typing.Optional["SqlDatabaseInstanceReplicationCluster"], result)

    @builtins.property
    def restore_backup_context(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceRestoreBackupContext"]:
        '''restore_backup_context block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#restore_backup_context SqlDatabaseInstance#restore_backup_context}
        '''
        result = self._values.get("restore_backup_context")
        return typing.cast(typing.Optional["SqlDatabaseInstanceRestoreBackupContext"], result)

    @builtins.property
    def root_password(self) -> typing.Optional[builtins.str]:
        '''Initial root password. Required for MS SQL Server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#root_password SqlDatabaseInstance#root_password}
        '''
        result = self._values.get("root_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def settings(self) -> typing.Optional["SqlDatabaseInstanceSettings"]:
        '''settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#settings SqlDatabaseInstance#settings}
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettings"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SqlDatabaseInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#timeouts SqlDatabaseInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SqlDatabaseInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceDnsNames",
    jsii_struct_bases=[],
    name_mapping={},
)
class SqlDatabaseInstanceDnsNames:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceDnsNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceDnsNamesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceDnsNamesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__139daea944be9c4bd0953561e8d0bae628262b8bdaa79d34cc166e0f0b8c46a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SqlDatabaseInstanceDnsNamesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e0f6b5399fc73fd1ec61917a78b370e82054b671d729bc430676f85fceb74a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SqlDatabaseInstanceDnsNamesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d5c9677c75191ff048b758b1f1efc8ec1a0931bdaf7ae27a7fee9c429a69a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c05831baa7c4022dcfed135fc3cad020d46514179eda6e79cf2282b96799d3b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__789338d26c566a516da2dd927195a690ed9bd0177218f6b7c0c5ad4ffc38e7a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceDnsNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceDnsNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__563e7470b3e27b667cf62054c998d19c1c384dc622cfec41833a59e84680b09e)
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
    def internal_value(self) -> typing.Optional[SqlDatabaseInstanceDnsNames]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceDnsNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceDnsNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcef201253e5e5380e0defb2a51c869703df2f21f0148a10911a554c14c87873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceIpAddress",
    jsii_struct_bases=[],
    name_mapping={},
)
class SqlDatabaseInstanceIpAddress:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceIpAddressList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceIpAddressList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1023ee743cafbf21dd66c5aebad96895bd45c4b639c13b04ca118c1ea2efce4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SqlDatabaseInstanceIpAddressOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea0fa515376fded868c948c002d3cd1fb8a1be10622460d401560c83216c09b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SqlDatabaseInstanceIpAddressOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2c79bcf494349ef4c59c1909482f231d1a71e76f2cd2a138b980f73446a3ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7ff8e558141ace1ea449a98c8b66d09db214bcbc7eecf51720e7c7b66530143)
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
            type_hints = typing.get_type_hints(_typecheckingstub__740fb8eff542db7fdafcc4bc380ecee8d11e8a58a759e8c56b233efa404e2cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceIpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceIpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4c7a0a11bcce91c9858b1804075bb63933e755a8ec2d49e33c8cd92ed2aec9e)
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
    def internal_value(self) -> typing.Optional[SqlDatabaseInstanceIpAddress]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceIpAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceIpAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b0d5cda62514ba7919d4871f40ef861f4feb1f2ea6245882b0a59d55f390d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceReplicaConfiguration",
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
class SqlDatabaseInstanceReplicaConfiguration:
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
        :param ca_certificate: PEM representation of the trusted CA's x509 certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ca_certificate SqlDatabaseInstance#ca_certificate}
        :param cascadable_replica: Specifies if a SQL Server replica is a cascadable replica. A cascadable replica is a SQL Server cross region replica that supports replica(s) under it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#cascadable_replica SqlDatabaseInstance#cascadable_replica}
        :param client_certificate: PEM representation of the replica's x509 certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#client_certificate SqlDatabaseInstance#client_certificate}
        :param client_key: PEM representation of the replica's private key. The corresponding public key in encoded in the client_certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#client_key SqlDatabaseInstance#client_key}
        :param connect_retry_interval: The number of seconds between connect retries. MySQL's default is 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#connect_retry_interval SqlDatabaseInstance#connect_retry_interval}
        :param dump_file_path: Path to a SQL file in Google Cloud Storage from which replica instances are created. Format is gs://bucket/filename. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#dump_file_path SqlDatabaseInstance#dump_file_path}
        :param failover_target: Specifies if the replica is the failover target. If the field is set to true the replica will be designated as a failover replica. If the master instance fails, the replica instance will be promoted as the new master instance. Not supported for Postgres Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#failover_target SqlDatabaseInstance#failover_target}
        :param master_heartbeat_period: Time in ms between replication heartbeats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#master_heartbeat_period SqlDatabaseInstance#master_heartbeat_period}
        :param password: Password for the replication connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#password SqlDatabaseInstance#password}
        :param ssl_cipher: Permissible ciphers for use in SSL encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ssl_cipher SqlDatabaseInstance#ssl_cipher}
        :param username: Username for replication connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#username SqlDatabaseInstance#username}
        :param verify_server_certificate: True if the master's common name value is checked during the SSL handshake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#verify_server_certificate SqlDatabaseInstance#verify_server_certificate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9f32b8b2aa7273badba55c69653945bb6911bb6dbef4ad8ff1ad655d7f09ce)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ca_certificate SqlDatabaseInstance#ca_certificate}
        '''
        result = self._values.get("ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cascadable_replica(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if a SQL Server replica is a cascadable replica.

        A cascadable replica is a SQL Server cross region replica that supports replica(s) under it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#cascadable_replica SqlDatabaseInstance#cascadable_replica}
        '''
        result = self._values.get("cascadable_replica")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM representation of the replica's x509 certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#client_certificate SqlDatabaseInstance#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''PEM representation of the replica's private key. The corresponding public key in encoded in the client_certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#client_key SqlDatabaseInstance#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect_retry_interval(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds between connect retries. MySQL's default is 60 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#connect_retry_interval SqlDatabaseInstance#connect_retry_interval}
        '''
        result = self._values.get("connect_retry_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dump_file_path(self) -> typing.Optional[builtins.str]:
        '''Path to a SQL file in Google Cloud Storage from which replica instances are created. Format is gs://bucket/filename.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#dump_file_path SqlDatabaseInstance#dump_file_path}
        '''
        result = self._values.get("dump_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failover_target(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the replica is the failover target.

        If the field is set to true the replica will be designated as a failover replica. If the master instance fails, the replica instance will be promoted as the new master instance. Not supported for Postgres

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#failover_target SqlDatabaseInstance#failover_target}
        '''
        result = self._values.get("failover_target")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def master_heartbeat_period(self) -> typing.Optional[jsii.Number]:
        '''Time in ms between replication heartbeats.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#master_heartbeat_period SqlDatabaseInstance#master_heartbeat_period}
        '''
        result = self._values.get("master_heartbeat_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the replication connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#password SqlDatabaseInstance#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_cipher(self) -> typing.Optional[builtins.str]:
        '''Permissible ciphers for use in SSL encryption.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ssl_cipher SqlDatabaseInstance#ssl_cipher}
        '''
        result = self._values.get("ssl_cipher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for replication connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#username SqlDatabaseInstance#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_server_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the master's common name value is checked during the SSL handshake.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#verify_server_certificate SqlDatabaseInstance#verify_server_certificate}
        '''
        result = self._values.get("verify_server_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceReplicaConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceReplicaConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceReplicaConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bf3fd84dbffa0d9761bd83aef829bf3676fc6f424e71c63055548166443094b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ac3e26d4a6cd7d888a2ee0d19aa8e7b7380b49b0d20a24066937f373d95cafd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fe670db9ee2a9a3554fb0caed9e24131bd7c96a547a54c405c67df19de0f08c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cascadableReplica", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b95eada0b1c207d5d469dfd5fabaa357ee54b39511a66ea641862026b7342ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__118ff0a40786616920ecfd7e4c8ae533e261f1231629de269681c9b43764896d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectRetryInterval")
    def connect_retry_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectRetryInterval"))

    @connect_retry_interval.setter
    def connect_retry_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9800b6a5a2d00996c3a530bd3c67f9c4cd437a71929f9e2e93d79ab1f9af80df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectRetryInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dumpFilePath")
    def dump_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dumpFilePath"))

    @dump_file_path.setter
    def dump_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10c8d7b5ff21963f0e2ac6828b2a43acb1be7dc1e13a56533104879247c7be89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a09be74b23a6e87264f7ec63a7000e6b9b3c163d04610bcf23a73ee744b2357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterHeartbeatPeriod")
    def master_heartbeat_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "masterHeartbeatPeriod"))

    @master_heartbeat_period.setter
    def master_heartbeat_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39047aa77174f2f3837d7a0d39ecee73426702b0a76e4189b0a1534df364bbc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterHeartbeatPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b075827e9e337c847cd32b6a61642f1fa86cb64f2c85b7551f649b21f4e0a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslCipher")
    def ssl_cipher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslCipher"))

    @ssl_cipher.setter
    def ssl_cipher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe9713066d7fd1d40a96a4f0a100b218b9b3141f54e77041c00b5abbbe5f907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslCipher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165e47ab654a2624e3d7616a19b1fa3d5d032de778a410c4082c27337a53d457)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84a619c60055754804cac9f0c2ccaf8532c0db7585733c8ff94c2326cca68df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyServerCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceReplicaConfiguration]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceReplicaConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceReplicaConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d5390c7390f54393b80a11aac218d669ae3ef15c90877549e6d88830c8776f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceReplicationCluster",
    jsii_struct_bases=[],
    name_mapping={"failover_dr_replica_name": "failoverDrReplicaName"},
)
class SqlDatabaseInstanceReplicationCluster:
    def __init__(
        self,
        *,
        failover_dr_replica_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param failover_dr_replica_name: If the instance is a primary instance, then this field identifies the disaster recovery (DR) replica. The standard format of this field is "your-project:your-instance". You can also set this field to "your-instance", but cloud SQL backend will convert it to the aforementioned standard format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#failover_dr_replica_name SqlDatabaseInstance#failover_dr_replica_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ba3d908375e150a6c085951e95f3889524a6740eb50bd38182d55eeee9c986)
            check_type(argname="argument failover_dr_replica_name", value=failover_dr_replica_name, expected_type=type_hints["failover_dr_replica_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failover_dr_replica_name is not None:
            self._values["failover_dr_replica_name"] = failover_dr_replica_name

    @builtins.property
    def failover_dr_replica_name(self) -> typing.Optional[builtins.str]:
        '''If the instance is a primary instance, then this field identifies the disaster recovery (DR) replica.

        The standard format of this field is "your-project:your-instance". You can also set this field to "your-instance", but cloud SQL backend will convert it to the aforementioned standard format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#failover_dr_replica_name SqlDatabaseInstance#failover_dr_replica_name}
        '''
        result = self._values.get("failover_dr_replica_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceReplicationCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceReplicationClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceReplicationClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f44a74a8c8600ba23ed7c7428e964c1d8c772975271feec8d146d0e590d6a768)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a7376d5808c67a679b7afe95e429028ab1b56a541e2608ded12e505f3341f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverDrReplicaName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SqlDatabaseInstanceReplicationCluster]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceReplicationCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceReplicationCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31684ca3158c7f26c975cc9cc57f796411fc4fa028c3dfb0be9bef1cc5a59f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceRestoreBackupContext",
    jsii_struct_bases=[],
    name_mapping={
        "backup_run_id": "backupRunId",
        "instance_id": "instanceId",
        "project": "project",
    },
)
class SqlDatabaseInstanceRestoreBackupContext:
    def __init__(
        self,
        *,
        backup_run_id: jsii.Number,
        instance_id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backup_run_id: The ID of the backup run to restore from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#backup_run_id SqlDatabaseInstance#backup_run_id}
        :param instance_id: The ID of the instance that the backup was taken from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#instance_id SqlDatabaseInstance#instance_id}
        :param project: The full project ID of the source instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#project SqlDatabaseInstance#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56be5af80cce82d2f7eb5040cab2b6898efbf0dd13061f2d63e05418e1ea4096)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#backup_run_id SqlDatabaseInstance#backup_run_id}
        '''
        result = self._values.get("backup_run_id")
        assert result is not None, "Required property 'backup_run_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the instance that the backup was taken from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#instance_id SqlDatabaseInstance#instance_id}
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The full project ID of the source instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#project SqlDatabaseInstance#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceRestoreBackupContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceRestoreBackupContextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceRestoreBackupContextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f681d2fedfb9a251b29158955bbb112b299e0bfc1db80e990ef67620823b4dc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f872fc6c2c6d08e99ba9e85f64c118cd04c322368da8aa19878d8dcb0ea0631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRunId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8832026024fce3e39b585588c7542e3fcc92b5925d58ae1cbebe81cece8af89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4133605125c858e77d61dbfcf9c4d079a7515f89c00d55e69f0ec92c4a6707ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceRestoreBackupContext]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceRestoreBackupContext], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceRestoreBackupContext],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f75815964f60b7081ed4a62bcdd31c35c42c3d42a9ad3c9009c1f6d93bbb0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceServerCaCert",
    jsii_struct_bases=[],
    name_mapping={},
)
class SqlDatabaseInstanceServerCaCert:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceServerCaCert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceServerCaCertList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceServerCaCertList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18580c5b4579137582bdcee8411a78861c880b4029567c026353767198ae9073)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SqlDatabaseInstanceServerCaCertOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c7d64cdd9f8dd4f4245aee088e3a14506fe3b1e062be2a972bcb9e43b6a9d7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SqlDatabaseInstanceServerCaCertOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7542de20feb2b9b2f4034c36e8ef63ae3cd46cd3137921fdd6190c46f8895381)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83c60bf2cccdca97c0fa8fefa6819a7b3abfadff95b769132ac6a10d4804721d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81c9fd62e9193ff5dc0be524b8a17aab9309e060bfd3ceffc3bee719bc1acf47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceServerCaCertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceServerCaCertOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69aa2a0c140c0f4513fbdbcbe2a900a6d96112bac44d2453b6b7d54ac7957088)
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
    def internal_value(self) -> typing.Optional[SqlDatabaseInstanceServerCaCert]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceServerCaCert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceServerCaCert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c1c858c8f1c2b4cb2901bd82f43b35c8c2fbc1802e7de951edf77ee899a427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettings",
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
class SqlDatabaseInstanceSettings:
    def __init__(
        self,
        *,
        tier: builtins.str,
        activation_policy: typing.Optional[builtins.str] = None,
        active_directory_config: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsActiveDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        advanced_machine_features: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        availability_type: typing.Optional[builtins.str] = None,
        backup_configuration: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsBackupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        collation: typing.Optional[builtins.str] = None,
        connection_pool_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlDatabaseInstanceSettingsConnectionPoolConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connector_enforcement: typing.Optional[builtins.str] = None,
        database_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlDatabaseInstanceSettingsDatabaseFlags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_cache_config: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsDataCacheConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deny_maintenance_period: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsDenyMaintenancePeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_autoresize: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_autoresize_limit: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        edition: typing.Optional[builtins.str] = None,
        enable_dataplex_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_google_ml_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        insights_config: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsInsightsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_configuration: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsIpConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        location_preference: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsLocationPreference", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_window: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        password_validation_policy: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsPasswordValidationPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        retain_backups_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sql_server_audit_config: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsSqlServerAuditConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param tier: The machine type to use. See tiers for more details and supported versions. Postgres supports only shared-core machine types, and custom machine types such as db-custom-2-13312. See the Custom Machine Type Documentation to learn about specifying custom machine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#tier SqlDatabaseInstance#tier}
        :param activation_policy: This specifies when the instance should be active. Can be either ALWAYS, NEVER or ON_DEMAND. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#activation_policy SqlDatabaseInstance#activation_policy}
        :param active_directory_config: active_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#active_directory_config SqlDatabaseInstance#active_directory_config}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#advanced_machine_features SqlDatabaseInstance#advanced_machine_features}
        :param availability_type: The availability type of the Cloud SQL instance, high availability (REGIONAL) or single zone (ZONAL). For all instances, ensure that settings.backup_configuration.enabled is set to true. For MySQL instances, ensure that settings.backup_configuration.binary_log_enabled is set to true. For Postgres instances, ensure that settings.backup_configuration.point_in_time_recovery_enabled is set to true. Defaults to ZONAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#availability_type SqlDatabaseInstance#availability_type}
        :param backup_configuration: backup_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#backup_configuration SqlDatabaseInstance#backup_configuration}
        :param collation: The name of server instance collation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#collation SqlDatabaseInstance#collation}
        :param connection_pool_config: connection_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#connection_pool_config SqlDatabaseInstance#connection_pool_config}
        :param connector_enforcement: Enables the enforcement of Cloud SQL Auth Proxy or Cloud SQL connectors for all the connections. If enabled, all the direct connections are rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#connector_enforcement SqlDatabaseInstance#connector_enforcement}
        :param database_flags: database_flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#database_flags SqlDatabaseInstance#database_flags}
        :param data_cache_config: data_cache_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#data_cache_config SqlDatabaseInstance#data_cache_config}
        :param deletion_protection_enabled: Configuration to protect against accidental instance deletion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#deletion_protection_enabled SqlDatabaseInstance#deletion_protection_enabled}
        :param deny_maintenance_period: deny_maintenance_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#deny_maintenance_period SqlDatabaseInstance#deny_maintenance_period}
        :param disk_autoresize: Enables auto-resizing of the storage size. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_autoresize SqlDatabaseInstance#disk_autoresize}
        :param disk_autoresize_limit: The maximum size, in GB, to which storage capacity can be automatically increased. The default value is 0, which specifies that there is no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_autoresize_limit SqlDatabaseInstance#disk_autoresize_limit}
        :param disk_size: The size of data disk, in GB. Size of a running instance cannot be reduced but can be increased. The minimum value is 10GB for PD_SSD, PD_HDD and 20GB for HYPERDISK_BALANCED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_size SqlDatabaseInstance#disk_size}
        :param disk_type: The type of supported data disk is tier dependent and can be PD_SSD or PD_HDD or HYPERDISK_BALANCED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_type SqlDatabaseInstance#disk_type}
        :param edition: The edition of the instance, can be ENTERPRISE or ENTERPRISE_PLUS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#edition SqlDatabaseInstance#edition}
        :param enable_dataplex_integration: Enables Dataplex Integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_dataplex_integration SqlDatabaseInstance#enable_dataplex_integration}
        :param enable_google_ml_integration: Enables Vertex AI Integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_google_ml_integration SqlDatabaseInstance#enable_google_ml_integration}
        :param insights_config: insights_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#insights_config SqlDatabaseInstance#insights_config}
        :param ip_configuration: ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ip_configuration SqlDatabaseInstance#ip_configuration}
        :param location_preference: location_preference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#location_preference SqlDatabaseInstance#location_preference}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#maintenance_window SqlDatabaseInstance#maintenance_window}
        :param password_validation_policy: password_validation_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#password_validation_policy SqlDatabaseInstance#password_validation_policy}
        :param pricing_plan: Pricing plan for this instance, can only be PER_USE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#pricing_plan SqlDatabaseInstance#pricing_plan}
        :param retain_backups_on_delete: When this parameter is set to true, Cloud SQL retains backups of the instance even after the instance is deleted. The ON_DEMAND backup will be retained until customer deletes the backup or the project. The AUTOMATED backup will be retained based on the backups retention setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retain_backups_on_delete SqlDatabaseInstance#retain_backups_on_delete}
        :param sql_server_audit_config: sql_server_audit_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#sql_server_audit_config SqlDatabaseInstance#sql_server_audit_config}
        :param time_zone: The time_zone to be used by the database engine (supported only for SQL Server), in SQL Server timezone format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#time_zone SqlDatabaseInstance#time_zone}
        :param user_labels: A set of key/value user label pairs to assign to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#user_labels SqlDatabaseInstance#user_labels}
        '''
        if isinstance(active_directory_config, dict):
            active_directory_config = SqlDatabaseInstanceSettingsActiveDirectoryConfig(**active_directory_config)
        if isinstance(advanced_machine_features, dict):
            advanced_machine_features = SqlDatabaseInstanceSettingsAdvancedMachineFeatures(**advanced_machine_features)
        if isinstance(backup_configuration, dict):
            backup_configuration = SqlDatabaseInstanceSettingsBackupConfiguration(**backup_configuration)
        if isinstance(data_cache_config, dict):
            data_cache_config = SqlDatabaseInstanceSettingsDataCacheConfig(**data_cache_config)
        if isinstance(deny_maintenance_period, dict):
            deny_maintenance_period = SqlDatabaseInstanceSettingsDenyMaintenancePeriod(**deny_maintenance_period)
        if isinstance(insights_config, dict):
            insights_config = SqlDatabaseInstanceSettingsInsightsConfig(**insights_config)
        if isinstance(ip_configuration, dict):
            ip_configuration = SqlDatabaseInstanceSettingsIpConfiguration(**ip_configuration)
        if isinstance(location_preference, dict):
            location_preference = SqlDatabaseInstanceSettingsLocationPreference(**location_preference)
        if isinstance(maintenance_window, dict):
            maintenance_window = SqlDatabaseInstanceSettingsMaintenanceWindow(**maintenance_window)
        if isinstance(password_validation_policy, dict):
            password_validation_policy = SqlDatabaseInstanceSettingsPasswordValidationPolicy(**password_validation_policy)
        if isinstance(sql_server_audit_config, dict):
            sql_server_audit_config = SqlDatabaseInstanceSettingsSqlServerAuditConfig(**sql_server_audit_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f4a325cfd642cd85ee31b029d619b2195a80301fae255d6fce8bf37b72c912)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#tier SqlDatabaseInstance#tier}
        '''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def activation_policy(self) -> typing.Optional[builtins.str]:
        '''This specifies when the instance should be active. Can be either ALWAYS, NEVER or ON_DEMAND.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#activation_policy SqlDatabaseInstance#activation_policy}
        '''
        result = self._values.get("activation_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def active_directory_config(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsActiveDirectoryConfig"]:
        '''active_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#active_directory_config SqlDatabaseInstance#active_directory_config}
        '''
        result = self._values.get("active_directory_config")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsActiveDirectoryConfig"], result)

    @builtins.property
    def advanced_machine_features(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsAdvancedMachineFeatures"]:
        '''advanced_machine_features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#advanced_machine_features SqlDatabaseInstance#advanced_machine_features}
        '''
        result = self._values.get("advanced_machine_features")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsAdvancedMachineFeatures"], result)

    @builtins.property
    def availability_type(self) -> typing.Optional[builtins.str]:
        '''The availability type of the Cloud SQL instance, high availability (REGIONAL) or single zone (ZONAL).

        For all instances, ensure that
        settings.backup_configuration.enabled is set to true.
        For MySQL instances, ensure that settings.backup_configuration.binary_log_enabled is set to true.
        For Postgres instances, ensure that settings.backup_configuration.point_in_time_recovery_enabled
        is set to true. Defaults to ZONAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#availability_type SqlDatabaseInstance#availability_type}
        '''
        result = self._values.get("availability_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_configuration(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsBackupConfiguration"]:
        '''backup_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#backup_configuration SqlDatabaseInstance#backup_configuration}
        '''
        result = self._values.get("backup_configuration")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsBackupConfiguration"], result)

    @builtins.property
    def collation(self) -> typing.Optional[builtins.str]:
        '''The name of server instance collation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#collation SqlDatabaseInstance#collation}
        '''
        result = self._values.get("collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_pool_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsConnectionPoolConfig"]]]:
        '''connection_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#connection_pool_config SqlDatabaseInstance#connection_pool_config}
        '''
        result = self._values.get("connection_pool_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsConnectionPoolConfig"]]], result)

    @builtins.property
    def connector_enforcement(self) -> typing.Optional[builtins.str]:
        '''Enables the enforcement of Cloud SQL Auth Proxy or Cloud SQL connectors for all the connections.

        If enabled, all the direct connections are rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#connector_enforcement SqlDatabaseInstance#connector_enforcement}
        '''
        result = self._values.get("connector_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_flags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsDatabaseFlags"]]]:
        '''database_flags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#database_flags SqlDatabaseInstance#database_flags}
        '''
        result = self._values.get("database_flags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsDatabaseFlags"]]], result)

    @builtins.property
    def data_cache_config(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsDataCacheConfig"]:
        '''data_cache_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#data_cache_config SqlDatabaseInstance#data_cache_config}
        '''
        result = self._values.get("data_cache_config")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsDataCacheConfig"], result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Configuration to protect against accidental instance deletion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#deletion_protection_enabled SqlDatabaseInstance#deletion_protection_enabled}
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deny_maintenance_period(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsDenyMaintenancePeriod"]:
        '''deny_maintenance_period block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#deny_maintenance_period SqlDatabaseInstance#deny_maintenance_period}
        '''
        result = self._values.get("deny_maintenance_period")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsDenyMaintenancePeriod"], result)

    @builtins.property
    def disk_autoresize(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables auto-resizing of the storage size. Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_autoresize SqlDatabaseInstance#disk_autoresize}
        '''
        result = self._values.get("disk_autoresize")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disk_autoresize_limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum size, in GB, to which storage capacity can be automatically increased.

        The default value is 0, which specifies that there is no limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_autoresize_limit SqlDatabaseInstance#disk_autoresize_limit}
        '''
        result = self._values.get("disk_autoresize_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        '''The size of data disk, in GB.

        Size of a running instance cannot be reduced but can be increased. The minimum value is 10GB for PD_SSD, PD_HDD and 20GB for HYPERDISK_BALANCED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_size SqlDatabaseInstance#disk_size}
        '''
        result = self._values.get("disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''The type of supported data disk is tier dependent and can be PD_SSD or PD_HDD or HYPERDISK_BALANCED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disk_type SqlDatabaseInstance#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''The edition of the instance, can be ENTERPRISE or ENTERPRISE_PLUS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#edition SqlDatabaseInstance#edition}
        '''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_dataplex_integration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Dataplex Integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_dataplex_integration SqlDatabaseInstance#enable_dataplex_integration}
        '''
        result = self._values.get("enable_dataplex_integration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_google_ml_integration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Vertex AI Integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_google_ml_integration SqlDatabaseInstance#enable_google_ml_integration}
        '''
        result = self._values.get("enable_google_ml_integration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def insights_config(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsInsightsConfig"]:
        '''insights_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#insights_config SqlDatabaseInstance#insights_config}
        '''
        result = self._values.get("insights_config")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsInsightsConfig"], result)

    @builtins.property
    def ip_configuration(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsIpConfiguration"]:
        '''ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ip_configuration SqlDatabaseInstance#ip_configuration}
        '''
        result = self._values.get("ip_configuration")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsIpConfiguration"], result)

    @builtins.property
    def location_preference(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsLocationPreference"]:
        '''location_preference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#location_preference SqlDatabaseInstance#location_preference}
        '''
        result = self._values.get("location_preference")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsLocationPreference"], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#maintenance_window SqlDatabaseInstance#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsMaintenanceWindow"], result)

    @builtins.property
    def password_validation_policy(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsPasswordValidationPolicy"]:
        '''password_validation_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#password_validation_policy SqlDatabaseInstance#password_validation_policy}
        '''
        result = self._values.get("password_validation_policy")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsPasswordValidationPolicy"], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''Pricing plan for this instance, can only be PER_USE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#pricing_plan SqlDatabaseInstance#pricing_plan}
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retain_backups_on_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When this parameter is set to true, Cloud SQL retains backups of the instance even after the instance is deleted.

        The ON_DEMAND backup will be retained until customer deletes the backup or the project. The AUTOMATED backup will be retained based on the backups retention setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retain_backups_on_delete SqlDatabaseInstance#retain_backups_on_delete}
        '''
        result = self._values.get("retain_backups_on_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sql_server_audit_config(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsSqlServerAuditConfig"]:
        '''sql_server_audit_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#sql_server_audit_config SqlDatabaseInstance#sql_server_audit_config}
        '''
        result = self._values.get("sql_server_audit_config")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsSqlServerAuditConfig"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time_zone to be used by the database engine (supported only for SQL Server), in SQL Server timezone format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#time_zone SqlDatabaseInstance#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value user label pairs to assign to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#user_labels SqlDatabaseInstance#user_labels}
        '''
        result = self._values.get("user_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsActiveDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain"},
)
class SqlDatabaseInstanceSettingsActiveDirectoryConfig:
    def __init__(self, *, domain: builtins.str) -> None:
        '''
        :param domain: Domain name of the Active Directory for SQL Server (e.g., mydomain.com). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#domain SqlDatabaseInstance#domain}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2dc813db5334b41b6f793c113709c729ad3c0f9b91a14c28239a46c2455f7ff)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
        }

    @builtins.property
    def domain(self) -> builtins.str:
        '''Domain name of the Active Directory for SQL Server (e.g., mydomain.com).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#domain SqlDatabaseInstance#domain}
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsActiveDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsActiveDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsActiveDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82c76f973fc6e7787abbccfb4753807c54eed8918c6b151cb30be50fabfdd396)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6df8b3f0061f030a5f92d02b65476c6678b4d26ba0ee8e61b49af2f64721b6f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsActiveDirectoryConfig]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsActiveDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsActiveDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc912ceeb0b5331a0d24f367a4fafe16eb8579ef5a7afa24a46d598117d15da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsAdvancedMachineFeatures",
    jsii_struct_bases=[],
    name_mapping={"threads_per_core": "threadsPerCore"},
)
class SqlDatabaseInstanceSettingsAdvancedMachineFeatures:
    def __init__(
        self,
        *,
        threads_per_core: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param threads_per_core: The number of threads per physical core. Can be 1 or 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#threads_per_core SqlDatabaseInstance#threads_per_core}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1cb33ed07dc41f1293082b18005f289220df93d700183d9b9442e714b48406)
            check_type(argname="argument threads_per_core", value=threads_per_core, expected_type=type_hints["threads_per_core"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if threads_per_core is not None:
            self._values["threads_per_core"] = threads_per_core

    @builtins.property
    def threads_per_core(self) -> typing.Optional[jsii.Number]:
        '''The number of threads per physical core. Can be 1 or 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#threads_per_core SqlDatabaseInstance#threads_per_core}
        '''
        result = self._values.get("threads_per_core")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsAdvancedMachineFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsAdvancedMachineFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsAdvancedMachineFeaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbff4b96835285c47646ad92bcdff28f8a8ea654662bbe4ffec9052a419e51fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4143403da535bb8a3af08073941d82856507f50d0beb91ab7f01713c0f204c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threadsPerCore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsAdvancedMachineFeatures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsAdvancedMachineFeatures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8066c411e11960fb03fe50099e3be4351d6ed5d4037201ceff4ce32c235142d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsBackupConfiguration",
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
class SqlDatabaseInstanceSettingsBackupConfiguration:
    def __init__(
        self,
        *,
        backup_retention_settings: typing.Optional[typing.Union["SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        binary_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        start_time: typing.Optional[builtins.str] = None,
        transaction_log_retention_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_retention_settings: backup_retention_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#backup_retention_settings SqlDatabaseInstance#backup_retention_settings}
        :param binary_log_enabled: True if binary logging is enabled. If settings.backup_configuration.enabled is false, this must be as well. Can only be used with MySQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#binary_log_enabled SqlDatabaseInstance#binary_log_enabled}
        :param enabled: True if backup configuration is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enabled SqlDatabaseInstance#enabled}
        :param location: Location of the backup configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#location SqlDatabaseInstance#location}
        :param point_in_time_recovery_enabled: True if Point-in-time recovery is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#point_in_time_recovery_enabled SqlDatabaseInstance#point_in_time_recovery_enabled}
        :param start_time: HH:MM format time indicating when backup configuration starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#start_time SqlDatabaseInstance#start_time}
        :param transaction_log_retention_days: The number of days of transaction logs we retain for point in time restore, from 1-7. (For PostgreSQL Enterprise Plus instances, from 1 to 35.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#transaction_log_retention_days SqlDatabaseInstance#transaction_log_retention_days}
        '''
        if isinstance(backup_retention_settings, dict):
            backup_retention_settings = SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings(**backup_retention_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49a68c70563937bcaeecea90fceec3d88c8d6aedfb82036fa7ae68ff3c206f2d)
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
    ) -> typing.Optional["SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings"]:
        '''backup_retention_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#backup_retention_settings SqlDatabaseInstance#backup_retention_settings}
        '''
        result = self._values.get("backup_retention_settings")
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings"], result)

    @builtins.property
    def binary_log_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if binary logging is enabled.

        If settings.backup_configuration.enabled is false, this must be as well. Can only be used with MySQL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#binary_log_enabled SqlDatabaseInstance#binary_log_enabled}
        '''
        result = self._values.get("binary_log_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if backup configuration is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enabled SqlDatabaseInstance#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Location of the backup configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#location SqlDatabaseInstance#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def point_in_time_recovery_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if Point-in-time recovery is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#point_in_time_recovery_enabled SqlDatabaseInstance#point_in_time_recovery_enabled}
        '''
        result = self._values.get("point_in_time_recovery_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''HH:MM format time indicating when backup configuration starts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#start_time SqlDatabaseInstance#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transaction_log_retention_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days of transaction logs we retain for point in time restore, from 1-7.

        (For PostgreSQL Enterprise Plus instances, from 1 to 35.)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#transaction_log_retention_days SqlDatabaseInstance#transaction_log_retention_days}
        '''
        result = self._values.get("transaction_log_retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsBackupConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings",
    jsii_struct_bases=[],
    name_mapping={
        "retained_backups": "retainedBackups",
        "retention_unit": "retentionUnit",
    },
)
class SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings:
    def __init__(
        self,
        *,
        retained_backups: jsii.Number,
        retention_unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param retained_backups: Number of backups to retain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retained_backups SqlDatabaseInstance#retained_backups}
        :param retention_unit: The unit that 'retainedBackups' represents. Defaults to COUNT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retention_unit SqlDatabaseInstance#retention_unit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c437328f320ab782a48f15f5c7f058b0b5e94f7a13331d236f2efa853ff1f4a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retained_backups SqlDatabaseInstance#retained_backups}
        '''
        result = self._values.get("retained_backups")
        assert result is not None, "Required property 'retained_backups' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def retention_unit(self) -> typing.Optional[builtins.str]:
        '''The unit that 'retainedBackups' represents. Defaults to COUNT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retention_unit SqlDatabaseInstance#retention_unit}
        '''
        result = self._values.get("retention_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed8605fa88b11df1e8d8025529e9e249bc8353d0ea93bcfa1b76ac1b7c797678)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a26c240f04f01584843ff0f4dafc2c957b3848481c31b348c20327f30b66ce77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainedBackups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionUnit")
    def retention_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionUnit"))

    @retention_unit.setter
    def retention_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37ac8880a6055b9875d613764ffe52b19e94c3c5cda7b948715e2d233da138b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bad84ee522cb598cb2afacf5438787f80039bbc2319c990b7b3648a50e9b2462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceSettingsBackupConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsBackupConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d452df95d3721dd4e482571c362ff3014359a001e4743c8ace46d512adb376b2)
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
        :param retained_backups: Number of backups to retain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retained_backups SqlDatabaseInstance#retained_backups}
        :param retention_unit: The unit that 'retainedBackups' represents. Defaults to COUNT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retention_unit SqlDatabaseInstance#retention_unit}
        '''
        value = SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings(
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
    ) -> SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsOutputReference:
        return typing.cast(SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsOutputReference, jsii.get(self, "backupRetentionSettings"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionSettingsInput")
    def backup_retention_settings_input(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings], jsii.get(self, "backupRetentionSettingsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3fc56a3ca1297119065f8798a3a37b9fadeb7128632cfdd67d8af2257481d890)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a75aa661c1d66c6309e0bb0d962c04204544fe53d6bd11aca0e43827335432ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f1e894c96cae6c79d52f35ff034e03f00210f0d10824adf8c6d595777915c56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5742b22d423e9abcdb4af41838778b0b26a2e720431c0c9fce647f935cefb8ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTimeRecoveryEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857c6c465f6022f0b59973874c3a2e1e1b823d2269db69ba70a4b55c372b9130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transactionLogRetentionDays")
    def transaction_log_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "transactionLogRetentionDays"))

    @transaction_log_retention_days.setter
    def transaction_log_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7817a974f7b40887e5a7779dc141924ead1d8a67c9ee219e45e598fb48938cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionLogRetentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsBackupConfiguration]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsBackupConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsBackupConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b62db911313134a30e41fa3a4d8d387e43f8b2eea288e1ed273feeca8d34515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsConnectionPoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connection_pooling_enabled": "connectionPoolingEnabled",
        "flags": "flags",
    },
)
class SqlDatabaseInstanceSettingsConnectionPoolConfig:
    def __init__(
        self,
        *,
        connection_pooling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlDatabaseInstanceSettingsConnectionPoolConfigFlags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection_pooling_enabled: Whether Managed Connection Pool is enabled for this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#connection_pooling_enabled SqlDatabaseInstance#connection_pooling_enabled}
        :param flags: flags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#flags SqlDatabaseInstance#flags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92237790b2079b4c1025c3a1bf1b82b6a4309bf3165c030fb4b895e13bf086b5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#connection_pooling_enabled SqlDatabaseInstance#connection_pooling_enabled}
        '''
        result = self._values.get("connection_pooling_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def flags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsConnectionPoolConfigFlags"]]]:
        '''flags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#flags SqlDatabaseInstance#flags}
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsConnectionPoolConfigFlags"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsConnectionPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsConnectionPoolConfigFlags",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class SqlDatabaseInstanceSettingsConnectionPoolConfigFlags:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Name of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#name SqlDatabaseInstance#name}
        :param value: Value of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#value SqlDatabaseInstance#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fbe2217aba68e8d41594134e546a69e4fb9ca5aba3cde8778a8f934f70d2518)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#name SqlDatabaseInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#value SqlDatabaseInstance#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsConnectionPoolConfigFlags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsConnectionPoolConfigFlagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsConnectionPoolConfigFlagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20f9eff8fa98a1216254a94732838088a2471fc936ade4ffb8a559db5bd83804)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SqlDatabaseInstanceSettingsConnectionPoolConfigFlagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b543bfdd4e682829d80321adf83bde67564175a834c13c62a9c26495dc61fc98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SqlDatabaseInstanceSettingsConnectionPoolConfigFlagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17300f4d54c8c1d434061cb9bf14ec261c5ada7787109f5d5b9b2bf99438470)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcd1a002d8b82e2bc9d2d38c6823b5f9cddf3f5d5f154ce3dc5a0e533bc75073)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9f487550e92495184fe736bfe1d289ffd9287d2a8dcd939e79ff0b53c17b520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4c7120a48d76cf3c47fee322ca3325883155b38b4d7397ddd906df21f202f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceSettingsConnectionPoolConfigFlagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsConnectionPoolConfigFlagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c07f4cd5eaf0000eb46edc77445abfe20a5aae3cff27d19f0ebe8071f73b845)
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
            type_hints = typing.get_type_hints(_typecheckingstub__729cc7241e16ca6704478789b3a573142ecd97efb4a7c000ee47786b33fbcc5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd8f4b118ae7771c0b78cae5c351b06a129ad95513b4e4fd46338428d2b8150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsConnectionPoolConfigFlags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsConnectionPoolConfigFlags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f684657c9a2c503ffe74e7c02fcb54a9d8cee54e26bc26bb60ba3ac5ca15e2c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceSettingsConnectionPoolConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsConnectionPoolConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__774fe5e14a4365b2907fc2db93a03563f8ffb7523cb9485a58d3e3e82fb15855)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SqlDatabaseInstanceSettingsConnectionPoolConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199d67dcf36d7363317ba050d57d4c1311223dd5414117bb88940453021474de)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SqlDatabaseInstanceSettingsConnectionPoolConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c67ecd994efd1993b393062fc9203769dec498ecd5284fa4c601077ec143809)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c639f437cca581e144a5d60eaf7df238d76954fabeb314d57e762ab3594c397)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d111bd9e568e3fdecfaa8d1f2de65d74a838a0f74b549bfd7a94460ccb2c256f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c08e7177cf27e13f61385122afb1d19a76d5348f89d1d4cffd9c015eddc1e3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceSettingsConnectionPoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsConnectionPoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b47747243ea45075b08a4479329d7b4a5526110dcfe71eb3219c2ca70b28cd4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFlags")
    def put_flags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsConnectionPoolConfigFlags, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c62f78a847ea4b01f81bcd2f09985782dd92d2261f294c35e82d289a318551d)
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
    def flags(self) -> SqlDatabaseInstanceSettingsConnectionPoolConfigFlagsList:
        return typing.cast(SqlDatabaseInstanceSettingsConnectionPoolConfigFlagsList, jsii.get(self, "flags"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]], jsii.get(self, "flagsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1dc3d0aa8568f8944445ea67b2d6ec20f00ba8d03dc7651918a1ed52070408cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionPoolingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsConnectionPoolConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsConnectionPoolConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsConnectionPoolConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee8bbaca696634d271c630f4c6f50ddf29cebd1f5519337c934d568fa03a2bf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsDataCacheConfig",
    jsii_struct_bases=[],
    name_mapping={"data_cache_enabled": "dataCacheEnabled"},
)
class SqlDatabaseInstanceSettingsDataCacheConfig:
    def __init__(
        self,
        *,
        data_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param data_cache_enabled: Whether data cache is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#data_cache_enabled SqlDatabaseInstance#data_cache_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0816fa3f3d36f57770772ea30ac2ed3633bb5a0f88f241b5416ebedfdd227e97)
            check_type(argname="argument data_cache_enabled", value=data_cache_enabled, expected_type=type_hints["data_cache_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_cache_enabled is not None:
            self._values["data_cache_enabled"] = data_cache_enabled

    @builtins.property
    def data_cache_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether data cache is enabled for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#data_cache_enabled SqlDatabaseInstance#data_cache_enabled}
        '''
        result = self._values.get("data_cache_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsDataCacheConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsDataCacheConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsDataCacheConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fe458e4b960fe5db0bcaafc47b8987fa02cc48364bef7b582fcc98be9207f1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ab74f77d53198a9011c28f99006cabee50a01ef7745a62d7b6f7cd0783c18c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataCacheEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsDataCacheConfig]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsDataCacheConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsDataCacheConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bde755d0d2f298f1d9f22fcf097ecb17511d558eae40d5cfc19d8acb486a8e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsDatabaseFlags",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class SqlDatabaseInstanceSettingsDatabaseFlags:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Name of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#name SqlDatabaseInstance#name}
        :param value: Value of the flag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#value SqlDatabaseInstance#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f33c9eab581d94610142bfe4047349dac9f80575bfdddd55cf645988b08e516)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#name SqlDatabaseInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the flag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#value SqlDatabaseInstance#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsDatabaseFlags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsDatabaseFlagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsDatabaseFlagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dcebd845cf94013faa6d087a9dccd309fbfba46e19e11ba7185b44be35cdc91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SqlDatabaseInstanceSettingsDatabaseFlagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7d49fd23b8df415535ad4d63b1f640d6acae4122ae6a14a5b153cbac5c48ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SqlDatabaseInstanceSettingsDatabaseFlagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aedfecb63055d272a86bc65b98b544266bbdc608c954a467cf9bc9242158d08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e15f011a0a3cce7ab8b049b7c7ca663009e103f7f6f5eca6c5515f5d34eef0f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b714259f437fa1bcbb21bb67b912b4ef052ac7d908401fc440f670acec4062a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsDatabaseFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsDatabaseFlags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsDatabaseFlags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff00e2c01ee0bd8855d56a92be371b5c96310595b198120508e200822d9bf27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceSettingsDatabaseFlagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsDatabaseFlagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92cdaeae6e8d8dfe23b030078caacebcd5151a0ee15584553e67e5a53d98081a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ea0fd2c05bf54fab568a56326afff8be822466c21a0e062ab5ad6f109a37019)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b57162a29fd61208d42db9a2b942caf5dca9f9961cac7a563d2c7d2ed592f7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsDatabaseFlags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsDatabaseFlags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsDatabaseFlags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e43f803320a1012d0ff76e7420bb3f31b38a06a3c41d6901fef12a7adf257a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsDenyMaintenancePeriod",
    jsii_struct_bases=[],
    name_mapping={"end_date": "endDate", "start_date": "startDate", "time": "time"},
)
class SqlDatabaseInstanceSettingsDenyMaintenancePeriod:
    def __init__(
        self,
        *,
        end_date: builtins.str,
        start_date: builtins.str,
        time: builtins.str,
    ) -> None:
        '''
        :param end_date: End date before which maintenance will not take place. The date is in format yyyy-mm-dd i.e., 2020-11-01, or mm-dd, i.e., 11-01 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#end_date SqlDatabaseInstance#end_date}
        :param start_date: Start date after which maintenance will not take place. The date is in format yyyy-mm-dd i.e., 2020-11-01, or mm-dd, i.e., 11-01 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#start_date SqlDatabaseInstance#start_date}
        :param time: Time in UTC when the "deny maintenance period" starts on start_date and ends on end_date. The time is in format: HH:mm:SS, i.e., 00:00:00 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#time SqlDatabaseInstance#time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090897c16ada1f62e0493a1c3d0bc0f376fdd8d67225b3396394383fc32b4aeb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#end_date SqlDatabaseInstance#end_date}
        '''
        result = self._values.get("end_date")
        assert result is not None, "Required property 'end_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_date(self) -> builtins.str:
        '''Start date after which maintenance will not take place.

        The date is in format yyyy-mm-dd i.e., 2020-11-01, or mm-dd, i.e., 11-01

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#start_date SqlDatabaseInstance#start_date}
        '''
        result = self._values.get("start_date")
        assert result is not None, "Required property 'start_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time(self) -> builtins.str:
        '''Time in UTC when the "deny maintenance period" starts on start_date and ends on end_date.

        The time is in format: HH:mm:SS, i.e., 00:00:00

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#time SqlDatabaseInstance#time}
        '''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsDenyMaintenancePeriod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsDenyMaintenancePeriodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsDenyMaintenancePeriodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff7fbfc0778662654c75e2f34a8c00fd90c20fef4d09bdcf095da72d1586bf58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b33658b971e41d6baf948f73bfa25c2537e41733b6b47bae4ad7ca05fe030c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startDate"))

    @start_date.setter
    def start_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4985d83cf42b1f7d219e2e99b3bf2378c9c15b73dc89012f74e6ebf1507ad38a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c1412b24f0d29832874407ab40c0537e332de0e2613026f5d7b244b8f8ff2d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsDenyMaintenancePeriod]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsDenyMaintenancePeriod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsDenyMaintenancePeriod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c173d75e64a84ccadca8b3a1370ff5b754c3d86d0f5d8a0643b4e6ec5beb969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsInsightsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "query_insights_enabled": "queryInsightsEnabled",
        "query_plans_per_minute": "queryPlansPerMinute",
        "query_string_length": "queryStringLength",
        "record_application_tags": "recordApplicationTags",
        "record_client_address": "recordClientAddress",
    },
)
class SqlDatabaseInstanceSettingsInsightsConfig:
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
        :param query_insights_enabled: True if Query Insights feature is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#query_insights_enabled SqlDatabaseInstance#query_insights_enabled}
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. Between 0 and 20. Default to 5. For Enterprise Plus instances, from 0 to 200. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#query_plans_per_minute SqlDatabaseInstance#query_plans_per_minute}
        :param query_string_length: Maximum query length stored in bytes. Between 256 and 4500. Default to 1024. For Enterprise Plus instances, from 1 to 1048576. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#query_string_length SqlDatabaseInstance#query_string_length}
        :param record_application_tags: True if Query Insights will record application tags from query when enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#record_application_tags SqlDatabaseInstance#record_application_tags}
        :param record_client_address: True if Query Insights will record client address when enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#record_client_address SqlDatabaseInstance#record_client_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bed2f49e117189d5f9c56d315b1d15369aac31e55f2d8b2c094185c9493394f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#query_insights_enabled SqlDatabaseInstance#query_insights_enabled}
        '''
        result = self._values.get("query_insights_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_plans_per_minute(self) -> typing.Optional[jsii.Number]:
        '''Number of query execution plans captured by Insights per minute for all queries combined.

        Between 0 and 20. Default to 5. For Enterprise Plus instances, from 0 to 200.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#query_plans_per_minute SqlDatabaseInstance#query_plans_per_minute}
        '''
        result = self._values.get("query_plans_per_minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def query_string_length(self) -> typing.Optional[jsii.Number]:
        '''Maximum query length stored in bytes.

        Between 256 and 4500. Default to 1024. For Enterprise Plus instances, from 1 to 1048576.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#query_string_length SqlDatabaseInstance#query_string_length}
        '''
        result = self._values.get("query_string_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def record_application_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if Query Insights will record application tags from query when enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#record_application_tags SqlDatabaseInstance#record_application_tags}
        '''
        result = self._values.get("record_application_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def record_client_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if Query Insights will record client address when enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#record_client_address SqlDatabaseInstance#record_client_address}
        '''
        result = self._values.get("record_client_address")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsInsightsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsInsightsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsInsightsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0a92fd2104396af417f6aa8da508d13fa99b7f98ff80cfc69793d8f2ca848f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6edf07748c884614ebcb7abe3e58e962ae469443b0d8d4c0190d854f787cda8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryInsightsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryPlansPerMinute")
    def query_plans_per_minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryPlansPerMinute"))

    @query_plans_per_minute.setter
    def query_plans_per_minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63464752be3851e035d8068793a2897c437243f14dbad748d74c995d6db07793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryPlansPerMinute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringLength")
    def query_string_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryStringLength"))

    @query_string_length.setter
    def query_string_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42a62494601d4e646045f5d968774cd6b6f0006eb9fbb5c847826b248095af7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c83fe561fe8c41a07462bc3ca95bd15e82971c3c343fd80c224d965eb89a9e28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19da9d1fff9c42ff6b1b013a5b9097d96a951df97a254d6dba7b9e332fdd943e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordClientAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsInsightsConfig]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsInsightsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsInsightsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65326ce7f968667837cdcfcc40ffe54fc0ee7ee119c498001ff0632278d1ae36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsIpConfiguration",
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
class SqlDatabaseInstanceSettingsIpConfiguration:
    def __init__(
        self,
        *,
        allocated_ip_range: typing.Optional[builtins.str] = None,
        authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_private_path_for_google_cloud_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ipv4_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_network: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlDatabaseInstanceSettingsIpConfigurationPscConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        server_ca_mode: typing.Optional[builtins.str] = None,
        server_ca_pool: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocated_ip_range: The name of the allocated ip range for the private ip CloudSQL instance. For example: "google-managed-services-default". If set, the instance ip will be created in the allocated range. The range name must comply with RFC 1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#allocated_ip_range SqlDatabaseInstance#allocated_ip_range}
        :param authorized_networks: authorized_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#authorized_networks SqlDatabaseInstance#authorized_networks}
        :param custom_subject_alternative_names: The custom subject alternative names for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#custom_subject_alternative_names SqlDatabaseInstance#custom_subject_alternative_names}
        :param enable_private_path_for_google_cloud_services: Whether Google Cloud services such as BigQuery are allowed to access data in this Cloud SQL instance over a private IP connection. SQLSERVER database type is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_private_path_for_google_cloud_services SqlDatabaseInstance#enable_private_path_for_google_cloud_services}
        :param ipv4_enabled: Whether this Cloud SQL instance should be assigned a public IPV4 address. At least ipv4_enabled must be enabled or a private_network must be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ipv4_enabled SqlDatabaseInstance#ipv4_enabled}
        :param private_network: The VPC network from which the Cloud SQL instance is accessible for private IP. For example, projects/myProject/global/networks/default. Specifying a network enables private IP. At least ipv4_enabled must be enabled or a private_network must be configured. This setting can be updated, but it cannot be removed after it is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#private_network SqlDatabaseInstance#private_network}
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#psc_config SqlDatabaseInstance#psc_config}
        :param server_ca_mode: Specify how the server certificate's Certificate Authority is hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#server_ca_mode SqlDatabaseInstance#server_ca_mode}
        :param server_ca_pool: The resource name of the server CA pool for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#server_ca_pool SqlDatabaseInstance#server_ca_pool}
        :param ssl_mode: Specify how SSL connection should be enforced in DB connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ssl_mode SqlDatabaseInstance#ssl_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe34d3ed763b412872746717e6789569095e9c8758a60c27990296d63b49bf6f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#allocated_ip_range SqlDatabaseInstance#allocated_ip_range}
        '''
        result = self._values.get("allocated_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorized_networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks"]]]:
        '''authorized_networks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#authorized_networks SqlDatabaseInstance#authorized_networks}
        '''
        result = self._values.get("authorized_networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks"]]], result)

    @builtins.property
    def custom_subject_alternative_names(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The custom subject alternative names for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#custom_subject_alternative_names SqlDatabaseInstance#custom_subject_alternative_names}
        '''
        result = self._values.get("custom_subject_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_private_path_for_google_cloud_services(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Google Cloud services such as BigQuery are allowed to access data in this Cloud SQL instance over a private IP connection.

        SQLSERVER database type is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_private_path_for_google_cloud_services SqlDatabaseInstance#enable_private_path_for_google_cloud_services}
        '''
        result = self._values.get("enable_private_path_for_google_cloud_services")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ipv4_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this Cloud SQL instance should be assigned a public IPV4 address.

        At least ipv4_enabled must be enabled or a private_network must be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ipv4_enabled SqlDatabaseInstance#ipv4_enabled}
        '''
        result = self._values.get("ipv4_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_network(self) -> typing.Optional[builtins.str]:
        '''The VPC network from which the Cloud SQL instance is accessible for private IP.

        For example, projects/myProject/global/networks/default. Specifying a network enables private IP. At least ipv4_enabled must be enabled or a private_network must be configured. This setting can be updated, but it cannot be removed after it is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#private_network SqlDatabaseInstance#private_network}
        '''
        result = self._values.get("private_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsIpConfigurationPscConfig"]]]:
        '''psc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#psc_config SqlDatabaseInstance#psc_config}
        '''
        result = self._values.get("psc_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsIpConfigurationPscConfig"]]], result)

    @builtins.property
    def server_ca_mode(self) -> typing.Optional[builtins.str]:
        '''Specify how the server certificate's Certificate Authority is hosted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#server_ca_mode SqlDatabaseInstance#server_ca_mode}
        '''
        result = self._values.get("server_ca_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_ca_pool(self) -> typing.Optional[builtins.str]:
        '''The resource name of the server CA pool for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#server_ca_pool SqlDatabaseInstance#server_ca_pool}
        '''
        result = self._values.get("server_ca_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        '''Specify how SSL connection should be enforced in DB connections.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ssl_mode SqlDatabaseInstance#ssl_mode}
        '''
        result = self._values.get("ssl_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "expiration_time": "expirationTime",
        "name": "name",
    },
)
class SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks:
    def __init__(
        self,
        *,
        value: builtins.str,
        expiration_time: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#value SqlDatabaseInstance#value}.
        :param expiration_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#expiration_time SqlDatabaseInstance#expiration_time}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#name SqlDatabaseInstance#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493097ffcbbc668070facbf3224a2c25ade663ab6ce0c24163f4d3aa948a44a2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#value SqlDatabaseInstance#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#expiration_time SqlDatabaseInstance#expiration_time}.'''
        result = self._values.get("expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#name SqlDatabaseInstance#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11688f84c0789065fe69658c84b88c538b470ebe38a896bdfb54b69b3ed1225a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a85e22e5188ec5e5abf00f763f2ac6b204d7067533c64a2f35aca539694c3e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54050e08a4c7c8ddad411cb8996cbcfa853c5567c23e2a7dfec2dc94e929b78f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f3bd6693b17730aab6e63b6f1660140328efefbc9ea8ae4e9add82e1cc4c10d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bf59539263b578951e89cabd8a61f5711bb792f8264c88f19348af6eec48e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcfab77f0ad2655e6c0073325aaf4e09e64303ce86e0ce995bede7fa0bf36340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1db14f8ce41e47399e1a02ce0e67051842e80e054455f0874de289377c3ec49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44bc40e06db86128a81e36206e2c1872c128d3c8a1255788c2017c549a85b9e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8b6e9c78977f7c567ebee093a7b39715bb15a3457b48c032eeeb91cdf2441c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348e999cbf6a8e9946a42e12aad35f01fc91905fc71eef481c1daaee1801f141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f202e17eb7dd0d85fc161967a44e019a844ab38b4cdbb7f701dba7ea4f80d3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceSettingsIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce6be414a9a15e1a9b78798ad407f2b94855f7d476bf0a70eeb303b7cc0cc1e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizedNetworks")
    def put_authorized_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9415cea5f3684e51964b92def458fe0ddafd3bb54eabf17be567fbbb0c6bfd05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthorizedNetworks", [value]))

    @jsii.member(jsii_name="putPscConfig")
    def put_psc_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlDatabaseInstanceSettingsIpConfigurationPscConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf6104b77d9fed4c07a1faa63b5eeffe7c1ef3329ad0f9d19cc050de5b4b241)
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
    ) -> SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksList:
        return typing.cast(SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksList, jsii.get(self, "authorizedNetworks"))

    @builtins.property
    @jsii.member(jsii_name="pscConfig")
    def psc_config(self) -> "SqlDatabaseInstanceSettingsIpConfigurationPscConfigList":
        return typing.cast("SqlDatabaseInstanceSettingsIpConfigurationPscConfigList", jsii.get(self, "pscConfig"))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpRangeInput")
    def allocated_ip_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allocatedIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedNetworksInput")
    def authorized_networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]], jsii.get(self, "authorizedNetworksInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsIpConfigurationPscConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsIpConfigurationPscConfig"]]], jsii.get(self, "pscConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9694848d5fb46ee76c4b0f449b1d6765f79586a7ab75f168a105ce3b4780f5a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ef633be7a24d758b0dc4ed2bfd5344e0b3ae26817ce22d1898ff09a304099be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64b7118c7aa16ecc004bbbf35af4c6f7db810327bbe31320c00304f20620b240)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30bd47e84cd47075552dde33568b0a622937b6a742b775d099014e17582504c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateNetwork")
    def private_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateNetwork"))

    @private_network.setter
    def private_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc8844662bbc2cb36509532e24571a5716c7074d441b99fb94ed24137f1dfe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverCaMode")
    def server_ca_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverCaMode"))

    @server_ca_mode.setter
    def server_ca_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc22a55a43fa503acd0851c52a126b14c76422744d30933ff3364a7b0b4e0e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCaMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverCaPool")
    def server_ca_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverCaPool"))

    @server_ca_pool.setter
    def server_ca_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5020f1c188eca2d8c037e8848df906774d19e4b066dd4293e685158f0b72d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCaPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslMode")
    def ssl_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslMode"))

    @ssl_mode.setter
    def ssl_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057cbe656b7c7c0898ccba23363b9514587101637858102b2d9ec5fec3f3191c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsIpConfiguration]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsIpConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsIpConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b5f7534567d021a92add2ab6673c105bb9f9912f34069d9e6a4e084c26ca45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsIpConfigurationPscConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_consumer_projects": "allowedConsumerProjects",
        "psc_auto_connections": "pscAutoConnections",
        "psc_enabled": "pscEnabled",
    },
)
class SqlDatabaseInstanceSettingsIpConfigurationPscConfig:
    def __init__(
        self,
        *,
        allowed_consumer_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
        psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_consumer_projects: List of consumer projects that are allow-listed for PSC connections to this instance. This instance can be connected to with PSC from any network in these projects. Each consumer project in this list may be represented by a project number (numeric) or by a project id (alphanumeric). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#allowed_consumer_projects SqlDatabaseInstance#allowed_consumer_projects}
        :param psc_auto_connections: psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#psc_auto_connections SqlDatabaseInstance#psc_auto_connections}
        :param psc_enabled: Whether PSC connectivity is enabled for this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#psc_enabled SqlDatabaseInstance#psc_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2640256bd9b56b6daf23679d6b26401fd77136c1208e9a5fb6ea236cb55e9599)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#allowed_consumer_projects SqlDatabaseInstance#allowed_consumer_projects}
        '''
        result = self._values.get("allowed_consumer_projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def psc_auto_connections(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections"]]]:
        '''psc_auto_connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#psc_auto_connections SqlDatabaseInstance#psc_auto_connections}
        '''
        result = self._values.get("psc_auto_connections")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections"]]], result)

    @builtins.property
    def psc_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether PSC connectivity is enabled for this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#psc_enabled SqlDatabaseInstance#psc_enabled}
        '''
        result = self._values.get("psc_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsIpConfigurationPscConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsIpConfigurationPscConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsIpConfigurationPscConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d9f027ee52dacdc064d1b9165b85d0009945d963b70554749ccd2ebdeea1902)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SqlDatabaseInstanceSettingsIpConfigurationPscConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc73937696db064a43dece13b79917e08e593621bae9042ca78f4e09e5e7c77f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SqlDatabaseInstanceSettingsIpConfigurationPscConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ecf85a6aa2efe13ced5ba46870bd4ba99a82d23b369c793009b54c0e8d2e7c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46ac68ac9957eb20c69183980dba360194bae1aef5e9acf8dfba2155acfe2c94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83463cb22b62d1f3f906ed49d749a8ec9bcadd3805fee3695abce85cef8e98e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationPscConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationPscConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationPscConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07b1f8b63b1853490119ee2f04179fb034c6dab232316bca99174b2a26fb139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceSettingsIpConfigurationPscConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsIpConfigurationPscConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__416c9d1c9222c79e0ba4b36e5360227af3c1c5030df124db4af0cf6e4510c990)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPscAutoConnections")
    def put_psc_auto_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83902193d635e0d0b95502a9f77cc7ad1f64a39d79002344183329874b8bf7e)
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
    ) -> "SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsList":
        return typing.cast("SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsList", jsii.get(self, "pscAutoConnections"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections"]]], jsii.get(self, "pscAutoConnectionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6c60b75d1c37477eef4ffe18930a3ce30b68bc0d230f3fe1f1a542b9bcde4dfc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b38f05a305c6f375b83f0f6ac26994f938537d9fcace8b40290b4854bc2e0e99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pscEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationPscConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationPscConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationPscConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487d16571b97454564d96c1a652b4b0e518d8ed02702eb83c37d02929d382ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_network": "consumerNetwork",
        "consumer_service_project_id": "consumerServiceProjectId",
    },
)
class SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections:
    def __init__(
        self,
        *,
        consumer_network: builtins.str,
        consumer_service_project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_network: The consumer network of this consumer endpoint. This must be a resource path that includes both the host project and the network name. The consumer host project of this network might be different from the consumer service project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#consumer_network SqlDatabaseInstance#consumer_network}
        :param consumer_service_project_id: The project ID of consumer service project of this consumer endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#consumer_service_project_id SqlDatabaseInstance#consumer_service_project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78dd6a3278c35476a3466c406b9ca8140188e51ec399a9135c90120bd08e8816)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#consumer_network SqlDatabaseInstance#consumer_network}
        '''
        result = self._values.get("consumer_network")
        assert result is not None, "Required property 'consumer_network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_service_project_id(self) -> typing.Optional[builtins.str]:
        '''The project ID of consumer service project of this consumer endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#consumer_service_project_id SqlDatabaseInstance#consumer_service_project_id}
        '''
        result = self._values.get("consumer_service_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb45318cf40bf74a9fba6a07411a00179088a4f9ab1f3bca512b5bb3e3af3d8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3c08fdfc29e67177ecf9c1c52fe0fcad61ddd58b1a3b5ac974f60b503243d7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375e21d4639f31d4bd08b81e12090f151d70b667819ab69ca1a10256cc68d580)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df2928634737577c9409ffc1051e1567947a27cb58913d57629adde1e81a5ddf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57b3c056b14e042ea22325cc5805305e7c0b55805daa802351dd043f5b962984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22118b152decaff1cea8219e393210c21b451ca0bc7715e5beb0c773929a402e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d4c846d81203277970dbc7b7b05bec6c916ce6ac217b2d52208194d137e955d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79adea3b1a99384d7b0ea635e2eb2486a7c9aac17344b45fdb1dd06528031fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerServiceProjectId")
    def consumer_service_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerServiceProjectId"))

    @consumer_service_project_id.setter
    def consumer_service_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a2c6317eb336983061d72e2b0e127cb81e02754ac5f4ab9ae4507e88abf94b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerServiceProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8c2491db7237939b14522745443974253a8b93c20a4ed6e648a35202a79392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsLocationPreference",
    jsii_struct_bases=[],
    name_mapping={
        "follow_gae_application": "followGaeApplication",
        "secondary_zone": "secondaryZone",
        "zone": "zone",
    },
)
class SqlDatabaseInstanceSettingsLocationPreference:
    def __init__(
        self,
        *,
        follow_gae_application: typing.Optional[builtins.str] = None,
        secondary_zone: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param follow_gae_application: A Google App Engine application whose zone to remain in. Must be in the same region as this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#follow_gae_application SqlDatabaseInstance#follow_gae_application}
        :param secondary_zone: The preferred Compute Engine zone for the secondary/failover. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#secondary_zone SqlDatabaseInstance#secondary_zone}
        :param zone: The preferred compute engine zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#zone SqlDatabaseInstance#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f86be3317e2511982cd4c025d816333e595012721bc8f24f35490d49f9dab4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#follow_gae_application SqlDatabaseInstance#follow_gae_application}
        '''
        result = self._values.get("follow_gae_application")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_zone(self) -> typing.Optional[builtins.str]:
        '''The preferred Compute Engine zone for the secondary/failover.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#secondary_zone SqlDatabaseInstance#secondary_zone}
        '''
        result = self._values.get("secondary_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The preferred compute engine zone.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#zone SqlDatabaseInstance#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsLocationPreference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsLocationPreferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsLocationPreferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3047bc8bda93621168d0ea91bf765f628d83e51befe654edc848868bd0cee046)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1d1368771c1692a133754068fdadb8aee3adf6d74b448c9e0755940aeacd77f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "followGaeApplication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryZone")
    def secondary_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryZone"))

    @secondary_zone.setter
    def secondary_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75adfde3c1856214e3a26c706baf3a4edac310fc05bbb7c288d8fbd8b4f4dffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4548300c6031cba53a952acd3097622beb1cbbab271b1565f66c7a1606d3bf0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsLocationPreference]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsLocationPreference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsLocationPreference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd8f9dbcaeecb3cc05da4a23ff5316ff3a00494f305d5a712cadf9f0320d92e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "hour": "hour", "update_track": "updateTrack"},
)
class SqlDatabaseInstanceSettingsMaintenanceWindow:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        hour: typing.Optional[jsii.Number] = None,
        update_track: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param day: Day of week (1-7), starting on Monday. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#day SqlDatabaseInstance#day}
        :param hour: Hour of day (0-23), ignored if day not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#hour SqlDatabaseInstance#hour}
        :param update_track: Receive updates after one week (canary) or after two weeks (stable) or after five weeks (week5) of notification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#update_track SqlDatabaseInstance#update_track}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d35185ac41cef3cc2bfa393b2082488a90e3829b756b23b10389d840d041b14)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#day SqlDatabaseInstance#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def hour(self) -> typing.Optional[jsii.Number]:
        '''Hour of day (0-23), ignored if day not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#hour SqlDatabaseInstance#hour}
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def update_track(self) -> typing.Optional[builtins.str]:
        '''Receive updates after one week (canary) or after two weeks (stable) or after five weeks (week5) of notification.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#update_track SqlDatabaseInstance#update_track}
        '''
        result = self._values.get("update_track")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c6129f4a50d9f0bdd9c7f62bd6b246872088f993bb7c4803883926933ce6708)
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
            type_hints = typing.get_type_hints(_typecheckingstub__245fae86da872ab833e25a951b05f8f263d8f6ad6be6ea23b3d2dd8ff8909af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hour")
    def hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hour"))

    @hour.setter
    def hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98914c0d8dc5590f99b33b950c0d03500b54f8aa4f6d537553c00aaff06b761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateTrack")
    def update_track(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTrack"))

    @update_track.setter
    def update_track(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8fe0b5e848be09826263d64bb6ece702c2e014a46a8c787546edd2fd7e067e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateTrack", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsMaintenanceWindow]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de855d1c6ea62869c6951a0b524f9450fde85a73bf5c1ee0d347e8ee92eb3ade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SqlDatabaseInstanceSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__875452f68abfc43b37a368a5a2f7405f63d1435bc384c1e0a1d707af08fc2c7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveDirectoryConfig")
    def put_active_directory_config(self, *, domain: builtins.str) -> None:
        '''
        :param domain: Domain name of the Active Directory for SQL Server (e.g., mydomain.com). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#domain SqlDatabaseInstance#domain}
        '''
        value = SqlDatabaseInstanceSettingsActiveDirectoryConfig(domain=domain)

        return typing.cast(None, jsii.invoke(self, "putActiveDirectoryConfig", [value]))

    @jsii.member(jsii_name="putAdvancedMachineFeatures")
    def put_advanced_machine_features(
        self,
        *,
        threads_per_core: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param threads_per_core: The number of threads per physical core. Can be 1 or 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#threads_per_core SqlDatabaseInstance#threads_per_core}
        '''
        value = SqlDatabaseInstanceSettingsAdvancedMachineFeatures(
            threads_per_core=threads_per_core
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedMachineFeatures", [value]))

    @jsii.member(jsii_name="putBackupConfiguration")
    def put_backup_configuration(
        self,
        *,
        backup_retention_settings: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        binary_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        location: typing.Optional[builtins.str] = None,
        point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        start_time: typing.Optional[builtins.str] = None,
        transaction_log_retention_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backup_retention_settings: backup_retention_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#backup_retention_settings SqlDatabaseInstance#backup_retention_settings}
        :param binary_log_enabled: True if binary logging is enabled. If settings.backup_configuration.enabled is false, this must be as well. Can only be used with MySQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#binary_log_enabled SqlDatabaseInstance#binary_log_enabled}
        :param enabled: True if backup configuration is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enabled SqlDatabaseInstance#enabled}
        :param location: Location of the backup configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#location SqlDatabaseInstance#location}
        :param point_in_time_recovery_enabled: True if Point-in-time recovery is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#point_in_time_recovery_enabled SqlDatabaseInstance#point_in_time_recovery_enabled}
        :param start_time: HH:MM format time indicating when backup configuration starts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#start_time SqlDatabaseInstance#start_time}
        :param transaction_log_retention_days: The number of days of transaction logs we retain for point in time restore, from 1-7. (For PostgreSQL Enterprise Plus instances, from 1 to 35.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#transaction_log_retention_days SqlDatabaseInstance#transaction_log_retention_days}
        '''
        value = SqlDatabaseInstanceSettingsBackupConfiguration(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsConnectionPoolConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a121a3d3b8836b174182407742c882a4d91f7718ed24d45f6f6bd5c1557c85b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnectionPoolConfig", [value]))

    @jsii.member(jsii_name="putDatabaseFlags")
    def put_database_flags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsDatabaseFlags, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20bc64a87ae189957c1ddcca38fd0bd3f088f0046f459d1d5683e15da73b7910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDatabaseFlags", [value]))

    @jsii.member(jsii_name="putDataCacheConfig")
    def put_data_cache_config(
        self,
        *,
        data_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param data_cache_enabled: Whether data cache is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#data_cache_enabled SqlDatabaseInstance#data_cache_enabled}
        '''
        value = SqlDatabaseInstanceSettingsDataCacheConfig(
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
        :param end_date: End date before which maintenance will not take place. The date is in format yyyy-mm-dd i.e., 2020-11-01, or mm-dd, i.e., 11-01 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#end_date SqlDatabaseInstance#end_date}
        :param start_date: Start date after which maintenance will not take place. The date is in format yyyy-mm-dd i.e., 2020-11-01, or mm-dd, i.e., 11-01 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#start_date SqlDatabaseInstance#start_date}
        :param time: Time in UTC when the "deny maintenance period" starts on start_date and ends on end_date. The time is in format: HH:mm:SS, i.e., 00:00:00 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#time SqlDatabaseInstance#time}
        '''
        value = SqlDatabaseInstanceSettingsDenyMaintenancePeriod(
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
        :param query_insights_enabled: True if Query Insights feature is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#query_insights_enabled SqlDatabaseInstance#query_insights_enabled}
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. Between 0 and 20. Default to 5. For Enterprise Plus instances, from 0 to 200. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#query_plans_per_minute SqlDatabaseInstance#query_plans_per_minute}
        :param query_string_length: Maximum query length stored in bytes. Between 256 and 4500. Default to 1024. For Enterprise Plus instances, from 1 to 1048576. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#query_string_length SqlDatabaseInstance#query_string_length}
        :param record_application_tags: True if Query Insights will record application tags from query when enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#record_application_tags SqlDatabaseInstance#record_application_tags}
        :param record_client_address: True if Query Insights will record client address when enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#record_client_address SqlDatabaseInstance#record_client_address}
        '''
        value = SqlDatabaseInstanceSettingsInsightsConfig(
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
        authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_private_path_for_google_cloud_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ipv4_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_network: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsIpConfigurationPscConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
        server_ca_mode: typing.Optional[builtins.str] = None,
        server_ca_pool: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocated_ip_range: The name of the allocated ip range for the private ip CloudSQL instance. For example: "google-managed-services-default". If set, the instance ip will be created in the allocated range. The range name must comply with RFC 1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#allocated_ip_range SqlDatabaseInstance#allocated_ip_range}
        :param authorized_networks: authorized_networks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#authorized_networks SqlDatabaseInstance#authorized_networks}
        :param custom_subject_alternative_names: The custom subject alternative names for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#custom_subject_alternative_names SqlDatabaseInstance#custom_subject_alternative_names}
        :param enable_private_path_for_google_cloud_services: Whether Google Cloud services such as BigQuery are allowed to access data in this Cloud SQL instance over a private IP connection. SQLSERVER database type is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_private_path_for_google_cloud_services SqlDatabaseInstance#enable_private_path_for_google_cloud_services}
        :param ipv4_enabled: Whether this Cloud SQL instance should be assigned a public IPV4 address. At least ipv4_enabled must be enabled or a private_network must be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ipv4_enabled SqlDatabaseInstance#ipv4_enabled}
        :param private_network: The VPC network from which the Cloud SQL instance is accessible for private IP. For example, projects/myProject/global/networks/default. Specifying a network enables private IP. At least ipv4_enabled must be enabled or a private_network must be configured. This setting can be updated, but it cannot be removed after it is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#private_network SqlDatabaseInstance#private_network}
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#psc_config SqlDatabaseInstance#psc_config}
        :param server_ca_mode: Specify how the server certificate's Certificate Authority is hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#server_ca_mode SqlDatabaseInstance#server_ca_mode}
        :param server_ca_pool: The resource name of the server CA pool for an instance with "CUSTOMER_MANAGED_CAS_CA" as the "server_ca_mode". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#server_ca_pool SqlDatabaseInstance#server_ca_pool}
        :param ssl_mode: Specify how SSL connection should be enforced in DB connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#ssl_mode SqlDatabaseInstance#ssl_mode}
        '''
        value = SqlDatabaseInstanceSettingsIpConfiguration(
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
        :param follow_gae_application: A Google App Engine application whose zone to remain in. Must be in the same region as this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#follow_gae_application SqlDatabaseInstance#follow_gae_application}
        :param secondary_zone: The preferred Compute Engine zone for the secondary/failover. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#secondary_zone SqlDatabaseInstance#secondary_zone}
        :param zone: The preferred compute engine zone. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#zone SqlDatabaseInstance#zone}
        '''
        value = SqlDatabaseInstanceSettingsLocationPreference(
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
        :param day: Day of week (1-7), starting on Monday. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#day SqlDatabaseInstance#day}
        :param hour: Hour of day (0-23), ignored if day not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#hour SqlDatabaseInstance#hour}
        :param update_track: Receive updates after one week (canary) or after two weeks (stable) or after five weeks (week5) of notification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#update_track SqlDatabaseInstance#update_track}
        '''
        value = SqlDatabaseInstanceSettingsMaintenanceWindow(
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
        :param enable_password_policy: Whether the password policy is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_password_policy SqlDatabaseInstance#enable_password_policy}
        :param complexity: Password complexity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#complexity SqlDatabaseInstance#complexity}
        :param disallow_username_substring: Disallow username as a part of the password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disallow_username_substring SqlDatabaseInstance#disallow_username_substring}
        :param min_length: Minimum number of characters allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#min_length SqlDatabaseInstance#min_length}
        :param password_change_interval: Minimum interval after which the password can be changed. This flag is only supported for PostgresSQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#password_change_interval SqlDatabaseInstance#password_change_interval}
        :param reuse_interval: Number of previous passwords that cannot be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#reuse_interval SqlDatabaseInstance#reuse_interval}
        '''
        value = SqlDatabaseInstanceSettingsPasswordValidationPolicy(
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
        :param bucket: The name of the destination bucket (e.g., gs://mybucket). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#bucket SqlDatabaseInstance#bucket}
        :param retention_interval: How long to keep generated audit files. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retention_interval SqlDatabaseInstance#retention_interval}
        :param upload_interval: How often to upload generated audit files. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#upload_interval SqlDatabaseInstance#upload_interval}
        '''
        value = SqlDatabaseInstanceSettingsSqlServerAuditConfig(
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
    ) -> SqlDatabaseInstanceSettingsActiveDirectoryConfigOutputReference:
        return typing.cast(SqlDatabaseInstanceSettingsActiveDirectoryConfigOutputReference, jsii.get(self, "activeDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedMachineFeatures")
    def advanced_machine_features(
        self,
    ) -> SqlDatabaseInstanceSettingsAdvancedMachineFeaturesOutputReference:
        return typing.cast(SqlDatabaseInstanceSettingsAdvancedMachineFeaturesOutputReference, jsii.get(self, "advancedMachineFeatures"))

    @builtins.property
    @jsii.member(jsii_name="backupConfiguration")
    def backup_configuration(
        self,
    ) -> SqlDatabaseInstanceSettingsBackupConfigurationOutputReference:
        return typing.cast(SqlDatabaseInstanceSettingsBackupConfigurationOutputReference, jsii.get(self, "backupConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="connectionPoolConfig")
    def connection_pool_config(
        self,
    ) -> SqlDatabaseInstanceSettingsConnectionPoolConfigList:
        return typing.cast(SqlDatabaseInstanceSettingsConnectionPoolConfigList, jsii.get(self, "connectionPoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="databaseFlags")
    def database_flags(self) -> SqlDatabaseInstanceSettingsDatabaseFlagsList:
        return typing.cast(SqlDatabaseInstanceSettingsDatabaseFlagsList, jsii.get(self, "databaseFlags"))

    @builtins.property
    @jsii.member(jsii_name="dataCacheConfig")
    def data_cache_config(
        self,
    ) -> SqlDatabaseInstanceSettingsDataCacheConfigOutputReference:
        return typing.cast(SqlDatabaseInstanceSettingsDataCacheConfigOutputReference, jsii.get(self, "dataCacheConfig"))

    @builtins.property
    @jsii.member(jsii_name="denyMaintenancePeriod")
    def deny_maintenance_period(
        self,
    ) -> SqlDatabaseInstanceSettingsDenyMaintenancePeriodOutputReference:
        return typing.cast(SqlDatabaseInstanceSettingsDenyMaintenancePeriodOutputReference, jsii.get(self, "denyMaintenancePeriod"))

    @builtins.property
    @jsii.member(jsii_name="insightsConfig")
    def insights_config(
        self,
    ) -> SqlDatabaseInstanceSettingsInsightsConfigOutputReference:
        return typing.cast(SqlDatabaseInstanceSettingsInsightsConfigOutputReference, jsii.get(self, "insightsConfig"))

    @builtins.property
    @jsii.member(jsii_name="ipConfiguration")
    def ip_configuration(
        self,
    ) -> SqlDatabaseInstanceSettingsIpConfigurationOutputReference:
        return typing.cast(SqlDatabaseInstanceSettingsIpConfigurationOutputReference, jsii.get(self, "ipConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="locationPreference")
    def location_preference(
        self,
    ) -> SqlDatabaseInstanceSettingsLocationPreferenceOutputReference:
        return typing.cast(SqlDatabaseInstanceSettingsLocationPreferenceOutputReference, jsii.get(self, "locationPreference"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> SqlDatabaseInstanceSettingsMaintenanceWindowOutputReference:
        return typing.cast(SqlDatabaseInstanceSettingsMaintenanceWindowOutputReference, jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="passwordValidationPolicy")
    def password_validation_policy(
        self,
    ) -> "SqlDatabaseInstanceSettingsPasswordValidationPolicyOutputReference":
        return typing.cast("SqlDatabaseInstanceSettingsPasswordValidationPolicyOutputReference", jsii.get(self, "passwordValidationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="sqlServerAuditConfig")
    def sql_server_audit_config(
        self,
    ) -> "SqlDatabaseInstanceSettingsSqlServerAuditConfigOutputReference":
        return typing.cast("SqlDatabaseInstanceSettingsSqlServerAuditConfigOutputReference", jsii.get(self, "sqlServerAuditConfig"))

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
    ) -> typing.Optional[SqlDatabaseInstanceSettingsActiveDirectoryConfig]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsActiveDirectoryConfig], jsii.get(self, "activeDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedMachineFeaturesInput")
    def advanced_machine_features_input(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsAdvancedMachineFeatures], jsii.get(self, "advancedMachineFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityTypeInput")
    def availability_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="backupConfigurationInput")
    def backup_configuration_input(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsBackupConfiguration]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsBackupConfiguration], jsii.get(self, "backupConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="collationInput")
    def collation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collationInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionPoolConfigInput")
    def connection_pool_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfig]]], jsii.get(self, "connectionPoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorEnforcementInput")
    def connector_enforcement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorEnforcementInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseFlagsInput")
    def database_flags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsDatabaseFlags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsDatabaseFlags]]], jsii.get(self, "databaseFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCacheConfigInput")
    def data_cache_config_input(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsDataCacheConfig]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsDataCacheConfig], jsii.get(self, "dataCacheConfigInput"))

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
    ) -> typing.Optional[SqlDatabaseInstanceSettingsDenyMaintenancePeriod]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsDenyMaintenancePeriod], jsii.get(self, "denyMaintenancePeriodInput"))

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
    ) -> typing.Optional[SqlDatabaseInstanceSettingsInsightsConfig]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsInsightsConfig], jsii.get(self, "insightsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="ipConfigurationInput")
    def ip_configuration_input(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsIpConfiguration]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsIpConfiguration], jsii.get(self, "ipConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="locationPreferenceInput")
    def location_preference_input(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsLocationPreference]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsLocationPreference], jsii.get(self, "locationPreferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsMaintenanceWindow]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsMaintenanceWindow], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordValidationPolicyInput")
    def password_validation_policy_input(
        self,
    ) -> typing.Optional["SqlDatabaseInstanceSettingsPasswordValidationPolicy"]:
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsPasswordValidationPolicy"], jsii.get(self, "passwordValidationPolicyInput"))

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
    ) -> typing.Optional["SqlDatabaseInstanceSettingsSqlServerAuditConfig"]:
        return typing.cast(typing.Optional["SqlDatabaseInstanceSettingsSqlServerAuditConfig"], jsii.get(self, "sqlServerAuditConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4e772d1d6370147013505656601369ef9374c72c9ab24d15f5492e4ba36beaf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityType")
    def availability_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityType"))

    @availability_type.setter
    def availability_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9254da10a68c5e19adf3afabb78a305ae25205ed56aa18b3026c8ad5bd110bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collation")
    def collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collation"))

    @collation.setter
    def collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be6c5084df2a00497ab7417cf890bf8e81044b1792fc028cb4519bcb3df82d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorEnforcement")
    def connector_enforcement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorEnforcement"))

    @connector_enforcement.setter
    def connector_enforcement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40767dcbdc6a299604592a341f0f2c160c0acf6841689e9b5730d022c27beeef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorEnforcement", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__cb02edb36ebb5fc05256af7427f6e7ebe3dda37696e092a73304e5b2b6adc1b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63a3965a87b0349a527a8f6e9934e940f06fc30f157827355871de0b128addd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskAutoresize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskAutoresizeLimit")
    def disk_autoresize_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskAutoresizeLimit"))

    @disk_autoresize_limit.setter
    def disk_autoresize_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b007f113398962e29f78ca9d34e52f95870a2846180feb6758f7218e3a28b651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskAutoresizeLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSize")
    def disk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSize"))

    @disk_size.setter
    def disk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2007981e8125814b6507ab8b2e3e213230524c365774d819681345fb391fded5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e17d33a4f683397c1af23955fb3dc4ffbbb2ac8c31195053079dc81ab1b78fec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d8c14856c022f11fee7425537252e109a8c48ebb816094f96fd9c5c89d82a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea496dacc89a66bc231753205e32a06e2bd792e4463be0c777b2c2eee048cd86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77dfcd24945f62226ff0346242bc0afabc771bdfacfe6ed3350972e0089bf97a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableGoogleMlIntegration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pricingPlan")
    def pricing_plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pricingPlan"))

    @pricing_plan.setter
    def pricing_plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa79e08decf7592a1470d2a894f1d680d58bfa22f40e15d6b5e92a8c07282aba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60cd073b046e77657d7b0924a56800a96afa268fd20e1c485e898a885cdf3c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainBackupsOnDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b5893ffefe72c3731ea82fef2f1464288d1b44b617bfeb25221c0a560f5da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d230f9eee67efc382159d7cee6b5896a5930c99b4f8f463066f1c0dbcf148e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userLabels")
    def user_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "userLabels"))

    @user_labels.setter
    def user_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be38c31184ff9ef10361b9e0d92a020e0a2224a9406fa589d754413a701c2fd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SqlDatabaseInstanceSettings]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7d3cc1ef0d35d7cba8b05d83dc3104f99d3d02a7fc9e90551bcae3e5fc8862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsPasswordValidationPolicy",
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
class SqlDatabaseInstanceSettingsPasswordValidationPolicy:
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
        :param enable_password_policy: Whether the password policy is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_password_policy SqlDatabaseInstance#enable_password_policy}
        :param complexity: Password complexity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#complexity SqlDatabaseInstance#complexity}
        :param disallow_username_substring: Disallow username as a part of the password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disallow_username_substring SqlDatabaseInstance#disallow_username_substring}
        :param min_length: Minimum number of characters allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#min_length SqlDatabaseInstance#min_length}
        :param password_change_interval: Minimum interval after which the password can be changed. This flag is only supported for PostgresSQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#password_change_interval SqlDatabaseInstance#password_change_interval}
        :param reuse_interval: Number of previous passwords that cannot be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#reuse_interval SqlDatabaseInstance#reuse_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28436dec1d60e5f9f162e49cc6b33a6185162fa967411e897985df6c246ff42f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#enable_password_policy SqlDatabaseInstance#enable_password_policy}
        '''
        result = self._values.get("enable_password_policy")
        assert result is not None, "Required property 'enable_password_policy' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def complexity(self) -> typing.Optional[builtins.str]:
        '''Password complexity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#complexity SqlDatabaseInstance#complexity}
        '''
        result = self._values.get("complexity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disallow_username_substring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disallow username as a part of the password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#disallow_username_substring SqlDatabaseInstance#disallow_username_substring}
        '''
        result = self._values.get("disallow_username_substring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of characters allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#min_length SqlDatabaseInstance#min_length}
        '''
        result = self._values.get("min_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_change_interval(self) -> typing.Optional[builtins.str]:
        '''Minimum interval after which the password can be changed. This flag is only supported for PostgresSQL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#password_change_interval SqlDatabaseInstance#password_change_interval}
        '''
        result = self._values.get("password_change_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reuse_interval(self) -> typing.Optional[jsii.Number]:
        '''Number of previous passwords that cannot be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#reuse_interval SqlDatabaseInstance#reuse_interval}
        '''
        result = self._values.get("reuse_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsPasswordValidationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsPasswordValidationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsPasswordValidationPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60e936be047fd46816da3fbf265a8248e20719a098890ad983d10a4ead38d832)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad39ec2588953874a3c9cc3165b1cb0fd9120539f75578e81b68179d90f1061b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb66254177e4a10a58c87bdb8f907bce692131f13d5d503bcd6ead726d145615)
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
            type_hints = typing.get_type_hints(_typecheckingstub__699637a351236547ff4560ef86788be1409adcc7b4e47f3eac5797aebcf435a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePasswordPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minLength")
    def min_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLength"))

    @min_length.setter
    def min_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd1f54bf9dde4c1617f644f3185793aeaa64f0a129c5857518bc504b924ab0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordChangeInterval")
    def password_change_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordChangeInterval"))

    @password_change_interval.setter
    def password_change_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0307a18889a93bb897466793069056321fd4613a72939caf107cd8bb4348394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordChangeInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reuseInterval")
    def reuse_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reuseInterval"))

    @reuse_interval.setter
    def reuse_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3646c23f752449980ea4087b662a1ec375f06961caafdc099b2865713b6c04c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reuseInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsPasswordValidationPolicy]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsPasswordValidationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsPasswordValidationPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c0b2a3a80de085f382957f58bf500b2cc3d893ea5dbed8f7218134772cecb70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsSqlServerAuditConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "retention_interval": "retentionInterval",
        "upload_interval": "uploadInterval",
    },
)
class SqlDatabaseInstanceSettingsSqlServerAuditConfig:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        retention_interval: typing.Optional[builtins.str] = None,
        upload_interval: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: The name of the destination bucket (e.g., gs://mybucket). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#bucket SqlDatabaseInstance#bucket}
        :param retention_interval: How long to keep generated audit files. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retention_interval SqlDatabaseInstance#retention_interval}
        :param upload_interval: How often to upload generated audit files. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#upload_interval SqlDatabaseInstance#upload_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f686c7c43a1fb76874801d8098be57364ca5bb30e5949d71798b54882810543f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#bucket SqlDatabaseInstance#bucket}
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_interval(self) -> typing.Optional[builtins.str]:
        '''How long to keep generated audit files.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s"..

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#retention_interval SqlDatabaseInstance#retention_interval}
        '''
        result = self._values.get("retention_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upload_interval(self) -> typing.Optional[builtins.str]:
        '''How often to upload generated audit files.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#upload_interval SqlDatabaseInstance#upload_interval}
        '''
        result = self._values.get("upload_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceSettingsSqlServerAuditConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceSettingsSqlServerAuditConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceSettingsSqlServerAuditConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d71a8d0bcebc884ec098fc18a6921006ed4b0d041ad660a39a87f91b5363e99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6ffb7afe95d7cc7b66b9365a24a8d33f68af17d5ec1772200d7bbfdefa40fcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionInterval")
    def retention_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionInterval"))

    @retention_interval.setter
    def retention_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091f4c32885beda4e0a3125c0fed1b4e24c415807517d754024732fb06d42257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uploadInterval")
    def upload_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uploadInterval"))

    @upload_interval.setter
    def upload_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da68f9ae4b3e7bd09d6d107d7b33642570d795c4f0930c3f666af03d3bb9bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uploadInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlDatabaseInstanceSettingsSqlServerAuditConfig]:
        return typing.cast(typing.Optional[SqlDatabaseInstanceSettingsSqlServerAuditConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlDatabaseInstanceSettingsSqlServerAuditConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd593ffff4a9c7cd205381d15d57bf80097904bff80ef9983c5517b374f82885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SqlDatabaseInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#create SqlDatabaseInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#delete SqlDatabaseInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#update SqlDatabaseInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24a64a305fcb158dc6d64df2c3fe6537f65d81e49b17b621e8712c723b86b12)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#create SqlDatabaseInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#delete SqlDatabaseInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/sql_database_instance#update SqlDatabaseInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlDatabaseInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlDatabaseInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.sqlDatabaseInstance.SqlDatabaseInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61cec9df86c3e9d2505ad08c310220923702d54d122b858ed0ce4efa3e6fe380)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4084c800d24f844098125b97939622092f799c245583a85b30a0ae4f3e1b33ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__738460a243fcd707e237992dd199e854b9cd586342f1e4d89e8b3f27d99a1b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f226ad1d8a02dbd1e0dfe84a4018d932c92bbf34242431e9d5de0d37344333b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb1997a2b28421989d2083f3387841745e95628b5c16fc56568ff3064302f85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SqlDatabaseInstance",
    "SqlDatabaseInstanceClone",
    "SqlDatabaseInstanceCloneOutputReference",
    "SqlDatabaseInstanceConfig",
    "SqlDatabaseInstanceDnsNames",
    "SqlDatabaseInstanceDnsNamesList",
    "SqlDatabaseInstanceDnsNamesOutputReference",
    "SqlDatabaseInstanceIpAddress",
    "SqlDatabaseInstanceIpAddressList",
    "SqlDatabaseInstanceIpAddressOutputReference",
    "SqlDatabaseInstanceReplicaConfiguration",
    "SqlDatabaseInstanceReplicaConfigurationOutputReference",
    "SqlDatabaseInstanceReplicationCluster",
    "SqlDatabaseInstanceReplicationClusterOutputReference",
    "SqlDatabaseInstanceRestoreBackupContext",
    "SqlDatabaseInstanceRestoreBackupContextOutputReference",
    "SqlDatabaseInstanceServerCaCert",
    "SqlDatabaseInstanceServerCaCertList",
    "SqlDatabaseInstanceServerCaCertOutputReference",
    "SqlDatabaseInstanceSettings",
    "SqlDatabaseInstanceSettingsActiveDirectoryConfig",
    "SqlDatabaseInstanceSettingsActiveDirectoryConfigOutputReference",
    "SqlDatabaseInstanceSettingsAdvancedMachineFeatures",
    "SqlDatabaseInstanceSettingsAdvancedMachineFeaturesOutputReference",
    "SqlDatabaseInstanceSettingsBackupConfiguration",
    "SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings",
    "SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettingsOutputReference",
    "SqlDatabaseInstanceSettingsBackupConfigurationOutputReference",
    "SqlDatabaseInstanceSettingsConnectionPoolConfig",
    "SqlDatabaseInstanceSettingsConnectionPoolConfigFlags",
    "SqlDatabaseInstanceSettingsConnectionPoolConfigFlagsList",
    "SqlDatabaseInstanceSettingsConnectionPoolConfigFlagsOutputReference",
    "SqlDatabaseInstanceSettingsConnectionPoolConfigList",
    "SqlDatabaseInstanceSettingsConnectionPoolConfigOutputReference",
    "SqlDatabaseInstanceSettingsDataCacheConfig",
    "SqlDatabaseInstanceSettingsDataCacheConfigOutputReference",
    "SqlDatabaseInstanceSettingsDatabaseFlags",
    "SqlDatabaseInstanceSettingsDatabaseFlagsList",
    "SqlDatabaseInstanceSettingsDatabaseFlagsOutputReference",
    "SqlDatabaseInstanceSettingsDenyMaintenancePeriod",
    "SqlDatabaseInstanceSettingsDenyMaintenancePeriodOutputReference",
    "SqlDatabaseInstanceSettingsInsightsConfig",
    "SqlDatabaseInstanceSettingsInsightsConfigOutputReference",
    "SqlDatabaseInstanceSettingsIpConfiguration",
    "SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks",
    "SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksList",
    "SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworksOutputReference",
    "SqlDatabaseInstanceSettingsIpConfigurationOutputReference",
    "SqlDatabaseInstanceSettingsIpConfigurationPscConfig",
    "SqlDatabaseInstanceSettingsIpConfigurationPscConfigList",
    "SqlDatabaseInstanceSettingsIpConfigurationPscConfigOutputReference",
    "SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections",
    "SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsList",
    "SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnectionsOutputReference",
    "SqlDatabaseInstanceSettingsLocationPreference",
    "SqlDatabaseInstanceSettingsLocationPreferenceOutputReference",
    "SqlDatabaseInstanceSettingsMaintenanceWindow",
    "SqlDatabaseInstanceSettingsMaintenanceWindowOutputReference",
    "SqlDatabaseInstanceSettingsOutputReference",
    "SqlDatabaseInstanceSettingsPasswordValidationPolicy",
    "SqlDatabaseInstanceSettingsPasswordValidationPolicyOutputReference",
    "SqlDatabaseInstanceSettingsSqlServerAuditConfig",
    "SqlDatabaseInstanceSettingsSqlServerAuditConfigOutputReference",
    "SqlDatabaseInstanceTimeouts",
    "SqlDatabaseInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a3bf1ac712a1c7cbe138519a7ed9482e4989d1c744d6981dec2442a5b0d9a4d5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database_version: builtins.str,
    clone: typing.Optional[typing.Union[SqlDatabaseInstanceClone, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    maintenance_version: typing.Optional[builtins.str] = None,
    master_instance_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    replica_configuration: typing.Optional[typing.Union[SqlDatabaseInstanceReplicaConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    replica_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_cluster: typing.Optional[typing.Union[SqlDatabaseInstanceReplicationCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_backup_context: typing.Optional[typing.Union[SqlDatabaseInstanceRestoreBackupContext, typing.Dict[builtins.str, typing.Any]]] = None,
    root_password: typing.Optional[builtins.str] = None,
    settings: typing.Optional[typing.Union[SqlDatabaseInstanceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[SqlDatabaseInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__25cd631e6e3821e1d1fe25b9eb858cc732b0aedafb1203d3849e4c6b6ec1fb1a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36f71fbd551e901be0957e4d86495bb924d17b6f7987d4b324d40215a8a7974(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285f8d9fd7abab2bcc721bc79996adf57025295eb7f0ff500380204f24763219(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c765d5eab238f5d57251eba14ed7d6f901180a8128d1109d56ab6e59f0ccd5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33319c414a9a36652e491e7b7c4315c27d7871c9e8a0379e089bbfc221a4b9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42616e4620c3d602069086cf029213456f80be5b1c3dac166524a439428e0d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4929e72c0605fd7c4ab0f378d3dd7ffd500b708c1e3d7faa0dc207f85c00c0c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddbf47ae16b53d58cc05abc5a18fc0431816cc90900268433cad49751117e577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fde7d5463af04abd53029aae824ff22c70340b3c04dd27db0c96c69cdc7d57e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3088e264c302a9074cc2feaf8ae9a19fd23508f23b2bdf9499fc03faeb229f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a944d29df4177231936dbe3509dc3fad556aa82d6a9d885d1d89b600ec9c62c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047552c008360797d8d223cc6599efe2a70e7d35130a6cc252cfdce168c98dc7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb79c6f86ac1a4c1789f3fc433e1de8c97410d31f35044e459f331bb54b39867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44a200e038d655ed373067ea7967371892ef11ef977afc99a1e867e92794105(
    *,
    source_instance_name: builtins.str,
    allocated_ip_range: typing.Optional[builtins.str] = None,
    database_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    point_in_time: typing.Optional[builtins.str] = None,
    preferred_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6021d18ad7fcdb130a45c562398c5c383ca7d6a2bd14ef49d2c786221ad7d206(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5ade42b83672fc3b813ca286c220e8dc18548a9dbd79448dac49ba60ed0a72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a713cb115600379a6a2f5d76b8a3cb493a804b16e23df6718591903eee76711(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ded8d7fe2bbcd66a8b0103737e74268fbbd73d46eead68b5777bc0578e79f33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c331b561177059dac99c078ca94c53ebaeced8d77cff8b6b90ba985df753da3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9edc2ec219472705981086b030c2451d94a077841e6f56fd7f30963dc54989(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0265b88e7f802de6d330b85c2c64634dc8971c2655ca1cd71ef4ac2b74c5cb(
    value: typing.Optional[SqlDatabaseInstanceClone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a7f54ffbe15d288113dab684fed8c4d7fcdca6badf25301c7d20f34a6b21d1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database_version: builtins.str,
    clone: typing.Optional[typing.Union[SqlDatabaseInstanceClone, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    maintenance_version: typing.Optional[builtins.str] = None,
    master_instance_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    replica_configuration: typing.Optional[typing.Union[SqlDatabaseInstanceReplicaConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    replica_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    replication_cluster: typing.Optional[typing.Union[SqlDatabaseInstanceReplicationCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_backup_context: typing.Optional[typing.Union[SqlDatabaseInstanceRestoreBackupContext, typing.Dict[builtins.str, typing.Any]]] = None,
    root_password: typing.Optional[builtins.str] = None,
    settings: typing.Optional[typing.Union[SqlDatabaseInstanceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[SqlDatabaseInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139daea944be9c4bd0953561e8d0bae628262b8bdaa79d34cc166e0f0b8c46a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e0f6b5399fc73fd1ec61917a78b370e82054b671d729bc430676f85fceb74a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d5c9677c75191ff048b758b1f1efc8ec1a0931bdaf7ae27a7fee9c429a69a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05831baa7c4022dcfed135fc3cad020d46514179eda6e79cf2282b96799d3b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__789338d26c566a516da2dd927195a690ed9bd0177218f6b7c0c5ad4ffc38e7a9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__563e7470b3e27b667cf62054c998d19c1c384dc622cfec41833a59e84680b09e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcef201253e5e5380e0defb2a51c869703df2f21f0148a10911a554c14c87873(
    value: typing.Optional[SqlDatabaseInstanceDnsNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1023ee743cafbf21dd66c5aebad96895bd45c4b639c13b04ca118c1ea2efce4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea0fa515376fded868c948c002d3cd1fb8a1be10622460d401560c83216c09b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2c79bcf494349ef4c59c1909482f231d1a71e76f2cd2a138b980f73446a3ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ff8e558141ace1ea449a98c8b66d09db214bcbc7eecf51720e7c7b66530143(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740fb8eff542db7fdafcc4bc380ecee8d11e8a58a759e8c56b233efa404e2cf2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c7a0a11bcce91c9858b1804075bb63933e755a8ec2d49e33c8cd92ed2aec9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b0d5cda62514ba7919d4871f40ef861f4feb1f2ea6245882b0a59d55f390d1(
    value: typing.Optional[SqlDatabaseInstanceIpAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9f32b8b2aa7273badba55c69653945bb6911bb6dbef4ad8ff1ad655d7f09ce(
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

def _typecheckingstub__4bf3fd84dbffa0d9761bd83aef829bf3676fc6f424e71c63055548166443094b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac3e26d4a6cd7d888a2ee0d19aa8e7b7380b49b0d20a24066937f373d95cafd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe670db9ee2a9a3554fb0caed9e24131bd7c96a547a54c405c67df19de0f08c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b95eada0b1c207d5d469dfd5fabaa357ee54b39511a66ea641862026b7342ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118ff0a40786616920ecfd7e4c8ae533e261f1231629de269681c9b43764896d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9800b6a5a2d00996c3a530bd3c67f9c4cd437a71929f9e2e93d79ab1f9af80df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c8d7b5ff21963f0e2ac6828b2a43acb1be7dc1e13a56533104879247c7be89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a09be74b23a6e87264f7ec63a7000e6b9b3c163d04610bcf23a73ee744b2357(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39047aa77174f2f3837d7a0d39ecee73426702b0a76e4189b0a1534df364bbc7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b075827e9e337c847cd32b6a61642f1fa86cb64f2c85b7551f649b21f4e0a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe9713066d7fd1d40a96a4f0a100b218b9b3141f54e77041c00b5abbbe5f907(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165e47ab654a2624e3d7616a19b1fa3d5d032de778a410c4082c27337a53d457(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a619c60055754804cac9f0c2ccaf8532c0db7585733c8ff94c2326cca68df9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5390c7390f54393b80a11aac218d669ae3ef15c90877549e6d88830c8776f0(
    value: typing.Optional[SqlDatabaseInstanceReplicaConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ba3d908375e150a6c085951e95f3889524a6740eb50bd38182d55eeee9c986(
    *,
    failover_dr_replica_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44a74a8c8600ba23ed7c7428e964c1d8c772975271feec8d146d0e590d6a768(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7376d5808c67a679b7afe95e429028ab1b56a541e2608ded12e505f3341f5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31684ca3158c7f26c975cc9cc57f796411fc4fa028c3dfb0be9bef1cc5a59f42(
    value: typing.Optional[SqlDatabaseInstanceReplicationCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56be5af80cce82d2f7eb5040cab2b6898efbf0dd13061f2d63e05418e1ea4096(
    *,
    backup_run_id: jsii.Number,
    instance_id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f681d2fedfb9a251b29158955bbb112b299e0bfc1db80e990ef67620823b4dc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f872fc6c2c6d08e99ba9e85f64c118cd04c322368da8aa19878d8dcb0ea0631(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8832026024fce3e39b585588c7542e3fcc92b5925d58ae1cbebe81cece8af89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4133605125c858e77d61dbfcf9c4d079a7515f89c00d55e69f0ec92c4a6707ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f75815964f60b7081ed4a62bcdd31c35c42c3d42a9ad3c9009c1f6d93bbb0e(
    value: typing.Optional[SqlDatabaseInstanceRestoreBackupContext],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18580c5b4579137582bdcee8411a78861c880b4029567c026353767198ae9073(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c7d64cdd9f8dd4f4245aee088e3a14506fe3b1e062be2a972bcb9e43b6a9d7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7542de20feb2b9b2f4034c36e8ef63ae3cd46cd3137921fdd6190c46f8895381(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c60bf2cccdca97c0fa8fefa6819a7b3abfadff95b769132ac6a10d4804721d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c9fd62e9193ff5dc0be524b8a17aab9309e060bfd3ceffc3bee719bc1acf47(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69aa2a0c140c0f4513fbdbcbe2a900a6d96112bac44d2453b6b7d54ac7957088(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c1c858c8f1c2b4cb2901bd82f43b35c8c2fbc1802e7de951edf77ee899a427(
    value: typing.Optional[SqlDatabaseInstanceServerCaCert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f4a325cfd642cd85ee31b029d619b2195a80301fae255d6fce8bf37b72c912(
    *,
    tier: builtins.str,
    activation_policy: typing.Optional[builtins.str] = None,
    active_directory_config: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsActiveDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    advanced_machine_features: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    availability_type: typing.Optional[builtins.str] = None,
    backup_configuration: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsBackupConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    collation: typing.Optional[builtins.str] = None,
    connection_pool_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsConnectionPoolConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connector_enforcement: typing.Optional[builtins.str] = None,
    database_flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsDatabaseFlags, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_cache_config: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsDataCacheConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deny_maintenance_period: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsDenyMaintenancePeriod, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_autoresize: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_autoresize_limit: typing.Optional[jsii.Number] = None,
    disk_size: typing.Optional[jsii.Number] = None,
    disk_type: typing.Optional[builtins.str] = None,
    edition: typing.Optional[builtins.str] = None,
    enable_dataplex_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_google_ml_integration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    insights_config: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsInsightsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_configuration: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsIpConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    location_preference: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsLocationPreference, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_window: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    password_validation_policy: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsPasswordValidationPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    retain_backups_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sql_server_audit_config: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsSqlServerAuditConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    user_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2dc813db5334b41b6f793c113709c729ad3c0f9b91a14c28239a46c2455f7ff(
    *,
    domain: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c76f973fc6e7787abbccfb4753807c54eed8918c6b151cb30be50fabfdd396(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df8b3f0061f030a5f92d02b65476c6678b4d26ba0ee8e61b49af2f64721b6f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc912ceeb0b5331a0d24f367a4fafe16eb8579ef5a7afa24a46d598117d15da2(
    value: typing.Optional[SqlDatabaseInstanceSettingsActiveDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1cb33ed07dc41f1293082b18005f289220df93d700183d9b9442e714b48406(
    *,
    threads_per_core: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbff4b96835285c47646ad92bcdff28f8a8ea654662bbe4ffec9052a419e51fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4143403da535bb8a3af08073941d82856507f50d0beb91ab7f01713c0f204c24(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8066c411e11960fb03fe50099e3be4351d6ed5d4037201ceff4ce32c235142d(
    value: typing.Optional[SqlDatabaseInstanceSettingsAdvancedMachineFeatures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a68c70563937bcaeecea90fceec3d88c8d6aedfb82036fa7ae68ff3c206f2d(
    *,
    backup_retention_settings: typing.Optional[typing.Union[SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    binary_log_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    location: typing.Optional[builtins.str] = None,
    point_in_time_recovery_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    start_time: typing.Optional[builtins.str] = None,
    transaction_log_retention_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c437328f320ab782a48f15f5c7f058b0b5e94f7a13331d236f2efa853ff1f4a(
    *,
    retained_backups: jsii.Number,
    retention_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8605fa88b11df1e8d8025529e9e249bc8353d0ea93bcfa1b76ac1b7c797678(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26c240f04f01584843ff0f4dafc2c957b3848481c31b348c20327f30b66ce77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37ac8880a6055b9875d613764ffe52b19e94c3c5cda7b948715e2d233da138b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad84ee522cb598cb2afacf5438787f80039bbc2319c990b7b3648a50e9b2462(
    value: typing.Optional[SqlDatabaseInstanceSettingsBackupConfigurationBackupRetentionSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d452df95d3721dd4e482571c362ff3014359a001e4743c8ace46d512adb376b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc56a3ca1297119065f8798a3a37b9fadeb7128632cfdd67d8af2257481d890(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75aa661c1d66c6309e0bb0d962c04204544fe53d6bd11aca0e43827335432ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1e894c96cae6c79d52f35ff034e03f00210f0d10824adf8c6d595777915c56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5742b22d423e9abcdb4af41838778b0b26a2e720431c0c9fce647f935cefb8ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857c6c465f6022f0b59973874c3a2e1e1b823d2269db69ba70a4b55c372b9130(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7817a974f7b40887e5a7779dc141924ead1d8a67c9ee219e45e598fb48938cad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b62db911313134a30e41fa3a4d8d387e43f8b2eea288e1ed273feeca8d34515(
    value: typing.Optional[SqlDatabaseInstanceSettingsBackupConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92237790b2079b4c1025c3a1bf1b82b6a4309bf3165c030fb4b895e13bf086b5(
    *,
    connection_pooling_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    flags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsConnectionPoolConfigFlags, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbe2217aba68e8d41594134e546a69e4fb9ca5aba3cde8778a8f934f70d2518(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f9eff8fa98a1216254a94732838088a2471fc936ade4ffb8a559db5bd83804(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b543bfdd4e682829d80321adf83bde67564175a834c13c62a9c26495dc61fc98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17300f4d54c8c1d434061cb9bf14ec261c5ada7787109f5d5b9b2bf99438470(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd1a002d8b82e2bc9d2d38c6823b5f9cddf3f5d5f154ce3dc5a0e533bc75073(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f487550e92495184fe736bfe1d289ffd9287d2a8dcd939e79ff0b53c17b520(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4c7120a48d76cf3c47fee322ca3325883155b38b4d7397ddd906df21f202f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfigFlags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c07f4cd5eaf0000eb46edc77445abfe20a5aae3cff27d19f0ebe8071f73b845(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729cc7241e16ca6704478789b3a573142ecd97efb4a7c000ee47786b33fbcc5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd8f4b118ae7771c0b78cae5c351b06a129ad95513b4e4fd46338428d2b8150(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f684657c9a2c503ffe74e7c02fcb54a9d8cee54e26bc26bb60ba3ac5ca15e2c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsConnectionPoolConfigFlags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774fe5e14a4365b2907fc2db93a03563f8ffb7523cb9485a58d3e3e82fb15855(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199d67dcf36d7363317ba050d57d4c1311223dd5414117bb88940453021474de(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c67ecd994efd1993b393062fc9203769dec498ecd5284fa4c601077ec143809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c639f437cca581e144a5d60eaf7df238d76954fabeb314d57e762ab3594c397(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d111bd9e568e3fdecfaa8d1f2de65d74a838a0f74b549bfd7a94460ccb2c256f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c08e7177cf27e13f61385122afb1d19a76d5348f89d1d4cffd9c015eddc1e3e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsConnectionPoolConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b47747243ea45075b08a4479329d7b4a5526110dcfe71eb3219c2ca70b28cd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c62f78a847ea4b01f81bcd2f09985782dd92d2261f294c35e82d289a318551d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsConnectionPoolConfigFlags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc3d0aa8568f8944445ea67b2d6ec20f00ba8d03dc7651918a1ed52070408cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee8bbaca696634d271c630f4c6f50ddf29cebd1f5519337c934d568fa03a2bf5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsConnectionPoolConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0816fa3f3d36f57770772ea30ac2ed3633bb5a0f88f241b5416ebedfdd227e97(
    *,
    data_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe458e4b960fe5db0bcaafc47b8987fa02cc48364bef7b582fcc98be9207f1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab74f77d53198a9011c28f99006cabee50a01ef7745a62d7b6f7cd0783c18c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bde755d0d2f298f1d9f22fcf097ecb17511d558eae40d5cfc19d8acb486a8e8(
    value: typing.Optional[SqlDatabaseInstanceSettingsDataCacheConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f33c9eab581d94610142bfe4047349dac9f80575bfdddd55cf645988b08e516(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dcebd845cf94013faa6d087a9dccd309fbfba46e19e11ba7185b44be35cdc91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7d49fd23b8df415535ad4d63b1f640d6acae4122ae6a14a5b153cbac5c48ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aedfecb63055d272a86bc65b98b544266bbdc608c954a467cf9bc9242158d08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15f011a0a3cce7ab8b049b7c7ca663009e103f7f6f5eca6c5515f5d34eef0f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b714259f437fa1bcbb21bb67b912b4ef052ac7d908401fc440f670acec4062a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff00e2c01ee0bd8855d56a92be371b5c96310595b198120508e200822d9bf27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsDatabaseFlags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cdaeae6e8d8dfe23b030078caacebcd5151a0ee15584553e67e5a53d98081a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea0fd2c05bf54fab568a56326afff8be822466c21a0e062ab5ad6f109a37019(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b57162a29fd61208d42db9a2b942caf5dca9f9961cac7a563d2c7d2ed592f7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e43f803320a1012d0ff76e7420bb3f31b38a06a3c41d6901fef12a7adf257a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsDatabaseFlags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090897c16ada1f62e0493a1c3d0bc0f376fdd8d67225b3396394383fc32b4aeb(
    *,
    end_date: builtins.str,
    start_date: builtins.str,
    time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7fbfc0778662654c75e2f34a8c00fd90c20fef4d09bdcf095da72d1586bf58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b33658b971e41d6baf948f73bfa25c2537e41733b6b47bae4ad7ca05fe030c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4985d83cf42b1f7d219e2e99b3bf2378c9c15b73dc89012f74e6ebf1507ad38a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1412b24f0d29832874407ab40c0537e332de0e2613026f5d7b244b8f8ff2d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c173d75e64a84ccadca8b3a1370ff5b754c3d86d0f5d8a0643b4e6ec5beb969(
    value: typing.Optional[SqlDatabaseInstanceSettingsDenyMaintenancePeriod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bed2f49e117189d5f9c56d315b1d15369aac31e55f2d8b2c094185c9493394f(
    *,
    query_insights_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_plans_per_minute: typing.Optional[jsii.Number] = None,
    query_string_length: typing.Optional[jsii.Number] = None,
    record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a92fd2104396af417f6aa8da508d13fa99b7f98ff80cfc69793d8f2ca848f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6edf07748c884614ebcb7abe3e58e962ae469443b0d8d4c0190d854f787cda8f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63464752be3851e035d8068793a2897c437243f14dbad748d74c995d6db07793(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42a62494601d4e646045f5d968774cd6b6f0006eb9fbb5c847826b248095af7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83fe561fe8c41a07462bc3ca95bd15e82971c3c343fd80c224d965eb89a9e28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19da9d1fff9c42ff6b1b013a5b9097d96a951df97a254d6dba7b9e332fdd943e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65326ce7f968667837cdcfcc40ffe54fc0ee7ee119c498001ff0632278d1ae36(
    value: typing.Optional[SqlDatabaseInstanceSettingsInsightsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe34d3ed763b412872746717e6789569095e9c8758a60c27990296d63b49bf6f(
    *,
    allocated_ip_range: typing.Optional[builtins.str] = None,
    authorized_networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_private_path_for_google_cloud_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ipv4_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_network: typing.Optional[builtins.str] = None,
    psc_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsIpConfigurationPscConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    server_ca_mode: typing.Optional[builtins.str] = None,
    server_ca_pool: typing.Optional[builtins.str] = None,
    ssl_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493097ffcbbc668070facbf3224a2c25ade663ab6ce0c24163f4d3aa948a44a2(
    *,
    value: builtins.str,
    expiration_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11688f84c0789065fe69658c84b88c538b470ebe38a896bdfb54b69b3ed1225a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a85e22e5188ec5e5abf00f763f2ac6b204d7067533c64a2f35aca539694c3e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54050e08a4c7c8ddad411cb8996cbcfa853c5567c23e2a7dfec2dc94e929b78f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3bd6693b17730aab6e63b6f1660140328efefbc9ea8ae4e9add82e1cc4c10d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf59539263b578951e89cabd8a61f5711bb792f8264c88f19348af6eec48e2d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfab77f0ad2655e6c0073325aaf4e09e64303ce86e0ce995bede7fa0bf36340(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1db14f8ce41e47399e1a02ce0e67051842e80e054455f0874de289377c3ec49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bc40e06db86128a81e36206e2c1872c128d3c8a1255788c2017c549a85b9e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8b6e9c78977f7c567ebee093a7b39715bb15a3457b48c032eeeb91cdf2441c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348e999cbf6a8e9946a42e12aad35f01fc91905fc71eef481c1daaee1801f141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f202e17eb7dd0d85fc161967a44e019a844ab38b4cdbb7f701dba7ea4f80d3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6be414a9a15e1a9b78798ad407f2b94855f7d476bf0a70eeb303b7cc0cc1e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9415cea5f3684e51964b92def458fe0ddafd3bb54eabf17be567fbbb0c6bfd05(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsIpConfigurationAuthorizedNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf6104b77d9fed4c07a1faa63b5eeffe7c1ef3329ad0f9d19cc050de5b4b241(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsIpConfigurationPscConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9694848d5fb46ee76c4b0f449b1d6765f79586a7ab75f168a105ce3b4780f5a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef633be7a24d758b0dc4ed2bfd5344e0b3ae26817ce22d1898ff09a304099be(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b7118c7aa16ecc004bbbf35af4c6f7db810327bbe31320c00304f20620b240(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bd47e84cd47075552dde33568b0a622937b6a742b775d099014e17582504c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc8844662bbc2cb36509532e24571a5716c7074d441b99fb94ed24137f1dfe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc22a55a43fa503acd0851c52a126b14c76422744d30933ff3364a7b0b4e0e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5020f1c188eca2d8c037e8848df906774d19e4b066dd4293e685158f0b72d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057cbe656b7c7c0898ccba23363b9514587101637858102b2d9ec5fec3f3191c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b5f7534567d021a92add2ab6673c105bb9f9912f34069d9e6a4e084c26ca45(
    value: typing.Optional[SqlDatabaseInstanceSettingsIpConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2640256bd9b56b6daf23679d6b26401fd77136c1208e9a5fb6ea236cb55e9599(
    *,
    allowed_consumer_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]]] = None,
    psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9f027ee52dacdc064d1b9165b85d0009945d963b70554749ccd2ebdeea1902(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc73937696db064a43dece13b79917e08e593621bae9042ca78f4e09e5e7c77f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ecf85a6aa2efe13ced5ba46870bd4ba99a82d23b369c793009b54c0e8d2e7c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ac68ac9957eb20c69183980dba360194bae1aef5e9acf8dfba2155acfe2c94(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83463cb22b62d1f3f906ed49d749a8ec9bcadd3805fee3695abce85cef8e98e2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07b1f8b63b1853490119ee2f04179fb034c6dab232316bca99174b2a26fb139(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationPscConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416c9d1c9222c79e0ba4b36e5360227af3c1c5030df124db4af0cf6e4510c990(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83902193d635e0d0b95502a9f77cc7ad1f64a39d79002344183329874b8bf7e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c60b75d1c37477eef4ffe18930a3ce30b68bc0d230f3fe1f1a542b9bcde4dfc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38f05a305c6f375b83f0f6ac26994f938537d9fcace8b40290b4854bc2e0e99(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487d16571b97454564d96c1a652b4b0e518d8ed02702eb83c37d02929d382ee5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationPscConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78dd6a3278c35476a3466c406b9ca8140188e51ec399a9135c90120bd08e8816(
    *,
    consumer_network: builtins.str,
    consumer_service_project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb45318cf40bf74a9fba6a07411a00179088a4f9ab1f3bca512b5bb3e3af3d8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3c08fdfc29e67177ecf9c1c52fe0fcad61ddd58b1a3b5ac974f60b503243d7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375e21d4639f31d4bd08b81e12090f151d70b667819ab69ca1a10256cc68d580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2928634737577c9409ffc1051e1567947a27cb58913d57629adde1e81a5ddf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b3c056b14e042ea22325cc5805305e7c0b55805daa802351dd043f5b962984(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22118b152decaff1cea8219e393210c21b451ca0bc7715e5beb0c773929a402e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4c846d81203277970dbc7b7b05bec6c916ce6ac217b2d52208194d137e955d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79adea3b1a99384d7b0ea635e2eb2486a7c9aac17344b45fdb1dd06528031fcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a2c6317eb336983061d72e2b0e127cb81e02754ac5f4ab9ae4507e88abf94b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8c2491db7237939b14522745443974253a8b93c20a4ed6e648a35202a79392(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceSettingsIpConfigurationPscConfigPscAutoConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f86be3317e2511982cd4c025d816333e595012721bc8f24f35490d49f9dab4(
    *,
    follow_gae_application: typing.Optional[builtins.str] = None,
    secondary_zone: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3047bc8bda93621168d0ea91bf765f628d83e51befe654edc848868bd0cee046(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d1368771c1692a133754068fdadb8aee3adf6d74b448c9e0755940aeacd77f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75adfde3c1856214e3a26c706baf3a4edac310fc05bbb7c288d8fbd8b4f4dffe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4548300c6031cba53a952acd3097622beb1cbbab271b1565f66c7a1606d3bf0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd8f9dbcaeecb3cc05da4a23ff5316ff3a00494f305d5a712cadf9f0320d92e(
    value: typing.Optional[SqlDatabaseInstanceSettingsLocationPreference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d35185ac41cef3cc2bfa393b2082488a90e3829b756b23b10389d840d041b14(
    *,
    day: typing.Optional[jsii.Number] = None,
    hour: typing.Optional[jsii.Number] = None,
    update_track: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6129f4a50d9f0bdd9c7f62bd6b246872088f993bb7c4803883926933ce6708(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245fae86da872ab833e25a951b05f8f263d8f6ad6be6ea23b3d2dd8ff8909af6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98914c0d8dc5590f99b33b950c0d03500b54f8aa4f6d537553c00aaff06b761(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fe0b5e848be09826263d64bb6ece702c2e014a46a8c787546edd2fd7e067e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de855d1c6ea62869c6951a0b524f9450fde85a73bf5c1ee0d347e8ee92eb3ade(
    value: typing.Optional[SqlDatabaseInstanceSettingsMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875452f68abfc43b37a368a5a2f7405f63d1435bc384c1e0a1d707af08fc2c7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a121a3d3b8836b174182407742c882a4d91f7718ed24d45f6f6bd5c1557c85b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsConnectionPoolConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bc64a87ae189957c1ddcca38fd0bd3f088f0046f459d1d5683e15da73b7910(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlDatabaseInstanceSettingsDatabaseFlags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e772d1d6370147013505656601369ef9374c72c9ab24d15f5492e4ba36beaf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9254da10a68c5e19adf3afabb78a305ae25205ed56aa18b3026c8ad5bd110bad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be6c5084df2a00497ab7417cf890bf8e81044b1792fc028cb4519bcb3df82d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40767dcbdc6a299604592a341f0f2c160c0acf6841689e9b5730d022c27beeef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb02edb36ebb5fc05256af7427f6e7ebe3dda37696e092a73304e5b2b6adc1b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a3965a87b0349a527a8f6e9934e940f06fc30f157827355871de0b128addd9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b007f113398962e29f78ca9d34e52f95870a2846180feb6758f7218e3a28b651(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2007981e8125814b6507ab8b2e3e213230524c365774d819681345fb391fded5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17d33a4f683397c1af23955fb3dc4ffbbb2ac8c31195053079dc81ab1b78fec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d8c14856c022f11fee7425537252e109a8c48ebb816094f96fd9c5c89d82a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea496dacc89a66bc231753205e32a06e2bd792e4463be0c777b2c2eee048cd86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77dfcd24945f62226ff0346242bc0afabc771bdfacfe6ed3350972e0089bf97a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa79e08decf7592a1470d2a894f1d680d58bfa22f40e15d6b5e92a8c07282aba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cd073b046e77657d7b0924a56800a96afa268fd20e1c485e898a885cdf3c98(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b5893ffefe72c3731ea82fef2f1464288d1b44b617bfeb25221c0a560f5da2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d230f9eee67efc382159d7cee6b5896a5930c99b4f8f463066f1c0dbcf148e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be38c31184ff9ef10361b9e0d92a020e0a2224a9406fa589d754413a701c2fd5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7d3cc1ef0d35d7cba8b05d83dc3104f99d3d02a7fc9e90551bcae3e5fc8862(
    value: typing.Optional[SqlDatabaseInstanceSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28436dec1d60e5f9f162e49cc6b33a6185162fa967411e897985df6c246ff42f(
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

def _typecheckingstub__60e936be047fd46816da3fbf265a8248e20719a098890ad983d10a4ead38d832(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad39ec2588953874a3c9cc3165b1cb0fd9120539f75578e81b68179d90f1061b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb66254177e4a10a58c87bdb8f907bce692131f13d5d503bcd6ead726d145615(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699637a351236547ff4560ef86788be1409adcc7b4e47f3eac5797aebcf435a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd1f54bf9dde4c1617f644f3185793aeaa64f0a129c5857518bc504b924ab0d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0307a18889a93bb897466793069056321fd4613a72939caf107cd8bb4348394(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3646c23f752449980ea4087b662a1ec375f06961caafdc099b2865713b6c04c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0b2a3a80de085f382957f58bf500b2cc3d893ea5dbed8f7218134772cecb70(
    value: typing.Optional[SqlDatabaseInstanceSettingsPasswordValidationPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f686c7c43a1fb76874801d8098be57364ca5bb30e5949d71798b54882810543f(
    *,
    bucket: typing.Optional[builtins.str] = None,
    retention_interval: typing.Optional[builtins.str] = None,
    upload_interval: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d71a8d0bcebc884ec098fc18a6921006ed4b0d041ad660a39a87f91b5363e99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ffb7afe95d7cc7b66b9365a24a8d33f68af17d5ec1772200d7bbfdefa40fcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091f4c32885beda4e0a3125c0fed1b4e24c415807517d754024732fb06d42257(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da68f9ae4b3e7bd09d6d107d7b33642570d795c4f0930c3f666af03d3bb9bea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd593ffff4a9c7cd205381d15d57bf80097904bff80ef9983c5517b374f82885(
    value: typing.Optional[SqlDatabaseInstanceSettingsSqlServerAuditConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24a64a305fcb158dc6d64df2c3fe6537f65d81e49b17b621e8712c723b86b12(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61cec9df86c3e9d2505ad08c310220923702d54d122b858ed0ce4efa3e6fe380(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4084c800d24f844098125b97939622092f799c245583a85b30a0ae4f3e1b33ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738460a243fcd707e237992dd199e854b9cd586342f1e4d89e8b3f27d99a1b91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f226ad1d8a02dbd1e0dfe84a4018d932c92bbf34242431e9d5de0d37344333b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb1997a2b28421989d2083f3387841745e95628b5c16fc56568ff3064302f85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SqlDatabaseInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
