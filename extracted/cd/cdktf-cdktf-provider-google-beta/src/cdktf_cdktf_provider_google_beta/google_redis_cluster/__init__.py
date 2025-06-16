r'''
# `google_redis_cluster`

Refer to the Terraform Registry for docs: [`google_redis_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster).
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


class GoogleRedisCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster google_redis_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        shard_count: jsii.Number,
        authorization_mode: typing.Optional[builtins.str] = None,
        automated_backup_config: typing.Optional[typing.Union["GoogleRedisClusterAutomatedBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cross_cluster_replication_config: typing.Optional[typing.Union["GoogleRedisClusterCrossClusterReplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs_source: typing.Optional[typing.Union["GoogleRedisClusterGcsSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        maintenance_policy: typing.Optional[typing.Union["GoogleRedisClusterMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_backup_source: typing.Optional[typing.Union["GoogleRedisClusterManagedBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["GoogleRedisClusterPersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleRedisClusterPscConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleRedisClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        zone_distribution_config: typing.Optional[typing.Union["GoogleRedisClusterZoneDistributionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster google_redis_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param shard_count: Required. Number of shards for the Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#shard_count GoogleRedisCluster#shard_count}
        :param authorization_mode: Optional. The authorization mode of the Redis cluster. If not provided, auth feature is disabled for the cluster. Default value: "AUTH_MODE_DISABLED" Possible values: ["AUTH_MODE_UNSPECIFIED", "AUTH_MODE_IAM_AUTH", "AUTH_MODE_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#authorization_mode GoogleRedisCluster#authorization_mode}
        :param automated_backup_config: automated_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#automated_backup_config GoogleRedisCluster#automated_backup_config}
        :param cross_cluster_replication_config: cross_cluster_replication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#cross_cluster_replication_config GoogleRedisCluster#cross_cluster_replication_config}
        :param deletion_protection_enabled: Optional. Indicates if the cluster is deletion protected or not. If the value if set to true, any delete cluster operation will fail. Default value is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#deletion_protection_enabled GoogleRedisCluster#deletion_protection_enabled}
        :param gcs_source: gcs_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#gcs_source GoogleRedisCluster#gcs_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#id GoogleRedisCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key: The KMS key used to encrypt the at-rest data of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#kms_key GoogleRedisCluster#kms_key}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#maintenance_policy GoogleRedisCluster#maintenance_policy}
        :param managed_backup_source: managed_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#managed_backup_source GoogleRedisCluster#managed_backup_source}
        :param name: Unique name of the resource in this scope including project and location using the form: projects/{projectId}/locations/{locationId}/clusters/{clusterId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#name GoogleRedisCluster#name}
        :param node_type: The nodeType for the Redis cluster. If not provided, REDIS_HIGHMEM_MEDIUM will be used as default Possible values: ["REDIS_SHARED_CORE_NANO", "REDIS_HIGHMEM_MEDIUM", "REDIS_HIGHMEM_XLARGE", "REDIS_STANDARD_SMALL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#node_type GoogleRedisCluster#node_type}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#persistence_config GoogleRedisCluster#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#project GoogleRedisCluster#project}.
        :param psc_configs: psc_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#psc_configs GoogleRedisCluster#psc_configs}
        :param redis_configs: Configure Redis Cluster behavior using a subset of native Redis configuration parameters. Please check Memorystore documentation for the list of supported parameters: https://cloud.google.com/memorystore/docs/cluster/supported-instance-configurations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#redis_configs GoogleRedisCluster#redis_configs}
        :param region: The name of the region of the Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#region GoogleRedisCluster#region}
        :param replica_count: Optional. The number of replica nodes per shard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#replica_count GoogleRedisCluster#replica_count}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#timeouts GoogleRedisCluster#timeouts}
        :param transit_encryption_mode: Optional. The in-transit encryption for the Redis cluster. If not provided, encryption is disabled for the cluster. Default value: "TRANSIT_ENCRYPTION_MODE_DISABLED" Possible values: ["TRANSIT_ENCRYPTION_MODE_UNSPECIFIED", "TRANSIT_ENCRYPTION_MODE_DISABLED", "TRANSIT_ENCRYPTION_MODE_SERVER_AUTHENTICATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#transit_encryption_mode GoogleRedisCluster#transit_encryption_mode}
        :param zone_distribution_config: zone_distribution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#zone_distribution_config GoogleRedisCluster#zone_distribution_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d06e83408d389d126307dc5da5dbea0b25bbdb25268e1b893b952189257b550)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleRedisClusterConfig(
            shard_count=shard_count,
            authorization_mode=authorization_mode,
            automated_backup_config=automated_backup_config,
            cross_cluster_replication_config=cross_cluster_replication_config,
            deletion_protection_enabled=deletion_protection_enabled,
            gcs_source=gcs_source,
            id=id,
            kms_key=kms_key,
            maintenance_policy=maintenance_policy,
            managed_backup_source=managed_backup_source,
            name=name,
            node_type=node_type,
            persistence_config=persistence_config,
            project=project,
            psc_configs=psc_configs,
            redis_configs=redis_configs,
            region=region,
            replica_count=replica_count,
            timeouts=timeouts,
            transit_encryption_mode=transit_encryption_mode,
            zone_distribution_config=zone_distribution_config,
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
        '''Generates CDKTF code for importing a GoogleRedisCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleRedisCluster to import.
        :param import_from_id: The id of the existing GoogleRedisCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleRedisCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f218ec7276baa83de99063a03dad61a503544e9d7cb8d4555432fe63a98f2c8f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutomatedBackupConfig")
    def put_automated_backup_config(
        self,
        *,
        fixed_frequency_schedule: typing.Union["GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule", typing.Dict[builtins.str, typing.Any]],
        retention: builtins.str,
    ) -> None:
        '''
        :param fixed_frequency_schedule: fixed_frequency_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#fixed_frequency_schedule GoogleRedisCluster#fixed_frequency_schedule}
        :param retention: How long to keep automated backups before the backups are deleted. The value should be between 1 day and 365 days. If not specified, the default value is 35 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#retention GoogleRedisCluster#retention}
        '''
        value = GoogleRedisClusterAutomatedBackupConfig(
            fixed_frequency_schedule=fixed_frequency_schedule, retention=retention
        )

        return typing.cast(None, jsii.invoke(self, "putAutomatedBackupConfig", [value]))

    @jsii.member(jsii_name="putCrossClusterReplicationConfig")
    def put_cross_cluster_replication_config(
        self,
        *,
        cluster_role: typing.Optional[builtins.str] = None,
        primary_cluster: typing.Optional[typing.Union["GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cluster_role: The role of the cluster in cross cluster replication. Supported values are:. 1. 'CLUSTER_ROLE_UNSPECIFIED': This is an independent cluster that has never participated in cross cluster replication. It allows both reads and writes. 1. 'NONE': This is an independent cluster that previously participated in cross cluster replication(either as a 'PRIMARY' or 'SECONDARY' cluster). It allows both reads and writes. 1. 'PRIMARY': This cluster serves as the replication source for secondary clusters that are replicating from it. Any data written to it is automatically replicated to its secondary clusters. It allows both reads and writes. 1. 'SECONDARY': This cluster replicates data from the primary cluster. It allows only reads. Possible values: ["CLUSTER_ROLE_UNSPECIFIED", "NONE", "PRIMARY", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#cluster_role GoogleRedisCluster#cluster_role}
        :param primary_cluster: primary_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#primary_cluster GoogleRedisCluster#primary_cluster}
        :param secondary_clusters: secondary_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#secondary_clusters GoogleRedisCluster#secondary_clusters}
        '''
        value = GoogleRedisClusterCrossClusterReplicationConfig(
            cluster_role=cluster_role,
            primary_cluster=primary_cluster,
            secondary_clusters=secondary_clusters,
        )

        return typing.cast(None, jsii.invoke(self, "putCrossClusterReplicationConfig", [value]))

    @jsii.member(jsii_name="putGcsSource")
    def put_gcs_source(self, *, uris: typing.Sequence[builtins.str]) -> None:
        '''
        :param uris: URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#uris GoogleRedisCluster#uris}
        '''
        value = GoogleRedisClusterGcsSource(uris=uris)

        return typing.cast(None, jsii.invoke(self, "putGcsSource", [value]))

    @jsii.member(jsii_name="putMaintenancePolicy")
    def put_maintenance_policy(
        self,
        *,
        weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#weekly_maintenance_window GoogleRedisCluster#weekly_maintenance_window}
        '''
        value = GoogleRedisClusterMaintenancePolicy(
            weekly_maintenance_window=weekly_maintenance_window
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenancePolicy", [value]))

    @jsii.member(jsii_name="putManagedBackupSource")
    def put_managed_backup_source(self, *, backup: builtins.str) -> None:
        '''
        :param backup: Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#backup GoogleRedisCluster#backup}
        '''
        value = GoogleRedisClusterManagedBackupSource(backup=backup)

        return typing.cast(None, jsii.invoke(self, "putManagedBackupSource", [value]))

    @jsii.member(jsii_name="putPersistenceConfig")
    def put_persistence_config(
        self,
        *,
        aof_config: typing.Optional[typing.Union["GoogleRedisClusterPersistenceConfigAofConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        rdb_config: typing.Optional[typing.Union["GoogleRedisClusterPersistenceConfigRdbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aof_config: aof_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#aof_config GoogleRedisCluster#aof_config}
        :param mode: Optional. Controls whether Persistence features are enabled. If not provided, the existing value will be used. - DISABLED: Persistence (both backup and restore) is disabled for the cluster. - RDB: RDB based Persistence is enabled. - AOF: AOF based Persistence is enabled. Possible values: ["PERSISTENCE_MODE_UNSPECIFIED", "DISABLED", "RDB", "AOF"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#mode GoogleRedisCluster#mode}
        :param rdb_config: rdb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#rdb_config GoogleRedisCluster#rdb_config}
        '''
        value = GoogleRedisClusterPersistenceConfig(
            aof_config=aof_config, mode=mode, rdb_config=rdb_config
        )

        return typing.cast(None, jsii.invoke(self, "putPersistenceConfig", [value]))

    @jsii.member(jsii_name="putPscConfigs")
    def put_psc_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleRedisClusterPscConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f3eb78a9105ce610c006bc97b1b10e13b728d2ea5b29d8e1ff7da49eba78e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPscConfigs", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#create GoogleRedisCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#delete GoogleRedisCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#update GoogleRedisCluster#update}.
        '''
        value = GoogleRedisClusterTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putZoneDistributionConfig")
    def put_zone_distribution_config(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Immutable. The mode for zone distribution for Memorystore Redis cluster. If not provided, MULTI_ZONE will be used as default Possible values: ["MULTI_ZONE", "SINGLE_ZONE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#mode GoogleRedisCluster#mode}
        :param zone: Immutable. The zone for single zone Memorystore Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#zone GoogleRedisCluster#zone}
        '''
        value = GoogleRedisClusterZoneDistributionConfig(mode=mode, zone=zone)

        return typing.cast(None, jsii.invoke(self, "putZoneDistributionConfig", [value]))

    @jsii.member(jsii_name="resetAuthorizationMode")
    def reset_authorization_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationMode", []))

    @jsii.member(jsii_name="resetAutomatedBackupConfig")
    def reset_automated_backup_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomatedBackupConfig", []))

    @jsii.member(jsii_name="resetCrossClusterReplicationConfig")
    def reset_cross_cluster_replication_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossClusterReplicationConfig", []))

    @jsii.member(jsii_name="resetDeletionProtectionEnabled")
    def reset_deletion_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtectionEnabled", []))

    @jsii.member(jsii_name="resetGcsSource")
    def reset_gcs_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsSource", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetMaintenancePolicy")
    def reset_maintenance_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenancePolicy", []))

    @jsii.member(jsii_name="resetManagedBackupSource")
    def reset_managed_backup_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedBackupSource", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNodeType")
    def reset_node_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeType", []))

    @jsii.member(jsii_name="resetPersistenceConfig")
    def reset_persistence_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersistenceConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPscConfigs")
    def reset_psc_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscConfigs", []))

    @jsii.member(jsii_name="resetRedisConfigs")
    def reset_redis_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisConfigs", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReplicaCount")
    def reset_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaCount", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTransitEncryptionMode")
    def reset_transit_encryption_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransitEncryptionMode", []))

    @jsii.member(jsii_name="resetZoneDistributionConfig")
    def reset_zone_distribution_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneDistributionConfig", []))

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
    @jsii.member(jsii_name="automatedBackupConfig")
    def automated_backup_config(
        self,
    ) -> "GoogleRedisClusterAutomatedBackupConfigOutputReference":
        return typing.cast("GoogleRedisClusterAutomatedBackupConfigOutputReference", jsii.get(self, "automatedBackupConfig"))

    @builtins.property
    @jsii.member(jsii_name="backupCollection")
    def backup_collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupCollection"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="crossClusterReplicationConfig")
    def cross_cluster_replication_config(
        self,
    ) -> "GoogleRedisClusterCrossClusterReplicationConfigOutputReference":
        return typing.cast("GoogleRedisClusterCrossClusterReplicationConfigOutputReference", jsii.get(self, "crossClusterReplicationConfig"))

    @builtins.property
    @jsii.member(jsii_name="discoveryEndpoints")
    def discovery_endpoints(self) -> "GoogleRedisClusterDiscoveryEndpointsList":
        return typing.cast("GoogleRedisClusterDiscoveryEndpointsList", jsii.get(self, "discoveryEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="gcsSource")
    def gcs_source(self) -> "GoogleRedisClusterGcsSourceOutputReference":
        return typing.cast("GoogleRedisClusterGcsSourceOutputReference", jsii.get(self, "gcsSource"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicy")
    def maintenance_policy(
        self,
    ) -> "GoogleRedisClusterMaintenancePolicyOutputReference":
        return typing.cast("GoogleRedisClusterMaintenancePolicyOutputReference", jsii.get(self, "maintenancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceSchedule")
    def maintenance_schedule(self) -> "GoogleRedisClusterMaintenanceScheduleList":
        return typing.cast("GoogleRedisClusterMaintenanceScheduleList", jsii.get(self, "maintenanceSchedule"))

    @builtins.property
    @jsii.member(jsii_name="managedBackupSource")
    def managed_backup_source(
        self,
    ) -> "GoogleRedisClusterManagedBackupSourceOutputReference":
        return typing.cast("GoogleRedisClusterManagedBackupSourceOutputReference", jsii.get(self, "managedBackupSource"))

    @builtins.property
    @jsii.member(jsii_name="persistenceConfig")
    def persistence_config(
        self,
    ) -> "GoogleRedisClusterPersistenceConfigOutputReference":
        return typing.cast("GoogleRedisClusterPersistenceConfigOutputReference", jsii.get(self, "persistenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="preciseSizeGb")
    def precise_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "preciseSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="pscConfigs")
    def psc_configs(self) -> "GoogleRedisClusterPscConfigsList":
        return typing.cast("GoogleRedisClusterPscConfigsList", jsii.get(self, "pscConfigs"))

    @builtins.property
    @jsii.member(jsii_name="pscConnections")
    def psc_connections(self) -> "GoogleRedisClusterPscConnectionsList":
        return typing.cast("GoogleRedisClusterPscConnectionsList", jsii.get(self, "pscConnections"))

    @builtins.property
    @jsii.member(jsii_name="pscServiceAttachments")
    def psc_service_attachments(self) -> "GoogleRedisClusterPscServiceAttachmentsList":
        return typing.cast("GoogleRedisClusterPscServiceAttachmentsList", jsii.get(self, "pscServiceAttachments"))

    @builtins.property
    @jsii.member(jsii_name="sizeGb")
    def size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGb"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateInfo")
    def state_info(self) -> "GoogleRedisClusterStateInfoList":
        return typing.cast("GoogleRedisClusterStateInfoList", jsii.get(self, "stateInfo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleRedisClusterTimeoutsOutputReference":
        return typing.cast("GoogleRedisClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="zoneDistributionConfig")
    def zone_distribution_config(
        self,
    ) -> "GoogleRedisClusterZoneDistributionConfigOutputReference":
        return typing.cast("GoogleRedisClusterZoneDistributionConfigOutputReference", jsii.get(self, "zoneDistributionConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizationModeInput")
    def authorization_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="automatedBackupConfigInput")
    def automated_backup_config_input(
        self,
    ) -> typing.Optional["GoogleRedisClusterAutomatedBackupConfig"]:
        return typing.cast(typing.Optional["GoogleRedisClusterAutomatedBackupConfig"], jsii.get(self, "automatedBackupConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="crossClusterReplicationConfigInput")
    def cross_cluster_replication_config_input(
        self,
    ) -> typing.Optional["GoogleRedisClusterCrossClusterReplicationConfig"]:
        return typing.cast(typing.Optional["GoogleRedisClusterCrossClusterReplicationConfig"], jsii.get(self, "crossClusterReplicationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionEnabledInput")
    def deletion_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsSourceInput")
    def gcs_source_input(self) -> typing.Optional["GoogleRedisClusterGcsSource"]:
        return typing.cast(typing.Optional["GoogleRedisClusterGcsSource"], jsii.get(self, "gcsSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicyInput")
    def maintenance_policy_input(
        self,
    ) -> typing.Optional["GoogleRedisClusterMaintenancePolicy"]:
        return typing.cast(typing.Optional["GoogleRedisClusterMaintenancePolicy"], jsii.get(self, "maintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="managedBackupSourceInput")
    def managed_backup_source_input(
        self,
    ) -> typing.Optional["GoogleRedisClusterManagedBackupSource"]:
        return typing.cast(typing.Optional["GoogleRedisClusterManagedBackupSource"], jsii.get(self, "managedBackupSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeInput")
    def node_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="persistenceConfigInput")
    def persistence_config_input(
        self,
    ) -> typing.Optional["GoogleRedisClusterPersistenceConfig"]:
        return typing.cast(typing.Optional["GoogleRedisClusterPersistenceConfig"], jsii.get(self, "persistenceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pscConfigsInput")
    def psc_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterPscConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterPscConfigs"]]], jsii.get(self, "pscConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="redisConfigsInput")
    def redis_configs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "redisConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaCountInput")
    def replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="shardCountInput")
    def shard_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "shardCountInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleRedisClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleRedisClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionModeInput")
    def transit_encryption_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitEncryptionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneDistributionConfigInput")
    def zone_distribution_config_input(
        self,
    ) -> typing.Optional["GoogleRedisClusterZoneDistributionConfig"]:
        return typing.cast(typing.Optional["GoogleRedisClusterZoneDistributionConfig"], jsii.get(self, "zoneDistributionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationMode")
    def authorization_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationMode"))

    @authorization_mode.setter
    def authorization_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb8457248878bc9a27f5fa539da594429af7ead11b3c0ee1f18d74522aafb2eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationMode", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__45bb2663677e2dceeb9a382cec90ebddac50b8ef9b39981accfc56b15a029096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbde1543e0c209061fbb0700c5355d558b617cab336c278d9d96c73c588cc638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eafb9b09128d05883d703d770dd92faa062dc76181d65a475133d784a4f34f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c8a785b5d2a737ba3fc953d7c71b7ed2908333c56b99824d897d0a0e7e034b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b521b3f6028d73a1ca5e884c1c0177af62c5fac9d32a93edba43e397b0f1aa05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a50115c1f952d192b490c63a5a25be31b2d8ae469fca81f48af70e2627629e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redisConfigs")
    def redis_configs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "redisConfigs"))

    @redis_configs.setter
    def redis_configs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9913e9ece04a764e8d5a0fb26eb01efe7b3adec9c586e0c701522f3d5080284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisConfigs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e89b4fefd552c9e14092f82ed324c59b965eb6355b5960aff782e0592054464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCount"))

    @replica_count.setter
    def replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4706de2b8d3bcd5826af64a03d25a590b3bc81dfdcf452bd411387d1d8d3a313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shardCount")
    def shard_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shardCount"))

    @shard_count.setter
    def shard_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e3a5d473330b6e841521a50e106f13a6c5282d65f96d7865529d5dedb9f092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shardCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionMode")
    def transit_encryption_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitEncryptionMode"))

    @transit_encryption_mode.setter
    def transit_encryption_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c8aa418230c5d3ffdba9bc58dace30d1cc5626569868aa6670af422e2cd5c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitEncryptionMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterAutomatedBackupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "fixed_frequency_schedule": "fixedFrequencySchedule",
        "retention": "retention",
    },
)
class GoogleRedisClusterAutomatedBackupConfig:
    def __init__(
        self,
        *,
        fixed_frequency_schedule: typing.Union["GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule", typing.Dict[builtins.str, typing.Any]],
        retention: builtins.str,
    ) -> None:
        '''
        :param fixed_frequency_schedule: fixed_frequency_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#fixed_frequency_schedule GoogleRedisCluster#fixed_frequency_schedule}
        :param retention: How long to keep automated backups before the backups are deleted. The value should be between 1 day and 365 days. If not specified, the default value is 35 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#retention GoogleRedisCluster#retention}
        '''
        if isinstance(fixed_frequency_schedule, dict):
            fixed_frequency_schedule = GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule(**fixed_frequency_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a048cc4bd602c6bd9c4e55d33993c7d4b9633e42831a1354cdf677350bfe6f6)
            check_type(argname="argument fixed_frequency_schedule", value=fixed_frequency_schedule, expected_type=type_hints["fixed_frequency_schedule"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fixed_frequency_schedule": fixed_frequency_schedule,
            "retention": retention,
        }

    @builtins.property
    def fixed_frequency_schedule(
        self,
    ) -> "GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule":
        '''fixed_frequency_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#fixed_frequency_schedule GoogleRedisCluster#fixed_frequency_schedule}
        '''
        result = self._values.get("fixed_frequency_schedule")
        assert result is not None, "Required property 'fixed_frequency_schedule' is missing"
        return typing.cast("GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule", result)

    @builtins.property
    def retention(self) -> builtins.str:
        '''How long to keep automated backups before the backups are deleted.

        The value should be between 1 day and 365 days. If not specified, the default value is 35 days.
        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#retention GoogleRedisCluster#retention}
        '''
        result = self._values.get("retention")
        assert result is not None, "Required property 'retention' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterAutomatedBackupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule",
    jsii_struct_bases=[],
    name_mapping={"start_time": "startTime"},
)
class GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule:
    def __init__(
        self,
        *,
        start_time: typing.Union["GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#start_time GoogleRedisCluster#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e321155fd068d95d89c761a46aeb71e0c4d4644c2e564853899fbf2c4ea6259)
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_time": start_time,
        }

    @builtins.property
    def start_time(
        self,
    ) -> "GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#start_time GoogleRedisCluster#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cd0b9679bf386eaf47aa754ae2a1c77f904e451b578d0aa848f9c493912fff7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(self, *, hours: jsii.Number) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#hours GoogleRedisCluster#hours}
        '''
        value = GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime(
            hours=hours
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference":
        return typing.cast("GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime"]:
        return typing.cast(typing.Optional["GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule]:
        return typing.cast(typing.Optional[GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81408c8cb39e2b02823da654d65c1215f2bfb4c3e3b34626a35eacb04f95e4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime",
    jsii_struct_bases=[],
    name_mapping={"hours": "hours"},
)
class GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime:
    def __init__(self, *, hours: jsii.Number) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#hours GoogleRedisCluster#hours}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ff1b1a96b6917a9b17d00739fed64cbd0821f92da864f8d36c80a52bcd0f99)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hours": hours,
        }

    @builtins.property
    def hours(self) -> jsii.Number:
        '''Hours of a day in 24 hour format.

        Must be greater than or equal to 0 and typically must be less than or equal to 23.
        An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#hours GoogleRedisCluster#hours}
        '''
        result = self._values.get("hours")
        assert result is not None, "Required property 'hours' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cb9fb8c083f296bd1d8559965b6074ad7ac5d456cda173bafdb3d2b3a43e8e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9891f4d10f2580fe8737d0d0f3f75467e6fd771899339f71e0a85f22fd24aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime]:
        return typing.cast(typing.Optional[GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731514626d407c0f7df5dbc73a0899e6c33be15a4c541f821c3d11bf4e01eea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterAutomatedBackupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterAutomatedBackupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9baaeb5251ec3dd75913735f3bd13d0fa4c6f53c734fde331b968029ccc0739b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFixedFrequencySchedule")
    def put_fixed_frequency_schedule(
        self,
        *,
        start_time: typing.Union[GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#start_time GoogleRedisCluster#start_time}
        '''
        value = GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule(
            start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putFixedFrequencySchedule", [value]))

    @builtins.property
    @jsii.member(jsii_name="fixedFrequencySchedule")
    def fixed_frequency_schedule(
        self,
    ) -> GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleOutputReference:
        return typing.cast(GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleOutputReference, jsii.get(self, "fixedFrequencySchedule"))

    @builtins.property
    @jsii.member(jsii_name="fixedFrequencyScheduleInput")
    def fixed_frequency_schedule_input(
        self,
    ) -> typing.Optional[GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule]:
        return typing.cast(typing.Optional[GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule], jsii.get(self, "fixedFrequencyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionInput")
    def retention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionInput"))

    @builtins.property
    @jsii.member(jsii_name="retention")
    def retention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retention"))

    @retention.setter
    def retention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ae5c922835e5cf724875e9abae70abd91424363d136b2f8ac422db6b6ac4d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterAutomatedBackupConfig]:
        return typing.cast(typing.Optional[GoogleRedisClusterAutomatedBackupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterAutomatedBackupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5708489f2aa0870fb85948228c4fb5498b3843c5e17a7062d76abe9c595a90a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "shard_count": "shardCount",
        "authorization_mode": "authorizationMode",
        "automated_backup_config": "automatedBackupConfig",
        "cross_cluster_replication_config": "crossClusterReplicationConfig",
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "gcs_source": "gcsSource",
        "id": "id",
        "kms_key": "kmsKey",
        "maintenance_policy": "maintenancePolicy",
        "managed_backup_source": "managedBackupSource",
        "name": "name",
        "node_type": "nodeType",
        "persistence_config": "persistenceConfig",
        "project": "project",
        "psc_configs": "pscConfigs",
        "redis_configs": "redisConfigs",
        "region": "region",
        "replica_count": "replicaCount",
        "timeouts": "timeouts",
        "transit_encryption_mode": "transitEncryptionMode",
        "zone_distribution_config": "zoneDistributionConfig",
    },
)
class GoogleRedisClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        shard_count: jsii.Number,
        authorization_mode: typing.Optional[builtins.str] = None,
        automated_backup_config: typing.Optional[typing.Union[GoogleRedisClusterAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        cross_cluster_replication_config: typing.Optional[typing.Union["GoogleRedisClusterCrossClusterReplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs_source: typing.Optional[typing.Union["GoogleRedisClusterGcsSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        maintenance_policy: typing.Optional[typing.Union["GoogleRedisClusterMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_backup_source: typing.Optional[typing.Union["GoogleRedisClusterManagedBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["GoogleRedisClusterPersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleRedisClusterPscConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleRedisClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        zone_distribution_config: typing.Optional[typing.Union["GoogleRedisClusterZoneDistributionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param shard_count: Required. Number of shards for the Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#shard_count GoogleRedisCluster#shard_count}
        :param authorization_mode: Optional. The authorization mode of the Redis cluster. If not provided, auth feature is disabled for the cluster. Default value: "AUTH_MODE_DISABLED" Possible values: ["AUTH_MODE_UNSPECIFIED", "AUTH_MODE_IAM_AUTH", "AUTH_MODE_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#authorization_mode GoogleRedisCluster#authorization_mode}
        :param automated_backup_config: automated_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#automated_backup_config GoogleRedisCluster#automated_backup_config}
        :param cross_cluster_replication_config: cross_cluster_replication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#cross_cluster_replication_config GoogleRedisCluster#cross_cluster_replication_config}
        :param deletion_protection_enabled: Optional. Indicates if the cluster is deletion protected or not. If the value if set to true, any delete cluster operation will fail. Default value is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#deletion_protection_enabled GoogleRedisCluster#deletion_protection_enabled}
        :param gcs_source: gcs_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#gcs_source GoogleRedisCluster#gcs_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#id GoogleRedisCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key: The KMS key used to encrypt the at-rest data of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#kms_key GoogleRedisCluster#kms_key}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#maintenance_policy GoogleRedisCluster#maintenance_policy}
        :param managed_backup_source: managed_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#managed_backup_source GoogleRedisCluster#managed_backup_source}
        :param name: Unique name of the resource in this scope including project and location using the form: projects/{projectId}/locations/{locationId}/clusters/{clusterId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#name GoogleRedisCluster#name}
        :param node_type: The nodeType for the Redis cluster. If not provided, REDIS_HIGHMEM_MEDIUM will be used as default Possible values: ["REDIS_SHARED_CORE_NANO", "REDIS_HIGHMEM_MEDIUM", "REDIS_HIGHMEM_XLARGE", "REDIS_STANDARD_SMALL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#node_type GoogleRedisCluster#node_type}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#persistence_config GoogleRedisCluster#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#project GoogleRedisCluster#project}.
        :param psc_configs: psc_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#psc_configs GoogleRedisCluster#psc_configs}
        :param redis_configs: Configure Redis Cluster behavior using a subset of native Redis configuration parameters. Please check Memorystore documentation for the list of supported parameters: https://cloud.google.com/memorystore/docs/cluster/supported-instance-configurations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#redis_configs GoogleRedisCluster#redis_configs}
        :param region: The name of the region of the Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#region GoogleRedisCluster#region}
        :param replica_count: Optional. The number of replica nodes per shard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#replica_count GoogleRedisCluster#replica_count}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#timeouts GoogleRedisCluster#timeouts}
        :param transit_encryption_mode: Optional. The in-transit encryption for the Redis cluster. If not provided, encryption is disabled for the cluster. Default value: "TRANSIT_ENCRYPTION_MODE_DISABLED" Possible values: ["TRANSIT_ENCRYPTION_MODE_UNSPECIFIED", "TRANSIT_ENCRYPTION_MODE_DISABLED", "TRANSIT_ENCRYPTION_MODE_SERVER_AUTHENTICATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#transit_encryption_mode GoogleRedisCluster#transit_encryption_mode}
        :param zone_distribution_config: zone_distribution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#zone_distribution_config GoogleRedisCluster#zone_distribution_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(automated_backup_config, dict):
            automated_backup_config = GoogleRedisClusterAutomatedBackupConfig(**automated_backup_config)
        if isinstance(cross_cluster_replication_config, dict):
            cross_cluster_replication_config = GoogleRedisClusterCrossClusterReplicationConfig(**cross_cluster_replication_config)
        if isinstance(gcs_source, dict):
            gcs_source = GoogleRedisClusterGcsSource(**gcs_source)
        if isinstance(maintenance_policy, dict):
            maintenance_policy = GoogleRedisClusterMaintenancePolicy(**maintenance_policy)
        if isinstance(managed_backup_source, dict):
            managed_backup_source = GoogleRedisClusterManagedBackupSource(**managed_backup_source)
        if isinstance(persistence_config, dict):
            persistence_config = GoogleRedisClusterPersistenceConfig(**persistence_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleRedisClusterTimeouts(**timeouts)
        if isinstance(zone_distribution_config, dict):
            zone_distribution_config = GoogleRedisClusterZoneDistributionConfig(**zone_distribution_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a769d4dae5c7f36c5de16433b8294ff6e1878e822b9a46feece879b0228dc8f2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument shard_count", value=shard_count, expected_type=type_hints["shard_count"])
            check_type(argname="argument authorization_mode", value=authorization_mode, expected_type=type_hints["authorization_mode"])
            check_type(argname="argument automated_backup_config", value=automated_backup_config, expected_type=type_hints["automated_backup_config"])
            check_type(argname="argument cross_cluster_replication_config", value=cross_cluster_replication_config, expected_type=type_hints["cross_cluster_replication_config"])
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument gcs_source", value=gcs_source, expected_type=type_hints["gcs_source"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument maintenance_policy", value=maintenance_policy, expected_type=type_hints["maintenance_policy"])
            check_type(argname="argument managed_backup_source", value=managed_backup_source, expected_type=type_hints["managed_backup_source"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument persistence_config", value=persistence_config, expected_type=type_hints["persistence_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument psc_configs", value=psc_configs, expected_type=type_hints["psc_configs"])
            check_type(argname="argument redis_configs", value=redis_configs, expected_type=type_hints["redis_configs"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument replica_count", value=replica_count, expected_type=type_hints["replica_count"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument transit_encryption_mode", value=transit_encryption_mode, expected_type=type_hints["transit_encryption_mode"])
            check_type(argname="argument zone_distribution_config", value=zone_distribution_config, expected_type=type_hints["zone_distribution_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "shard_count": shard_count,
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
        if authorization_mode is not None:
            self._values["authorization_mode"] = authorization_mode
        if automated_backup_config is not None:
            self._values["automated_backup_config"] = automated_backup_config
        if cross_cluster_replication_config is not None:
            self._values["cross_cluster_replication_config"] = cross_cluster_replication_config
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if gcs_source is not None:
            self._values["gcs_source"] = gcs_source
        if id is not None:
            self._values["id"] = id
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if maintenance_policy is not None:
            self._values["maintenance_policy"] = maintenance_policy
        if managed_backup_source is not None:
            self._values["managed_backup_source"] = managed_backup_source
        if name is not None:
            self._values["name"] = name
        if node_type is not None:
            self._values["node_type"] = node_type
        if persistence_config is not None:
            self._values["persistence_config"] = persistence_config
        if project is not None:
            self._values["project"] = project
        if psc_configs is not None:
            self._values["psc_configs"] = psc_configs
        if redis_configs is not None:
            self._values["redis_configs"] = redis_configs
        if region is not None:
            self._values["region"] = region
        if replica_count is not None:
            self._values["replica_count"] = replica_count
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if transit_encryption_mode is not None:
            self._values["transit_encryption_mode"] = transit_encryption_mode
        if zone_distribution_config is not None:
            self._values["zone_distribution_config"] = zone_distribution_config

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
    def shard_count(self) -> jsii.Number:
        '''Required. Number of shards for the Redis cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#shard_count GoogleRedisCluster#shard_count}
        '''
        result = self._values.get("shard_count")
        assert result is not None, "Required property 'shard_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def authorization_mode(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The authorization mode of the Redis cluster. If not provided, auth feature is disabled for the cluster. Default value: "AUTH_MODE_DISABLED" Possible values: ["AUTH_MODE_UNSPECIFIED", "AUTH_MODE_IAM_AUTH", "AUTH_MODE_DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#authorization_mode GoogleRedisCluster#authorization_mode}
        '''
        result = self._values.get("authorization_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automated_backup_config(
        self,
    ) -> typing.Optional[GoogleRedisClusterAutomatedBackupConfig]:
        '''automated_backup_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#automated_backup_config GoogleRedisCluster#automated_backup_config}
        '''
        result = self._values.get("automated_backup_config")
        return typing.cast(typing.Optional[GoogleRedisClusterAutomatedBackupConfig], result)

    @builtins.property
    def cross_cluster_replication_config(
        self,
    ) -> typing.Optional["GoogleRedisClusterCrossClusterReplicationConfig"]:
        '''cross_cluster_replication_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#cross_cluster_replication_config GoogleRedisCluster#cross_cluster_replication_config}
        '''
        result = self._values.get("cross_cluster_replication_config")
        return typing.cast(typing.Optional["GoogleRedisClusterCrossClusterReplicationConfig"], result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Indicates if the cluster is deletion protected or not.
        If the value if set to true, any delete cluster operation will fail.
        Default value is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#deletion_protection_enabled GoogleRedisCluster#deletion_protection_enabled}
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs_source(self) -> typing.Optional["GoogleRedisClusterGcsSource"]:
        '''gcs_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#gcs_source GoogleRedisCluster#gcs_source}
        '''
        result = self._values.get("gcs_source")
        return typing.cast(typing.Optional["GoogleRedisClusterGcsSource"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#id GoogleRedisCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The KMS key used to encrypt the at-rest data of the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#kms_key GoogleRedisCluster#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_policy(
        self,
    ) -> typing.Optional["GoogleRedisClusterMaintenancePolicy"]:
        '''maintenance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#maintenance_policy GoogleRedisCluster#maintenance_policy}
        '''
        result = self._values.get("maintenance_policy")
        return typing.cast(typing.Optional["GoogleRedisClusterMaintenancePolicy"], result)

    @builtins.property
    def managed_backup_source(
        self,
    ) -> typing.Optional["GoogleRedisClusterManagedBackupSource"]:
        '''managed_backup_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#managed_backup_source GoogleRedisCluster#managed_backup_source}
        '''
        result = self._values.get("managed_backup_source")
        return typing.cast(typing.Optional["GoogleRedisClusterManagedBackupSource"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Unique name of the resource in this scope including project and location using the form: projects/{projectId}/locations/{locationId}/clusters/{clusterId}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#name GoogleRedisCluster#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''The nodeType for the Redis cluster.

        If not provided, REDIS_HIGHMEM_MEDIUM will be used as default Possible values: ["REDIS_SHARED_CORE_NANO", "REDIS_HIGHMEM_MEDIUM", "REDIS_HIGHMEM_XLARGE", "REDIS_STANDARD_SMALL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#node_type GoogleRedisCluster#node_type}
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def persistence_config(
        self,
    ) -> typing.Optional["GoogleRedisClusterPersistenceConfig"]:
        '''persistence_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#persistence_config GoogleRedisCluster#persistence_config}
        '''
        result = self._values.get("persistence_config")
        return typing.cast(typing.Optional["GoogleRedisClusterPersistenceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#project GoogleRedisCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterPscConfigs"]]]:
        '''psc_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#psc_configs GoogleRedisCluster#psc_configs}
        '''
        result = self._values.get("psc_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterPscConfigs"]]], result)

    @builtins.property
    def redis_configs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Configure Redis Cluster behavior using a subset of native Redis configuration parameters.

        Please check Memorystore documentation for the list of supported parameters:
        https://cloud.google.com/memorystore/docs/cluster/supported-instance-configurations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#redis_configs GoogleRedisCluster#redis_configs}
        '''
        result = self._values.get("redis_configs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The name of the region of the Redis cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#region GoogleRedisCluster#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Optional. The number of replica nodes per shard.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#replica_count GoogleRedisCluster#replica_count}
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleRedisClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#timeouts GoogleRedisCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleRedisClusterTimeouts"], result)

    @builtins.property
    def transit_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The in-transit encryption for the Redis cluster.
        If not provided, encryption is disabled for the cluster. Default value: "TRANSIT_ENCRYPTION_MODE_DISABLED" Possible values: ["TRANSIT_ENCRYPTION_MODE_UNSPECIFIED", "TRANSIT_ENCRYPTION_MODE_DISABLED", "TRANSIT_ENCRYPTION_MODE_SERVER_AUTHENTICATION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#transit_encryption_mode GoogleRedisCluster#transit_encryption_mode}
        '''
        result = self._values.get("transit_encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_distribution_config(
        self,
    ) -> typing.Optional["GoogleRedisClusterZoneDistributionConfig"]:
        '''zone_distribution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#zone_distribution_config GoogleRedisCluster#zone_distribution_config}
        '''
        result = self._values.get("zone_distribution_config")
        return typing.cast(typing.Optional["GoogleRedisClusterZoneDistributionConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_role": "clusterRole",
        "primary_cluster": "primaryCluster",
        "secondary_clusters": "secondaryClusters",
    },
)
class GoogleRedisClusterCrossClusterReplicationConfig:
    def __init__(
        self,
        *,
        cluster_role: typing.Optional[builtins.str] = None,
        primary_cluster: typing.Optional[typing.Union["GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cluster_role: The role of the cluster in cross cluster replication. Supported values are:. 1. 'CLUSTER_ROLE_UNSPECIFIED': This is an independent cluster that has never participated in cross cluster replication. It allows both reads and writes. 1. 'NONE': This is an independent cluster that previously participated in cross cluster replication(either as a 'PRIMARY' or 'SECONDARY' cluster). It allows both reads and writes. 1. 'PRIMARY': This cluster serves as the replication source for secondary clusters that are replicating from it. Any data written to it is automatically replicated to its secondary clusters. It allows both reads and writes. 1. 'SECONDARY': This cluster replicates data from the primary cluster. It allows only reads. Possible values: ["CLUSTER_ROLE_UNSPECIFIED", "NONE", "PRIMARY", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#cluster_role GoogleRedisCluster#cluster_role}
        :param primary_cluster: primary_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#primary_cluster GoogleRedisCluster#primary_cluster}
        :param secondary_clusters: secondary_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#secondary_clusters GoogleRedisCluster#secondary_clusters}
        '''
        if isinstance(primary_cluster, dict):
            primary_cluster = GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster(**primary_cluster)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a4562145e1724425bc64d28efab38701cfe13afa7e9018930ccf722f7ddc10)
            check_type(argname="argument cluster_role", value=cluster_role, expected_type=type_hints["cluster_role"])
            check_type(argname="argument primary_cluster", value=primary_cluster, expected_type=type_hints["primary_cluster"])
            check_type(argname="argument secondary_clusters", value=secondary_clusters, expected_type=type_hints["secondary_clusters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_role is not None:
            self._values["cluster_role"] = cluster_role
        if primary_cluster is not None:
            self._values["primary_cluster"] = primary_cluster
        if secondary_clusters is not None:
            self._values["secondary_clusters"] = secondary_clusters

    @builtins.property
    def cluster_role(self) -> typing.Optional[builtins.str]:
        '''The role of the cluster in cross cluster replication. Supported values are:.

        1. 'CLUSTER_ROLE_UNSPECIFIED': This is an independent cluster that has never participated in cross cluster replication. It allows both reads and writes.
        2. 'NONE': This is an independent cluster that previously participated in cross cluster replication(either as a 'PRIMARY' or 'SECONDARY' cluster). It allows both reads and writes.
        3. 'PRIMARY': This cluster serves as the replication source for secondary clusters that are replicating from it. Any data written to it is automatically replicated to its secondary clusters. It allows both reads and writes.
        4. 'SECONDARY': This cluster replicates data from the primary cluster. It allows only reads. Possible values: ["CLUSTER_ROLE_UNSPECIFIED", "NONE", "PRIMARY", "SECONDARY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#cluster_role GoogleRedisCluster#cluster_role}
        '''
        result = self._values.get("cluster_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_cluster(
        self,
    ) -> typing.Optional["GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster"]:
        '''primary_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#primary_cluster GoogleRedisCluster#primary_cluster}
        '''
        result = self._values.get("primary_cluster")
        return typing.cast(typing.Optional["GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster"], result)

    @builtins.property
    def secondary_clusters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters"]]]:
        '''secondary_clusters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#secondary_clusters GoogleRedisCluster#secondary_clusters}
        '''
        result = self._values.get("secondary_clusters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterCrossClusterReplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigMembership",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleRedisClusterCrossClusterReplicationConfigMembership:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterCrossClusterReplicationConfigMembership(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterCrossClusterReplicationConfigMembershipList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigMembershipList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c18119b0a1f4ccb8ffb4c64cb2689ff19562b9442518f0f1d78cc94432d2947)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleRedisClusterCrossClusterReplicationConfigMembershipOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5746835521c9710d249988b7b1a97cffb8ab43c08281512ffdb2c649b4b334)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterCrossClusterReplicationConfigMembershipOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf625ecedefce53cf9dac2ae39190d16cd30725deeddb527e0302ac43c6562d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d31b9fdd6e6b0d518670bc8b072645bf8f6e61a3fe47e4c6b9c3deb44fa65c74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a53e0072c6b98cbbfdef7cf6c290b5d6f09c60684b446a2324fc19c71e7c4034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterCrossClusterReplicationConfigMembershipOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigMembershipOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13a460d586281ee4bac210bebcd084ffd2567aa3fe4eadf9b113792e80e9aeaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="primaryCluster")
    def primary_cluster(
        self,
    ) -> "GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterList":
        return typing.cast("GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterList", jsii.get(self, "primaryCluster"))

    @builtins.property
    @jsii.member(jsii_name="secondaryClusters")
    def secondary_clusters(
        self,
    ) -> "GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersList":
        return typing.cast("GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersList", jsii.get(self, "secondaryClusters"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembership]:
        return typing.cast(typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembership], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembership],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db4902b92a3d63588e406c1b3dddd97949e6eb93152ccab9f63ca7bdf78ddc89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13e0c4dfeb65b5fffa4b3bbde9247c776ca09b92b611f4156671a608595d2269)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3655d498131eba6324ca4ff2a2a4f1909217a23a0c8885643ed43e954d8785ec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e660209bd660e8dd6f94f0d56307c56c7001229ec6198de638ac9ea87dd91f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__968f78ac9b2345c435d51ab693fb2c80c1306a6fe1cde015b42f7dda409973a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1970c6f676fe7d4bdb8330dc9f5edd4fb0cecc338fb95c4655737fe66cd97790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a29e9274a2fc850438146c0679ad9682b593f6ffda0af1d98fc4e79f01d3566)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster]:
        return typing.cast(typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17285d7e863d8256e4b502df5cb69e26c6e469c6558acc949b20953177508820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b338b214e43c83d854e378cc8f438573ab903b38ff3b02d4fdd0aab5301dfd58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb8698edb7bfb3c19ca2457a62907fd6fb8d1100f221b2ff5569043a9f98128)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7561b57ee686057a69d988185e219ae0012a0b4c6031d0449774025d1d8bfb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a9eb9c9b34234595c6990d84e34389e6edf97cde662cdca833f14c29c6cab10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd19c56e0e9877426b3a685e927a021f9d5b42a5825afe1eaaa01af7bfa224f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77c360c9c740eb7b6a0f04ae1c7a8040ef83265a9d895b517ec1fedcb0a66ca1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters]:
        return typing.cast(typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1664971886e14199da3d51624508492fd3f3fe950ebe5c6eaef76ef08ba2e9a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterCrossClusterReplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__772dee1f8db967ac6aa51fb7fcdb79d0e6ac77f61bc672d33249550454f81b4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrimaryCluster")
    def put_primary_cluster(
        self,
        *,
        cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster: The full resource path of the primary cluster in the format: projects/{project}/locations/{region}/clusters/{cluster-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#cluster GoogleRedisCluster#cluster}
        '''
        value = GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster(
            cluster=cluster
        )

        return typing.cast(None, jsii.invoke(self, "putPrimaryCluster", [value]))

    @jsii.member(jsii_name="putSecondaryClusters")
    def put_secondary_clusters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2cb368a143a955e4019c6fae70a071c817e17bdbc1d1730f310feb5aeda1add)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecondaryClusters", [value]))

    @jsii.member(jsii_name="resetClusterRole")
    def reset_cluster_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterRole", []))

    @jsii.member(jsii_name="resetPrimaryCluster")
    def reset_primary_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryCluster", []))

    @jsii.member(jsii_name="resetSecondaryClusters")
    def reset_secondary_clusters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryClusters", []))

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(
        self,
    ) -> GoogleRedisClusterCrossClusterReplicationConfigMembershipList:
        return typing.cast(GoogleRedisClusterCrossClusterReplicationConfigMembershipList, jsii.get(self, "membership"))

    @builtins.property
    @jsii.member(jsii_name="primaryCluster")
    def primary_cluster(
        self,
    ) -> "GoogleRedisClusterCrossClusterReplicationConfigPrimaryClusterOutputReference":
        return typing.cast("GoogleRedisClusterCrossClusterReplicationConfigPrimaryClusterOutputReference", jsii.get(self, "primaryCluster"))

    @builtins.property
    @jsii.member(jsii_name="secondaryClusters")
    def secondary_clusters(
        self,
    ) -> "GoogleRedisClusterCrossClusterReplicationConfigSecondaryClustersList":
        return typing.cast("GoogleRedisClusterCrossClusterReplicationConfigSecondaryClustersList", jsii.get(self, "secondaryClusters"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="clusterRoleInput")
    def cluster_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryClusterInput")
    def primary_cluster_input(
        self,
    ) -> typing.Optional["GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster"]:
        return typing.cast(typing.Optional["GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster"], jsii.get(self, "primaryClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryClustersInput")
    def secondary_clusters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters"]]], jsii.get(self, "secondaryClustersInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterRole")
    def cluster_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterRole"))

    @cluster_role.setter
    def cluster_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fb736ad98a095b40cdfc2444a2cb0c48beb6c62605c8552372cfab3881b2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterCrossClusterReplicationConfig]:
        return typing.cast(typing.Optional[GoogleRedisClusterCrossClusterReplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterCrossClusterReplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e22336135f3dd35ed9ef25b075cee71d0312de3d3fa5eef6306a7490cd441b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster"},
)
class GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster:
    def __init__(self, *, cluster: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cluster: The full resource path of the primary cluster in the format: projects/{project}/locations/{region}/clusters/{cluster-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#cluster GoogleRedisCluster#cluster}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97cbf58e0232caf916026a805afdb209d6aa8e03cd16a0e6ee5faf448e32f311)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster is not None:
            self._values["cluster"] = cluster

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''The full resource path of the primary cluster in the format: projects/{project}/locations/{region}/clusters/{cluster-id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#cluster GoogleRedisCluster#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterCrossClusterReplicationConfigPrimaryClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigPrimaryClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa265bd682aaeab9b76b21003d562590fdedfefb70f2d09b3fc7c25964bc5bbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCluster")
    def reset_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCluster", []))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6ca44f878347e099e8a99e3342e597565d9ea1df8a8259356e0bbfddca3e82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster]:
        return typing.cast(typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f6ce32a42bff9b5a7b67f68f26182af16148baba2721cb4bfa4ed0fb1e5dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster"},
)
class GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters:
    def __init__(self, *, cluster: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cluster: The full resource path of the secondary cluster in the format: projects/{project}/locations/{region}/clusters/{cluster-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#cluster GoogleRedisCluster#cluster}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8ebb5bccd29b1bb96b130518421f6d1979a80f4a6e2cf82829569d2ccc78b5)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster is not None:
            self._values["cluster"] = cluster

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''The full resource path of the secondary cluster in the format: projects/{project}/locations/{region}/clusters/{cluster-id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#cluster GoogleRedisCluster#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterCrossClusterReplicationConfigSecondaryClustersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigSecondaryClustersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__648e8c54fac614c3aceb522540a53a1613a208aa34b7b7bd11988d1fff7f4012)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleRedisClusterCrossClusterReplicationConfigSecondaryClustersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f28ca0968524be4f989d0204def7ada36e1e84cff91d1aded3a5e6f7904d2d6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterCrossClusterReplicationConfigSecondaryClustersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c82c5633a0c64de4f8c0b498fe09a0392b42527ff3d7ad85aa55a4023f34c88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6c586a41bbead36966152b382a20a8da84782f979dd6a41a572d106b23f963b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__481ef4f760524409fc52f6341f5462a19f8453706b4cec824bf9f443117aa0b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8221409ff905de8ada52155ad477f67f26e54876da0cbb610dd859ca96b8cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterCrossClusterReplicationConfigSecondaryClustersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterCrossClusterReplicationConfigSecondaryClustersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04bb6f29ba4d5c4acf6e9d3c2a1a792eb837b58501ec76a4b85410a97c57da9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCluster")
    def reset_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCluster", []))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45870e063eb18228ff6b31e0cb9a84194aca5ae74b3574b5aaa23296b53a5fdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00c2bb85b8698584759c64a365a4c4aa5a0e46fc7d1727ee1649a8c688142f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterDiscoveryEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleRedisClusterDiscoveryEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterDiscoveryEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterDiscoveryEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterDiscoveryEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__359e2089b1e5fbc815f14be1981d2cddd98d76ad2fb87179806d8ba73c35fcc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleRedisClusterDiscoveryEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e57ba031bef1fae202adadbeb32f07227fd693af0ecf9d1e890b1cc532ad1f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterDiscoveryEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1960688266eec07fb26a0aaf82ecfb5bd2eef5ed8bd6f95eb704efaca49440)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c0b4273e730873afcbb5af556d3d99b0d09f88ffac0294893fd4e47fdd44161)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bcaecdaac443d7ef7b8ae5f8ac95b920686dd69f1ffec78343358e427891bf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterDiscoveryEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterDiscoveryEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2124372e3e90746a66c1e2ea57a0a69bcc5c2c7fcccd05559e8181cf58b03004)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="pscConfig")
    def psc_config(self) -> "GoogleRedisClusterDiscoveryEndpointsPscConfigList":
        return typing.cast("GoogleRedisClusterDiscoveryEndpointsPscConfigList", jsii.get(self, "pscConfig"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleRedisClusterDiscoveryEndpoints]:
        return typing.cast(typing.Optional[GoogleRedisClusterDiscoveryEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterDiscoveryEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e1564ac180aad6adbde43511d6dcd876cdaecc1e0892b09707e33a408ba382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterDiscoveryEndpointsPscConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleRedisClusterDiscoveryEndpointsPscConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterDiscoveryEndpointsPscConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterDiscoveryEndpointsPscConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterDiscoveryEndpointsPscConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed9eb789dfd339950f565193f000276a3efcb351b97cd2d6d3da9a830cfd1341)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleRedisClusterDiscoveryEndpointsPscConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046e574789714c35860f777da363511063f80380e6edac5d9f305992ecab1a6d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterDiscoveryEndpointsPscConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1696f3d7d27eb636492c7f719459811105c139ca5e6e5c97a46f6b942ca354f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fa1493f879fe87ab67f9df1879e77e2fce7a9495dca1e5ddbaef59bfc0411ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3df02122959c73d88266360cc4f44881cbba35a086d257d0e892430d24ce4d39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterDiscoveryEndpointsPscConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterDiscoveryEndpointsPscConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__347c1d7f82af063caf2aa29ef65d4c9535dfdc76cb00535f51273b0885d69230)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterDiscoveryEndpointsPscConfig]:
        return typing.cast(typing.Optional[GoogleRedisClusterDiscoveryEndpointsPscConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterDiscoveryEndpointsPscConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeec9f307274baf0167c54dcca8c5d6baa068d59da3b91210191bd84f11eec8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterGcsSource",
    jsii_struct_bases=[],
    name_mapping={"uris": "uris"},
)
class GoogleRedisClusterGcsSource:
    def __init__(self, *, uris: typing.Sequence[builtins.str]) -> None:
        '''
        :param uris: URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#uris GoogleRedisCluster#uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640fa3eb040bf3c7a315a01581c5b967ce13b15a21d22bd7e1014d5403e4063e)
            check_type(argname="argument uris", value=uris, expected_type=type_hints["uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uris": uris,
        }

    @builtins.property
    def uris(self) -> typing.List[builtins.str]:
        '''URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#uris GoogleRedisCluster#uris}
        '''
        result = self._values.get("uris")
        assert result is not None, "Required property 'uris' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterGcsSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterGcsSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterGcsSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__add5145c891087d27ceed6cfc32ffb05b2fb8b6f8c85fdc8039fff73feffe3b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="urisInput")
    def uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "urisInput"))

    @builtins.property
    @jsii.member(jsii_name="uris")
    def uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "uris"))

    @uris.setter
    def uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026e5c7bbe3b81a778386e6016efeac08148693cbdfcfd38cf9360f80eb2b836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleRedisClusterGcsSource]:
        return typing.cast(typing.Optional[GoogleRedisClusterGcsSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterGcsSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8492d44b1e5726f153b16251172d19ccbf3dea8cdd46fecffe70e09e835fd574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterMaintenancePolicy",
    jsii_struct_bases=[],
    name_mapping={"weekly_maintenance_window": "weeklyMaintenanceWindow"},
)
class GoogleRedisClusterMaintenancePolicy:
    def __init__(
        self,
        *,
        weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#weekly_maintenance_window GoogleRedisCluster#weekly_maintenance_window}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075f3caf6b66a07c55f7497ccd05fe3f204fa2767b2fdbce075ff3453f5d312d)
            check_type(argname="argument weekly_maintenance_window", value=weekly_maintenance_window, expected_type=type_hints["weekly_maintenance_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if weekly_maintenance_window is not None:
            self._values["weekly_maintenance_window"] = weekly_maintenance_window

    @builtins.property
    def weekly_maintenance_window(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow"]]]:
        '''weekly_maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#weekly_maintenance_window GoogleRedisCluster#weekly_maintenance_window}
        '''
        result = self._values.get("weekly_maintenance_window")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterMaintenancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterMaintenancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterMaintenancePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b8e2d866fc3ae373e6c2436d9a365a0823eeff6ac07d08ec7f1689126eb6503)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWeeklyMaintenanceWindow")
    def put_weekly_maintenance_window(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a95a9d9dad1dc5a6b4a4df7f5e1e2286421f05a268e5357106384382f08fb7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWeeklyMaintenanceWindow", [value]))

    @jsii.member(jsii_name="resetWeeklyMaintenanceWindow")
    def reset_weekly_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklyMaintenanceWindow", []))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="weeklyMaintenanceWindow")
    def weekly_maintenance_window(
        self,
    ) -> "GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowList":
        return typing.cast("GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowList", jsii.get(self, "weeklyMaintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="weeklyMaintenanceWindowInput")
    def weekly_maintenance_window_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow"]]], jsii.get(self, "weeklyMaintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleRedisClusterMaintenancePolicy]:
        return typing.cast(typing.Optional[GoogleRedisClusterMaintenancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterMaintenancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e783a8395df99d346a9bbd194ee227c6efc0ad6e1b0f48be347c9e6ef6b311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "start_time": "startTime"},
)
class GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow:
    def __init__(
        self,
        *,
        day: builtins.str,
        start_time: typing.Union["GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day: Required. The day of week that maintenance updates occur. - DAY_OF_WEEK_UNSPECIFIED: The day of the week is unspecified. - MONDAY: Monday - TUESDAY: Tuesday - WEDNESDAY: Wednesday - THURSDAY: Thursday - FRIDAY: Friday - SATURDAY: Saturday - SUNDAY: Sunday Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#day GoogleRedisCluster#day}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#start_time GoogleRedisCluster#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9888a1a0660dd934a8554a8ccb96624b5cf55241156514650d473e8ca50290c1)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "start_time": start_time,
        }

    @builtins.property
    def day(self) -> builtins.str:
        '''Required. The day of week that maintenance updates occur.

        - DAY_OF_WEEK_UNSPECIFIED: The day of the week is unspecified.
        - MONDAY: Monday
        - TUESDAY: Tuesday
        - WEDNESDAY: Wednesday
        - THURSDAY: Thursday
        - FRIDAY: Friday
        - SATURDAY: Saturday
        - SUNDAY: Sunday Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#day GoogleRedisCluster#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(
        self,
    ) -> "GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#start_time GoogleRedisCluster#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8adb52f0faa28cd96b639cb2cce1e6c06a0eaf829ec40164f3c95080f6f1db13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc01eadec8cef67c5f479c8abcef1ee83139a92f1ce58b00451916b71ceda9fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2464c48c65b3b4e4210f6e2ea4cea500d7412b2fa58c2243472278ff0ee510b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3018171a60f26c8d7165e04d922331c076fc9acaea3f52830ab5fe024073604f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__550b7503adf72c6c83a5148bbd630f7cae5568123f52380f87e3c13dc0df88c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0266a96ecd0f92e4251e4b0c4af70a6f8f2dfdcf52d7bc68d687564da0c63be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3e1cdffafdf2897a1d5a812dcdeaf6862869250b2e3058d17117c0c924ddbff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#hours GoogleRedisCluster#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#minutes GoogleRedisCluster#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#nanos GoogleRedisCluster#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#seconds GoogleRedisCluster#seconds}
        '''
        value = GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference":
        return typing.cast("GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime"]:
        return typing.cast(typing.Optional["GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9485b9a3a317cc8af402239e78369f0bfff3f492300dd71e3f42c50891b6c84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54b6e74391af924af08961623985075118513bbf1990bc03c39d0dc77626e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#hours GoogleRedisCluster#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#minutes GoogleRedisCluster#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#nanos GoogleRedisCluster#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#seconds GoogleRedisCluster#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbbc3150680f45546a4144ca8b8c348741389d922ceb074a11412bc318e3ebdc)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of day in 24 hour format.

        Should be from 0 to 23.
        An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#hours GoogleRedisCluster#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#minutes GoogleRedisCluster#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#nanos GoogleRedisCluster#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time.

        Must normally be from 0 to 59.
        An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#seconds GoogleRedisCluster#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e88548335c5ac56d2597252c544153d78976ec761de27ae4d8a9e805323a190)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b0b5b0e4508da56c0ab91e6f6acf755c6317805fb185eb0bf6b7bb5118f864)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e781848b8a3fd342ea5d4388183d42bcc7885ae5184fd29db7811a626210a323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159632bb7a14192e78370c59c43f387c3e83b9984389f20ace0da2d8d8d8bb8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1386ea7e673c070f23088c63aff935a15e60a185a7bf1e1fe4c13ca6949faeb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime]:
        return typing.cast(typing.Optional[GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84623036c7f84b95f00835c7fbd04dca22089d580182ea47a2f8865e5cdbf31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterMaintenanceSchedule",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleRedisClusterMaintenanceSchedule:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterMaintenanceSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterMaintenanceScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterMaintenanceScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e83ddcf6c2a63e494b23d6eae39159675a25d93db5012c06462a17e81291d4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleRedisClusterMaintenanceScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__004560d6aba93ebea5126293eb4517ff103b0d8cfa5edb7d6e1e6c994326d7d4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterMaintenanceScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79727fc259dc8db2c708f41d2cb931a101c2083e9be78a55d606be37c5143bd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bae9320b724f3588a199a8b3317d487918472a4c4ea561a981cee138c39b307f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__513e76ec522b00ad2a57c059ce10652f37ce0a6e3cf35a55d3b9b5211b7a6601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterMaintenanceScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterMaintenanceScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__caf9d1c361d05a854293197e270448f27b7d64ba0a6ac50c6e2888a0ea4cf3d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="scheduleDeadlineTime")
    def schedule_deadline_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleDeadlineTime"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleRedisClusterMaintenanceSchedule]:
        return typing.cast(typing.Optional[GoogleRedisClusterMaintenanceSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterMaintenanceSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7982f745237a5a9a7d97e2c7d74c7972708002ee5ecb98c8482d35f10164d6f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterManagedBackupSource",
    jsii_struct_bases=[],
    name_mapping={"backup": "backup"},
)
class GoogleRedisClusterManagedBackupSource:
    def __init__(self, *, backup: builtins.str) -> None:
        '''
        :param backup: Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#backup GoogleRedisCluster#backup}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b5fe8cb12d5415d9570c0ad9d884b7f4cc85910284178cf4264b65bcedcc79)
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup": backup,
        }

    @builtins.property
    def backup(self) -> builtins.str:
        '''Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#backup GoogleRedisCluster#backup}
        '''
        result = self._values.get("backup")
        assert result is not None, "Required property 'backup' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterManagedBackupSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterManagedBackupSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterManagedBackupSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a19208788f7d4ac944d851f8c659154764b198b122088e82a8b307a69576edaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="backup")
    def backup(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backup"))

    @backup.setter
    def backup(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55711fb11420df1b2715feaac60d52a2af0b6aca4143a32b6b416df642a07c70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleRedisClusterManagedBackupSource]:
        return typing.cast(typing.Optional[GoogleRedisClusterManagedBackupSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterManagedBackupSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61711dbdfa3b83fdfefeacc4265c4e1ea24f03717d57ae7b93d6f136aa27bc6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPersistenceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aof_config": "aofConfig",
        "mode": "mode",
        "rdb_config": "rdbConfig",
    },
)
class GoogleRedisClusterPersistenceConfig:
    def __init__(
        self,
        *,
        aof_config: typing.Optional[typing.Union["GoogleRedisClusterPersistenceConfigAofConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        rdb_config: typing.Optional[typing.Union["GoogleRedisClusterPersistenceConfigRdbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aof_config: aof_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#aof_config GoogleRedisCluster#aof_config}
        :param mode: Optional. Controls whether Persistence features are enabled. If not provided, the existing value will be used. - DISABLED: Persistence (both backup and restore) is disabled for the cluster. - RDB: RDB based Persistence is enabled. - AOF: AOF based Persistence is enabled. Possible values: ["PERSISTENCE_MODE_UNSPECIFIED", "DISABLED", "RDB", "AOF"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#mode GoogleRedisCluster#mode}
        :param rdb_config: rdb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#rdb_config GoogleRedisCluster#rdb_config}
        '''
        if isinstance(aof_config, dict):
            aof_config = GoogleRedisClusterPersistenceConfigAofConfig(**aof_config)
        if isinstance(rdb_config, dict):
            rdb_config = GoogleRedisClusterPersistenceConfigRdbConfig(**rdb_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1101e46a05e463205a4df4ed6c756471dfca26fe8ccf11f98e53702cda9e5da)
            check_type(argname="argument aof_config", value=aof_config, expected_type=type_hints["aof_config"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument rdb_config", value=rdb_config, expected_type=type_hints["rdb_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aof_config is not None:
            self._values["aof_config"] = aof_config
        if mode is not None:
            self._values["mode"] = mode
        if rdb_config is not None:
            self._values["rdb_config"] = rdb_config

    @builtins.property
    def aof_config(
        self,
    ) -> typing.Optional["GoogleRedisClusterPersistenceConfigAofConfig"]:
        '''aof_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#aof_config GoogleRedisCluster#aof_config}
        '''
        result = self._values.get("aof_config")
        return typing.cast(typing.Optional["GoogleRedisClusterPersistenceConfigAofConfig"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Controls whether Persistence features are enabled. If not provided, the existing value will be used.

        - DISABLED: 	Persistence (both backup and restore) is disabled for the cluster.
        - RDB: RDB based Persistence is enabled.
        - AOF: AOF based Persistence is enabled. Possible values: ["PERSISTENCE_MODE_UNSPECIFIED", "DISABLED", "RDB", "AOF"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#mode GoogleRedisCluster#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_config(
        self,
    ) -> typing.Optional["GoogleRedisClusterPersistenceConfigRdbConfig"]:
        '''rdb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#rdb_config GoogleRedisCluster#rdb_config}
        '''
        result = self._values.get("rdb_config")
        return typing.cast(typing.Optional["GoogleRedisClusterPersistenceConfigRdbConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterPersistenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPersistenceConfigAofConfig",
    jsii_struct_bases=[],
    name_mapping={"append_fsync": "appendFsync"},
)
class GoogleRedisClusterPersistenceConfigAofConfig:
    def __init__(self, *, append_fsync: typing.Optional[builtins.str] = None) -> None:
        '''
        :param append_fsync: Optional. Available fsync modes. - NO - Do not explicitly call fsync(). Rely on OS defaults. - EVERYSEC - Call fsync() once per second in a background thread. A balance between performance and durability. - ALWAYS - Call fsync() for earch write command. Possible values: ["APPEND_FSYNC_UNSPECIFIED", "NO", "EVERYSEC", "ALWAYS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#append_fsync GoogleRedisCluster#append_fsync}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3266a6a21cb6d327dc4cdd2f87571b87a64542b6752e12809ee571e5d92e0bd)
            check_type(argname="argument append_fsync", value=append_fsync, expected_type=type_hints["append_fsync"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if append_fsync is not None:
            self._values["append_fsync"] = append_fsync

    @builtins.property
    def append_fsync(self) -> typing.Optional[builtins.str]:
        '''Optional. Available fsync modes.

        - NO - Do not explicitly call fsync(). Rely on OS defaults.
        - EVERYSEC - Call fsync() once per second in a background thread. A balance between performance and durability.
        - ALWAYS - Call fsync() for earch write command. Possible values: ["APPEND_FSYNC_UNSPECIFIED", "NO", "EVERYSEC", "ALWAYS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#append_fsync GoogleRedisCluster#append_fsync}
        '''
        result = self._values.get("append_fsync")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterPersistenceConfigAofConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterPersistenceConfigAofConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPersistenceConfigAofConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0bc41637c95d3946e0d9a886b800468c74c8b36374b6a6b3f16985ef50d7f55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAppendFsync")
    def reset_append_fsync(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppendFsync", []))

    @builtins.property
    @jsii.member(jsii_name="appendFsyncInput")
    def append_fsync_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appendFsyncInput"))

    @builtins.property
    @jsii.member(jsii_name="appendFsync")
    def append_fsync(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appendFsync"))

    @append_fsync.setter
    def append_fsync(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea99b663e90e18f7561b1a16c6340b7cb8651c733a6d7379ea95a64540987ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appendFsync", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterPersistenceConfigAofConfig]:
        return typing.cast(typing.Optional[GoogleRedisClusterPersistenceConfigAofConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterPersistenceConfigAofConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9c10762c362e8e0334d34f82987016fb56edd10e5399bd7309ff498a4eee7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterPersistenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPersistenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ada6fa70ef5b6ab84db7311d73a4c7900b5994033727f2de680010b0b27db5cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAofConfig")
    def put_aof_config(
        self,
        *,
        append_fsync: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param append_fsync: Optional. Available fsync modes. - NO - Do not explicitly call fsync(). Rely on OS defaults. - EVERYSEC - Call fsync() once per second in a background thread. A balance between performance and durability. - ALWAYS - Call fsync() for earch write command. Possible values: ["APPEND_FSYNC_UNSPECIFIED", "NO", "EVERYSEC", "ALWAYS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#append_fsync GoogleRedisCluster#append_fsync}
        '''
        value = GoogleRedisClusterPersistenceConfigAofConfig(append_fsync=append_fsync)

        return typing.cast(None, jsii.invoke(self, "putAofConfig", [value]))

    @jsii.member(jsii_name="putRdbConfig")
    def put_rdb_config(
        self,
        *,
        rdb_snapshot_period: typing.Optional[builtins.str] = None,
        rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rdb_snapshot_period: Optional. Available snapshot periods for scheduling. - ONE_HOUR: Snapshot every 1 hour. - SIX_HOURS: Snapshot every 6 hours. - TWELVE_HOURS: Snapshot every 12 hours. - TWENTY_FOUR_HOURS: Snapshot every 24 hours. Possible values: ["SNAPSHOT_PERIOD_UNSPECIFIED", "ONE_HOUR", "SIX_HOURS", "TWELVE_HOURS", "TWENTY_FOUR_HOURS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#rdb_snapshot_period GoogleRedisCluster#rdb_snapshot_period}
        :param rdb_snapshot_start_time: The time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#rdb_snapshot_start_time GoogleRedisCluster#rdb_snapshot_start_time}
        '''
        value = GoogleRedisClusterPersistenceConfigRdbConfig(
            rdb_snapshot_period=rdb_snapshot_period,
            rdb_snapshot_start_time=rdb_snapshot_start_time,
        )

        return typing.cast(None, jsii.invoke(self, "putRdbConfig", [value]))

    @jsii.member(jsii_name="resetAofConfig")
    def reset_aof_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAofConfig", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetRdbConfig")
    def reset_rdb_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbConfig", []))

    @builtins.property
    @jsii.member(jsii_name="aofConfig")
    def aof_config(self) -> GoogleRedisClusterPersistenceConfigAofConfigOutputReference:
        return typing.cast(GoogleRedisClusterPersistenceConfigAofConfigOutputReference, jsii.get(self, "aofConfig"))

    @builtins.property
    @jsii.member(jsii_name="rdbConfig")
    def rdb_config(
        self,
    ) -> "GoogleRedisClusterPersistenceConfigRdbConfigOutputReference":
        return typing.cast("GoogleRedisClusterPersistenceConfigRdbConfigOutputReference", jsii.get(self, "rdbConfig"))

    @builtins.property
    @jsii.member(jsii_name="aofConfigInput")
    def aof_config_input(
        self,
    ) -> typing.Optional[GoogleRedisClusterPersistenceConfigAofConfig]:
        return typing.cast(typing.Optional[GoogleRedisClusterPersistenceConfigAofConfig], jsii.get(self, "aofConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbConfigInput")
    def rdb_config_input(
        self,
    ) -> typing.Optional["GoogleRedisClusterPersistenceConfigRdbConfig"]:
        return typing.cast(typing.Optional["GoogleRedisClusterPersistenceConfigRdbConfig"], jsii.get(self, "rdbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e74149603d62e6bd5ce3ade9f1033453096021cbc2238af0650c2de5d4ca57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleRedisClusterPersistenceConfig]:
        return typing.cast(typing.Optional[GoogleRedisClusterPersistenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterPersistenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e3070390855c7ac099ba11e56b85e5b811a690844300218f1d1c6a803b26fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPersistenceConfigRdbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "rdb_snapshot_period": "rdbSnapshotPeriod",
        "rdb_snapshot_start_time": "rdbSnapshotStartTime",
    },
)
class GoogleRedisClusterPersistenceConfigRdbConfig:
    def __init__(
        self,
        *,
        rdb_snapshot_period: typing.Optional[builtins.str] = None,
        rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rdb_snapshot_period: Optional. Available snapshot periods for scheduling. - ONE_HOUR: Snapshot every 1 hour. - SIX_HOURS: Snapshot every 6 hours. - TWELVE_HOURS: Snapshot every 12 hours. - TWENTY_FOUR_HOURS: Snapshot every 24 hours. Possible values: ["SNAPSHOT_PERIOD_UNSPECIFIED", "ONE_HOUR", "SIX_HOURS", "TWELVE_HOURS", "TWENTY_FOUR_HOURS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#rdb_snapshot_period GoogleRedisCluster#rdb_snapshot_period}
        :param rdb_snapshot_start_time: The time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#rdb_snapshot_start_time GoogleRedisCluster#rdb_snapshot_start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d69c4e4e3cfa2716ea16509d78ca28a5f869540992ad7faf721795a62142362)
            check_type(argname="argument rdb_snapshot_period", value=rdb_snapshot_period, expected_type=type_hints["rdb_snapshot_period"])
            check_type(argname="argument rdb_snapshot_start_time", value=rdb_snapshot_start_time, expected_type=type_hints["rdb_snapshot_start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rdb_snapshot_period is not None:
            self._values["rdb_snapshot_period"] = rdb_snapshot_period
        if rdb_snapshot_start_time is not None:
            self._values["rdb_snapshot_start_time"] = rdb_snapshot_start_time

    @builtins.property
    def rdb_snapshot_period(self) -> typing.Optional[builtins.str]:
        '''Optional. Available snapshot periods for scheduling.

        - ONE_HOUR:	Snapshot every 1 hour.
        - SIX_HOURS:	Snapshot every 6 hours.
        - TWELVE_HOURS:	Snapshot every 12 hours.
        - TWENTY_FOUR_HOURS:	Snapshot every 24 hours. Possible values: ["SNAPSHOT_PERIOD_UNSPECIFIED", "ONE_HOUR", "SIX_HOURS", "TWELVE_HOURS", "TWENTY_FOUR_HOURS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#rdb_snapshot_period GoogleRedisCluster#rdb_snapshot_period}
        '''
        result = self._values.get("rdb_snapshot_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_snapshot_start_time(self) -> typing.Optional[builtins.str]:
        '''The time that the first snapshot was/will be attempted, and to which future snapshots will be aligned.

        If not provided, the current time will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#rdb_snapshot_start_time GoogleRedisCluster#rdb_snapshot_start_time}
        '''
        result = self._values.get("rdb_snapshot_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterPersistenceConfigRdbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterPersistenceConfigRdbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPersistenceConfigRdbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fcb5606bf3171e83ac6da5549e0bd09a1771f51be6b1e56fed5355f43b6cb1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRdbSnapshotPeriod")
    def reset_rdb_snapshot_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbSnapshotPeriod", []))

    @jsii.member(jsii_name="resetRdbSnapshotStartTime")
    def reset_rdb_snapshot_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbSnapshotStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotPeriodInput")
    def rdb_snapshot_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rdbSnapshotPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotStartTimeInput")
    def rdb_snapshot_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rdbSnapshotStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotPeriod")
    def rdb_snapshot_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdbSnapshotPeriod"))

    @rdb_snapshot_period.setter
    def rdb_snapshot_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2442205b2a241146f21e8935261644945a8f2aea63ac5230fd95ff575a71afb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotStartTime")
    def rdb_snapshot_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdbSnapshotStartTime"))

    @rdb_snapshot_start_time.setter
    def rdb_snapshot_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b7ce33ee3a41d3214291baf0acf9c2c8042e6110020d2d058dc5d812c775e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterPersistenceConfigRdbConfig]:
        return typing.cast(typing.Optional[GoogleRedisClusterPersistenceConfigRdbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterPersistenceConfigRdbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660d5aaa0e560d97cfb81608bd3425e025f4085f9e8e09ee6f70e9f8206d7a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPscConfigs",
    jsii_struct_bases=[],
    name_mapping={"network": "network"},
)
class GoogleRedisClusterPscConfigs:
    def __init__(self, *, network: builtins.str) -> None:
        '''
        :param network: Required. The consumer network where the network address of the discovery endpoint will be reserved, in the form of projects/{network_project_id_or_number}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#network GoogleRedisCluster#network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0402bd927a8309f2a9e5635125604253cd81145f133bf5968082b99f85aed85)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network": network,
        }

    @builtins.property
    def network(self) -> builtins.str:
        '''Required. The consumer network where the network address of the discovery endpoint will be reserved, in the form of projects/{network_project_id_or_number}/global/networks/{network_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#network GoogleRedisCluster#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterPscConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterPscConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPscConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e2ccb5cc930f2b1799b1a7c33e176640d52ca30094086afbdf2b8e07deb980b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleRedisClusterPscConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6697574b211bfa517698c0fba73c48c2e641d6415b0475bbb7faa3007a77bdb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterPscConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ace13e1fb7cd1084a8a0c2d352ac90b6fbf8a6482f02bbd7d15a8e5910f1a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9272aa2591c2552c3c5123fb74a5dd8a074b63e16241a79dde0605a7b2b847f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af2d47859aae24060c697d9c7e0743281e90493ad5afb41a590a3e46aa38c4b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterPscConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterPscConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterPscConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6f41d2f372adea80fa6c86b7aa3ec9339e60a0755b17f8ccde4d020c521b79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterPscConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPscConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba04429a89f6fd1c259e95dc57fd7fb95e9b50f5de3149683ec696319845abab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635fd7d0d72f2a2aef683947c57b90b8a979d370f98490b2ab6e070aa3abad59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterPscConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterPscConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterPscConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd1b677f0d5961f44fb0f92c749e04cb30bcb0dfae0e51ae01e091b0cf2ed377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPscConnections",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleRedisClusterPscConnections:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterPscConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterPscConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPscConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90dbeb22d9c1d7de398a61ecccd9e443da014448a1e72593d28371a0328347fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleRedisClusterPscConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300370da3b3d74f73f0bdc0905b597e27b2f334d2d3b748da45165c829fd2f03)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterPscConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f48b7f3ce314131473e43f7bf8fffbf4c3657111331adc933066d57427effe9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b689b75b76a478dd6df53a052e17f647b7df0ad2a559a80ab68ef23177bf8166)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce86a11bd7f401e064108162e1aaebd91b29f92cbd842a52c7972c47cb1b6d47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterPscConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPscConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e71412847b6361b38f13ba12bd2cb0aaa4b9ce0966004232f0bd30c90b02fa23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="forwardingRule")
    def forwarding_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingRule"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionId")
    def psc_connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleRedisClusterPscConnections]:
        return typing.cast(typing.Optional[GoogleRedisClusterPscConnections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterPscConnections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4398f64a35f54aed2b77ff79562ffb2642d0f0d16def5d5069bdfb6f96d49c9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPscServiceAttachments",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleRedisClusterPscServiceAttachments:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterPscServiceAttachments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterPscServiceAttachmentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPscServiceAttachmentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb486cdb81eb7dd2c36ac6c2ea90127dde91705e561a8ceb8037697f35335ccb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleRedisClusterPscServiceAttachmentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac31ad1168512e3978c40f9e70175ae5343f55626f8d6eddc0ace5b26a7c89f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterPscServiceAttachmentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c288e7a2cf02b2900a0899b1bbd142104310dec19276143ae1af1bf051904e38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1371f4402a428ccb24edbd18dce17168ccb0f8aae0112c74d2de24a305f28a95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f4e05d661962f2dc4f922db66bcd43b3b0ba486f1f3b8f336d6801da6da7f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterPscServiceAttachmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterPscServiceAttachmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d462b0a8b31d01cf38e8a9a1c6ef1f4b37a23c3e708fd1ebd6c20404789104fa)
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
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterPscServiceAttachments]:
        return typing.cast(typing.Optional[GoogleRedisClusterPscServiceAttachments], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterPscServiceAttachments],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36e130db6f05312f3b980e80e7d5dd8115d63e1571d59c9d8eb82c1153c21a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterStateInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleRedisClusterStateInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterStateInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterStateInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterStateInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7702d7c4ab60a39ec038ae2f972663439ef514705eefc9220e60eb5bf7f8fa4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleRedisClusterStateInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10d1d41c3dc906fdf719d0797b99f21cab82646bccfcce44f0863a359c777fe0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterStateInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b38553457dac83c7f773c8a6e46ae000b137d87a889225a39569f161a559da7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28b8d2a208d1d6da1ca5456c7160d33db8fc81ee73043b2d1abba591388fd60f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73dc091817700c4d845724d8b09a1ff93f12ec57bbedc72ef1ba2a6a9e110423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterStateInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterStateInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__728b3423877b59c2ffb94c0ab7a91cc30aa9c8ad8f839b9d9a022fc01d7765e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="updateInfo")
    def update_info(self) -> "GoogleRedisClusterStateInfoUpdateInfoList":
        return typing.cast("GoogleRedisClusterStateInfoUpdateInfoList", jsii.get(self, "updateInfo"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleRedisClusterStateInfo]:
        return typing.cast(typing.Optional[GoogleRedisClusterStateInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterStateInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6165c10d3ced73c6e478d04b224115450a93defcded6f0d187d9160e72e87df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterStateInfoUpdateInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleRedisClusterStateInfoUpdateInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterStateInfoUpdateInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterStateInfoUpdateInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterStateInfoUpdateInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27365506daed076b3a34464c7524e68c0291960414e0982c8c605e7e5391890b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleRedisClusterStateInfoUpdateInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500ca134759bcbe1b0394b8c26c6772fdf3f1389ef1bf6c499ccd823fd13cf3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleRedisClusterStateInfoUpdateInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d520073dddbc1d09e1f2e73b0e96bd56976b4698447ea9cfc9450b7bfb33d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6701f505bdeed61abb35ad99038f6b04b078087339c49aa0c7d2d3e950c62a50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b58cd0c5958182c2469ce2fd64b1a88c5b356daebc9a70d3ebb809a83c34b8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleRedisClusterStateInfoUpdateInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterStateInfoUpdateInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88f195ab6c33824857d5e35a203e3800f83e638fbc7deed0e6bb600ef920b7ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="targetReplicaCount")
    def target_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetReplicaCount"))

    @builtins.property
    @jsii.member(jsii_name="targetShardCount")
    def target_shard_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetShardCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleRedisClusterStateInfoUpdateInfo]:
        return typing.cast(typing.Optional[GoogleRedisClusterStateInfoUpdateInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterStateInfoUpdateInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256f100ae316e0840e0505a51354adf0a4b447a4c3592ec07d49f1968037126f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleRedisClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#create GoogleRedisCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#delete GoogleRedisCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#update GoogleRedisCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1d5d647d2989e3bcba53d3fce3d683f4151f0bbae6967b00434dc2f291fa6a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#create GoogleRedisCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#delete GoogleRedisCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#update GoogleRedisCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6375653458e83c3553a9037a64c3b51d0b6b491290546bb66ff65d73481e31b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d940e111f99a08ba1c5b35a31de2222bb61b1a5e4c60e3464235edb6dcff7d9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b927a19d62b1ab0cf1f58a405952c2e5df8a7b43ac2b2fb69eb3906f69f72f3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37a28a60ca692ff0c89fbbef68b913e3aee97a06afd5802fd18cfce9a4376fa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f871d6e91498bff041d305011902853f58b2df6d4f0574b372cd5a6227fe341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterZoneDistributionConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "zone": "zone"},
)
class GoogleRedisClusterZoneDistributionConfig:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Immutable. The mode for zone distribution for Memorystore Redis cluster. If not provided, MULTI_ZONE will be used as default Possible values: ["MULTI_ZONE", "SINGLE_ZONE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#mode GoogleRedisCluster#mode}
        :param zone: Immutable. The zone for single zone Memorystore Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#zone GoogleRedisCluster#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c5aa90a668990f9fbfdffb16347bbd4d32a9654c3537c0311ee8e9bf3dbdb8)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Immutable.

        The mode for zone distribution for Memorystore Redis cluster.
        If not provided, MULTI_ZONE will be used as default Possible values: ["MULTI_ZONE", "SINGLE_ZONE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#mode GoogleRedisCluster#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Immutable. The zone for single zone Memorystore Redis cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_redis_cluster#zone GoogleRedisCluster#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleRedisClusterZoneDistributionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleRedisClusterZoneDistributionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleRedisCluster.GoogleRedisClusterZoneDistributionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35c76e98e076c307f10911363304dd963b9f3301fc08eeb07eb0fd81e295b34f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320425d08e6b7fc45b11a00085bc97511a9c267d8c43bc2cbd0d681374a0c5de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb44502e2f2b746b58a1b3a0ef321494775c17ce16a241872602cab41b3ec7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleRedisClusterZoneDistributionConfig]:
        return typing.cast(typing.Optional[GoogleRedisClusterZoneDistributionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleRedisClusterZoneDistributionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e095227c758e4cbb8248991a687136cb8f0f6dfbe3b36be295a2c0128408ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleRedisCluster",
    "GoogleRedisClusterAutomatedBackupConfig",
    "GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule",
    "GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleOutputReference",
    "GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime",
    "GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference",
    "GoogleRedisClusterAutomatedBackupConfigOutputReference",
    "GoogleRedisClusterConfig",
    "GoogleRedisClusterCrossClusterReplicationConfig",
    "GoogleRedisClusterCrossClusterReplicationConfigMembership",
    "GoogleRedisClusterCrossClusterReplicationConfigMembershipList",
    "GoogleRedisClusterCrossClusterReplicationConfigMembershipOutputReference",
    "GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster",
    "GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterList",
    "GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterOutputReference",
    "GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters",
    "GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersList",
    "GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersOutputReference",
    "GoogleRedisClusterCrossClusterReplicationConfigOutputReference",
    "GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster",
    "GoogleRedisClusterCrossClusterReplicationConfigPrimaryClusterOutputReference",
    "GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters",
    "GoogleRedisClusterCrossClusterReplicationConfigSecondaryClustersList",
    "GoogleRedisClusterCrossClusterReplicationConfigSecondaryClustersOutputReference",
    "GoogleRedisClusterDiscoveryEndpoints",
    "GoogleRedisClusterDiscoveryEndpointsList",
    "GoogleRedisClusterDiscoveryEndpointsOutputReference",
    "GoogleRedisClusterDiscoveryEndpointsPscConfig",
    "GoogleRedisClusterDiscoveryEndpointsPscConfigList",
    "GoogleRedisClusterDiscoveryEndpointsPscConfigOutputReference",
    "GoogleRedisClusterGcsSource",
    "GoogleRedisClusterGcsSourceOutputReference",
    "GoogleRedisClusterMaintenancePolicy",
    "GoogleRedisClusterMaintenancePolicyOutputReference",
    "GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow",
    "GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowList",
    "GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
    "GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    "GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
    "GoogleRedisClusterMaintenanceSchedule",
    "GoogleRedisClusterMaintenanceScheduleList",
    "GoogleRedisClusterMaintenanceScheduleOutputReference",
    "GoogleRedisClusterManagedBackupSource",
    "GoogleRedisClusterManagedBackupSourceOutputReference",
    "GoogleRedisClusterPersistenceConfig",
    "GoogleRedisClusterPersistenceConfigAofConfig",
    "GoogleRedisClusterPersistenceConfigAofConfigOutputReference",
    "GoogleRedisClusterPersistenceConfigOutputReference",
    "GoogleRedisClusterPersistenceConfigRdbConfig",
    "GoogleRedisClusterPersistenceConfigRdbConfigOutputReference",
    "GoogleRedisClusterPscConfigs",
    "GoogleRedisClusterPscConfigsList",
    "GoogleRedisClusterPscConfigsOutputReference",
    "GoogleRedisClusterPscConnections",
    "GoogleRedisClusterPscConnectionsList",
    "GoogleRedisClusterPscConnectionsOutputReference",
    "GoogleRedisClusterPscServiceAttachments",
    "GoogleRedisClusterPscServiceAttachmentsList",
    "GoogleRedisClusterPscServiceAttachmentsOutputReference",
    "GoogleRedisClusterStateInfo",
    "GoogleRedisClusterStateInfoList",
    "GoogleRedisClusterStateInfoOutputReference",
    "GoogleRedisClusterStateInfoUpdateInfo",
    "GoogleRedisClusterStateInfoUpdateInfoList",
    "GoogleRedisClusterStateInfoUpdateInfoOutputReference",
    "GoogleRedisClusterTimeouts",
    "GoogleRedisClusterTimeoutsOutputReference",
    "GoogleRedisClusterZoneDistributionConfig",
    "GoogleRedisClusterZoneDistributionConfigOutputReference",
]

publication.publish()

def _typecheckingstub__0d06e83408d389d126307dc5da5dbea0b25bbdb25268e1b893b952189257b550(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    shard_count: jsii.Number,
    authorization_mode: typing.Optional[builtins.str] = None,
    automated_backup_config: typing.Optional[typing.Union[GoogleRedisClusterAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_cluster_replication_config: typing.Optional[typing.Union[GoogleRedisClusterCrossClusterReplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs_source: typing.Optional[typing.Union[GoogleRedisClusterGcsSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    maintenance_policy: typing.Optional[typing.Union[GoogleRedisClusterMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_backup_source: typing.Optional[typing.Union[GoogleRedisClusterManagedBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[GoogleRedisClusterPersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleRedisClusterPscConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleRedisClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
    zone_distribution_config: typing.Optional[typing.Union[GoogleRedisClusterZoneDistributionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f218ec7276baa83de99063a03dad61a503544e9d7cb8d4555432fe63a98f2c8f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f3eb78a9105ce610c006bc97b1b10e13b728d2ea5b29d8e1ff7da49eba78e8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleRedisClusterPscConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8457248878bc9a27f5fa539da594429af7ead11b3c0ee1f18d74522aafb2eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45bb2663677e2dceeb9a382cec90ebddac50b8ef9b39981accfc56b15a029096(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbde1543e0c209061fbb0700c5355d558b617cab336c278d9d96c73c588cc638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eafb9b09128d05883d703d770dd92faa062dc76181d65a475133d784a4f34f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c8a785b5d2a737ba3fc953d7c71b7ed2908333c56b99824d897d0a0e7e034b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b521b3f6028d73a1ca5e884c1c0177af62c5fac9d32a93edba43e397b0f1aa05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a50115c1f952d192b490c63a5a25be31b2d8ae469fca81f48af70e2627629e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9913e9ece04a764e8d5a0fb26eb01efe7b3adec9c586e0c701522f3d5080284(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e89b4fefd552c9e14092f82ed324c59b965eb6355b5960aff782e0592054464(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4706de2b8d3bcd5826af64a03d25a590b3bc81dfdcf452bd411387d1d8d3a313(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e3a5d473330b6e841521a50e106f13a6c5282d65f96d7865529d5dedb9f092(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c8aa418230c5d3ffdba9bc58dace30d1cc5626569868aa6670af422e2cd5c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a048cc4bd602c6bd9c4e55d33993c7d4b9633e42831a1354cdf677350bfe6f6(
    *,
    fixed_frequency_schedule: typing.Union[GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule, typing.Dict[builtins.str, typing.Any]],
    retention: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e321155fd068d95d89c761a46aeb71e0c4d4644c2e564853899fbf2c4ea6259(
    *,
    start_time: typing.Union[GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd0b9679bf386eaf47aa754ae2a1c77f904e451b578d0aa848f9c493912fff7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81408c8cb39e2b02823da654d65c1215f2bfb4c3e3b34626a35eacb04f95e4f(
    value: typing.Optional[GoogleRedisClusterAutomatedBackupConfigFixedFrequencySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ff1b1a96b6917a9b17d00739fed64cbd0821f92da864f8d36c80a52bcd0f99(
    *,
    hours: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb9fb8c083f296bd1d8559965b6074ad7ac5d456cda173bafdb3d2b3a43e8e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9891f4d10f2580fe8737d0d0f3f75467e6fd771899339f71e0a85f22fd24aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731514626d407c0f7df5dbc73a0899e6c33be15a4c541f821c3d11bf4e01eea8(
    value: typing.Optional[GoogleRedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9baaeb5251ec3dd75913735f3bd13d0fa4c6f53c734fde331b968029ccc0739b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ae5c922835e5cf724875e9abae70abd91424363d136b2f8ac422db6b6ac4d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5708489f2aa0870fb85948228c4fb5498b3843c5e17a7062d76abe9c595a90a3(
    value: typing.Optional[GoogleRedisClusterAutomatedBackupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a769d4dae5c7f36c5de16433b8294ff6e1878e822b9a46feece879b0228dc8f2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    shard_count: jsii.Number,
    authorization_mode: typing.Optional[builtins.str] = None,
    automated_backup_config: typing.Optional[typing.Union[GoogleRedisClusterAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_cluster_replication_config: typing.Optional[typing.Union[GoogleRedisClusterCrossClusterReplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs_source: typing.Optional[typing.Union[GoogleRedisClusterGcsSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    maintenance_policy: typing.Optional[typing.Union[GoogleRedisClusterMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_backup_source: typing.Optional[typing.Union[GoogleRedisClusterManagedBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[GoogleRedisClusterPersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleRedisClusterPscConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleRedisClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
    zone_distribution_config: typing.Optional[typing.Union[GoogleRedisClusterZoneDistributionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a4562145e1724425bc64d28efab38701cfe13afa7e9018930ccf722f7ddc10(
    *,
    cluster_role: typing.Optional[builtins.str] = None,
    primary_cluster: typing.Optional[typing.Union[GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    secondary_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c18119b0a1f4ccb8ffb4c64cb2689ff19562b9442518f0f1d78cc94432d2947(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5746835521c9710d249988b7b1a97cffb8ab43c08281512ffdb2c649b4b334(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf625ecedefce53cf9dac2ae39190d16cd30725deeddb527e0302ac43c6562d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31b9fdd6e6b0d518670bc8b072645bf8f6e61a3fe47e4c6b9c3deb44fa65c74(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53e0072c6b98cbbfdef7cf6c290b5d6f09c60684b446a2324fc19c71e7c4034(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a460d586281ee4bac210bebcd084ffd2567aa3fe4eadf9b113792e80e9aeaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4902b92a3d63588e406c1b3dddd97949e6eb93152ccab9f63ca7bdf78ddc89(
    value: typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembership],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e0c4dfeb65b5fffa4b3bbde9247c776ca09b92b611f4156671a608595d2269(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3655d498131eba6324ca4ff2a2a4f1909217a23a0c8885643ed43e954d8785ec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e660209bd660e8dd6f94f0d56307c56c7001229ec6198de638ac9ea87dd91f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968f78ac9b2345c435d51ab693fb2c80c1306a6fe1cde015b42f7dda409973a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1970c6f676fe7d4bdb8330dc9f5edd4fb0cecc338fb95c4655737fe66cd97790(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a29e9274a2fc850438146c0679ad9682b593f6ffda0af1d98fc4e79f01d3566(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17285d7e863d8256e4b502df5cb69e26c6e469c6558acc949b20953177508820(
    value: typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b338b214e43c83d854e378cc8f438573ab903b38ff3b02d4fdd0aab5301dfd58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb8698edb7bfb3c19ca2457a62907fd6fb8d1100f221b2ff5569043a9f98128(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7561b57ee686057a69d988185e219ae0012a0b4c6031d0449774025d1d8bfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9eb9c9b34234595c6990d84e34389e6edf97cde662cdca833f14c29c6cab10(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd19c56e0e9877426b3a685e927a021f9d5b42a5825afe1eaaa01af7bfa224f3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c360c9c740eb7b6a0f04ae1c7a8040ef83265a9d895b517ec1fedcb0a66ca1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1664971886e14199da3d51624508492fd3f3fe950ebe5c6eaef76ef08ba2e9a6(
    value: typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772dee1f8db967ac6aa51fb7fcdb79d0e6ac77f61bc672d33249550454f81b4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2cb368a143a955e4019c6fae70a071c817e17bdbc1d1730f310feb5aeda1add(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fb736ad98a095b40cdfc2444a2cb0c48beb6c62605c8552372cfab3881b2bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e22336135f3dd35ed9ef25b075cee71d0312de3d3fa5eef6306a7490cd441b(
    value: typing.Optional[GoogleRedisClusterCrossClusterReplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97cbf58e0232caf916026a805afdb209d6aa8e03cd16a0e6ee5faf448e32f311(
    *,
    cluster: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa265bd682aaeab9b76b21003d562590fdedfefb70f2d09b3fc7c25964bc5bbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6ca44f878347e099e8a99e3342e597565d9ea1df8a8259356e0bbfddca3e82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f6ce32a42bff9b5a7b67f68f26182af16148baba2721cb4bfa4ed0fb1e5dfc(
    value: typing.Optional[GoogleRedisClusterCrossClusterReplicationConfigPrimaryCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8ebb5bccd29b1bb96b130518421f6d1979a80f4a6e2cf82829569d2ccc78b5(
    *,
    cluster: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648e8c54fac614c3aceb522540a53a1613a208aa34b7b7bd11988d1fff7f4012(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f28ca0968524be4f989d0204def7ada36e1e84cff91d1aded3a5e6f7904d2d6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c82c5633a0c64de4f8c0b498fe09a0392b42527ff3d7ad85aa55a4023f34c88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c586a41bbead36966152b382a20a8da84782f979dd6a41a572d106b23f963b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481ef4f760524409fc52f6341f5462a19f8453706b4cec824bf9f443117aa0b7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8221409ff905de8ada52155ad477f67f26e54876da0cbb610dd859ca96b8cf7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bb6f29ba4d5c4acf6e9d3c2a1a792eb837b58501ec76a4b85410a97c57da9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45870e063eb18228ff6b31e0cb9a84194aca5ae74b3574b5aaa23296b53a5fdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00c2bb85b8698584759c64a365a4c4aa5a0e46fc7d1727ee1649a8c688142f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterCrossClusterReplicationConfigSecondaryClusters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359e2089b1e5fbc815f14be1981d2cddd98d76ad2fb87179806d8ba73c35fcc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e57ba031bef1fae202adadbeb32f07227fd693af0ecf9d1e890b1cc532ad1f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1960688266eec07fb26a0aaf82ecfb5bd2eef5ed8bd6f95eb704efaca49440(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0b4273e730873afcbb5af556d3d99b0d09f88ffac0294893fd4e47fdd44161(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bcaecdaac443d7ef7b8ae5f8ac95b920686dd69f1ffec78343358e427891bf1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2124372e3e90746a66c1e2ea57a0a69bcc5c2c7fcccd05559e8181cf58b03004(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e1564ac180aad6adbde43511d6dcd876cdaecc1e0892b09707e33a408ba382(
    value: typing.Optional[GoogleRedisClusterDiscoveryEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9eb789dfd339950f565193f000276a3efcb351b97cd2d6d3da9a830cfd1341(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046e574789714c35860f777da363511063f80380e6edac5d9f305992ecab1a6d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1696f3d7d27eb636492c7f719459811105c139ca5e6e5c97a46f6b942ca354f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa1493f879fe87ab67f9df1879e77e2fce7a9495dca1e5ddbaef59bfc0411ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df02122959c73d88266360cc4f44881cbba35a086d257d0e892430d24ce4d39(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347c1d7f82af063caf2aa29ef65d4c9535dfdc76cb00535f51273b0885d69230(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeec9f307274baf0167c54dcca8c5d6baa068d59da3b91210191bd84f11eec8c(
    value: typing.Optional[GoogleRedisClusterDiscoveryEndpointsPscConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640fa3eb040bf3c7a315a01581c5b967ce13b15a21d22bd7e1014d5403e4063e(
    *,
    uris: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add5145c891087d27ceed6cfc32ffb05b2fb8b6f8c85fdc8039fff73feffe3b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026e5c7bbe3b81a778386e6016efeac08148693cbdfcfd38cf9360f80eb2b836(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8492d44b1e5726f153b16251172d19ccbf3dea8cdd46fecffe70e09e835fd574(
    value: typing.Optional[GoogleRedisClusterGcsSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075f3caf6b66a07c55f7497ccd05fe3f204fa2767b2fdbce075ff3453f5d312d(
    *,
    weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8e2d866fc3ae373e6c2436d9a365a0823eeff6ac07d08ec7f1689126eb6503(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a95a9d9dad1dc5a6b4a4df7f5e1e2286421f05a268e5357106384382f08fb7d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e783a8395df99d346a9bbd194ee227c6efc0ad6e1b0f48be347c9e6ef6b311(
    value: typing.Optional[GoogleRedisClusterMaintenancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9888a1a0660dd934a8554a8ccb96624b5cf55241156514650d473e8ca50290c1(
    *,
    day: builtins.str,
    start_time: typing.Union[GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8adb52f0faa28cd96b639cb2cce1e6c06a0eaf829ec40164f3c95080f6f1db13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc01eadec8cef67c5f479c8abcef1ee83139a92f1ce58b00451916b71ceda9fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2464c48c65b3b4e4210f6e2ea4cea500d7412b2fa58c2243472278ff0ee510b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3018171a60f26c8d7165e04d922331c076fc9acaea3f52830ab5fe024073604f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550b7503adf72c6c83a5148bbd630f7cae5568123f52380f87e3c13dc0df88c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0266a96ecd0f92e4251e4b0c4af70a6f8f2dfdcf52d7bc68d687564da0c63be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e1cdffafdf2897a1d5a812dcdeaf6862869250b2e3058d17117c0c924ddbff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9485b9a3a317cc8af402239e78369f0bfff3f492300dd71e3f42c50891b6c84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54b6e74391af924af08961623985075118513bbf1990bc03c39d0dc77626e5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindow]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbc3150680f45546a4144ca8b8c348741389d922ceb074a11412bc318e3ebdc(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e88548335c5ac56d2597252c544153d78976ec761de27ae4d8a9e805323a190(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b0b5b0e4508da56c0ab91e6f6acf755c6317805fb185eb0bf6b7bb5118f864(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e781848b8a3fd342ea5d4388183d42bcc7885ae5184fd29db7811a626210a323(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159632bb7a14192e78370c59c43f387c3e83b9984389f20ace0da2d8d8d8bb8a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1386ea7e673c070f23088c63aff935a15e60a185a7bf1e1fe4c13ca6949faeb5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84623036c7f84b95f00835c7fbd04dca22089d580182ea47a2f8865e5cdbf31(
    value: typing.Optional[GoogleRedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e83ddcf6c2a63e494b23d6eae39159675a25d93db5012c06462a17e81291d4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004560d6aba93ebea5126293eb4517ff103b0d8cfa5edb7d6e1e6c994326d7d4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79727fc259dc8db2c708f41d2cb931a101c2083e9be78a55d606be37c5143bd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae9320b724f3588a199a8b3317d487918472a4c4ea561a981cee138c39b307f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513e76ec522b00ad2a57c059ce10652f37ce0a6e3cf35a55d3b9b5211b7a6601(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf9d1c361d05a854293197e270448f27b7d64ba0a6ac50c6e2888a0ea4cf3d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7982f745237a5a9a7d97e2c7d74c7972708002ee5ecb98c8482d35f10164d6f4(
    value: typing.Optional[GoogleRedisClusterMaintenanceSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b5fe8cb12d5415d9570c0ad9d884b7f4cc85910284178cf4264b65bcedcc79(
    *,
    backup: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19208788f7d4ac944d851f8c659154764b198b122088e82a8b307a69576edaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55711fb11420df1b2715feaac60d52a2af0b6aca4143a32b6b416df642a07c70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61711dbdfa3b83fdfefeacc4265c4e1ea24f03717d57ae7b93d6f136aa27bc6a(
    value: typing.Optional[GoogleRedisClusterManagedBackupSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1101e46a05e463205a4df4ed6c756471dfca26fe8ccf11f98e53702cda9e5da(
    *,
    aof_config: typing.Optional[typing.Union[GoogleRedisClusterPersistenceConfigAofConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    rdb_config: typing.Optional[typing.Union[GoogleRedisClusterPersistenceConfigRdbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3266a6a21cb6d327dc4cdd2f87571b87a64542b6752e12809ee571e5d92e0bd(
    *,
    append_fsync: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0bc41637c95d3946e0d9a886b800468c74c8b36374b6a6b3f16985ef50d7f55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea99b663e90e18f7561b1a16c6340b7cb8651c733a6d7379ea95a64540987ca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9c10762c362e8e0334d34f82987016fb56edd10e5399bd7309ff498a4eee7b(
    value: typing.Optional[GoogleRedisClusterPersistenceConfigAofConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada6fa70ef5b6ab84db7311d73a4c7900b5994033727f2de680010b0b27db5cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e74149603d62e6bd5ce3ade9f1033453096021cbc2238af0650c2de5d4ca57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e3070390855c7ac099ba11e56b85e5b811a690844300218f1d1c6a803b26fb(
    value: typing.Optional[GoogleRedisClusterPersistenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d69c4e4e3cfa2716ea16509d78ca28a5f869540992ad7faf721795a62142362(
    *,
    rdb_snapshot_period: typing.Optional[builtins.str] = None,
    rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fcb5606bf3171e83ac6da5549e0bd09a1771f51be6b1e56fed5355f43b6cb1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2442205b2a241146f21e8935261644945a8f2aea63ac5230fd95ff575a71afb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b7ce33ee3a41d3214291baf0acf9c2c8042e6110020d2d058dc5d812c775e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660d5aaa0e560d97cfb81608bd3425e025f4085f9e8e09ee6f70e9f8206d7a73(
    value: typing.Optional[GoogleRedisClusterPersistenceConfigRdbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0402bd927a8309f2a9e5635125604253cd81145f133bf5968082b99f85aed85(
    *,
    network: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2ccb5cc930f2b1799b1a7c33e176640d52ca30094086afbdf2b8e07deb980b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6697574b211bfa517698c0fba73c48c2e641d6415b0475bbb7faa3007a77bdb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ace13e1fb7cd1084a8a0c2d352ac90b6fbf8a6482f02bbd7d15a8e5910f1a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9272aa2591c2552c3c5123fb74a5dd8a074b63e16241a79dde0605a7b2b847f7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2d47859aae24060c697d9c7e0743281e90493ad5afb41a590a3e46aa38c4b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6f41d2f372adea80fa6c86b7aa3ec9339e60a0755b17f8ccde4d020c521b79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleRedisClusterPscConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba04429a89f6fd1c259e95dc57fd7fb95e9b50f5de3149683ec696319845abab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635fd7d0d72f2a2aef683947c57b90b8a979d370f98490b2ab6e070aa3abad59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1b677f0d5961f44fb0f92c749e04cb30bcb0dfae0e51ae01e091b0cf2ed377(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterPscConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90dbeb22d9c1d7de398a61ecccd9e443da014448a1e72593d28371a0328347fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300370da3b3d74f73f0bdc0905b597e27b2f334d2d3b748da45165c829fd2f03(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f48b7f3ce314131473e43f7bf8fffbf4c3657111331adc933066d57427effe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b689b75b76a478dd6df53a052e17f647b7df0ad2a559a80ab68ef23177bf8166(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce86a11bd7f401e064108162e1aaebd91b29f92cbd842a52c7972c47cb1b6d47(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71412847b6361b38f13ba12bd2cb0aaa4b9ce0966004232f0bd30c90b02fa23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4398f64a35f54aed2b77ff79562ffb2642d0f0d16def5d5069bdfb6f96d49c9e(
    value: typing.Optional[GoogleRedisClusterPscConnections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb486cdb81eb7dd2c36ac6c2ea90127dde91705e561a8ceb8037697f35335ccb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac31ad1168512e3978c40f9e70175ae5343f55626f8d6eddc0ace5b26a7c89f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c288e7a2cf02b2900a0899b1bbd142104310dec19276143ae1af1bf051904e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1371f4402a428ccb24edbd18dce17168ccb0f8aae0112c74d2de24a305f28a95(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4e05d661962f2dc4f922db66bcd43b3b0ba486f1f3b8f336d6801da6da7f3a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d462b0a8b31d01cf38e8a9a1c6ef1f4b37a23c3e708fd1ebd6c20404789104fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e130db6f05312f3b980e80e7d5dd8115d63e1571d59c9d8eb82c1153c21a18(
    value: typing.Optional[GoogleRedisClusterPscServiceAttachments],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7702d7c4ab60a39ec038ae2f972663439ef514705eefc9220e60eb5bf7f8fa4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d1d41c3dc906fdf719d0797b99f21cab82646bccfcce44f0863a359c777fe0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b38553457dac83c7f773c8a6e46ae000b137d87a889225a39569f161a559da7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b8d2a208d1d6da1ca5456c7160d33db8fc81ee73043b2d1abba591388fd60f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73dc091817700c4d845724d8b09a1ff93f12ec57bbedc72ef1ba2a6a9e110423(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728b3423877b59c2ffb94c0ab7a91cc30aa9c8ad8f839b9d9a022fc01d7765e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6165c10d3ced73c6e478d04b224115450a93defcded6f0d187d9160e72e87df0(
    value: typing.Optional[GoogleRedisClusterStateInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27365506daed076b3a34464c7524e68c0291960414e0982c8c605e7e5391890b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500ca134759bcbe1b0394b8c26c6772fdf3f1389ef1bf6c499ccd823fd13cf3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d520073dddbc1d09e1f2e73b0e96bd56976b4698447ea9cfc9450b7bfb33d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6701f505bdeed61abb35ad99038f6b04b078087339c49aa0c7d2d3e950c62a50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b58cd0c5958182c2469ce2fd64b1a88c5b356daebc9a70d3ebb809a83c34b8d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f195ab6c33824857d5e35a203e3800f83e638fbc7deed0e6bb600ef920b7ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256f100ae316e0840e0505a51354adf0a4b447a4c3592ec07d49f1968037126f(
    value: typing.Optional[GoogleRedisClusterStateInfoUpdateInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1d5d647d2989e3bcba53d3fce3d683f4151f0bbae6967b00434dc2f291fa6a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6375653458e83c3553a9037a64c3b51d0b6b491290546bb66ff65d73481e31b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d940e111f99a08ba1c5b35a31de2222bb61b1a5e4c60e3464235edb6dcff7d9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b927a19d62b1ab0cf1f58a405952c2e5df8a7b43ac2b2fb69eb3906f69f72f3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a28a60ca692ff0c89fbbef68b913e3aee97a06afd5802fd18cfce9a4376fa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f871d6e91498bff041d305011902853f58b2df6d4f0574b372cd5a6227fe341(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleRedisClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c5aa90a668990f9fbfdffb16347bbd4d32a9654c3537c0311ee8e9bf3dbdb8(
    *,
    mode: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c76e98e076c307f10911363304dd963b9f3301fc08eeb07eb0fd81e295b34f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320425d08e6b7fc45b11a00085bc97511a9c267d8c43bc2cbd0d681374a0c5de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb44502e2f2b746b58a1b3a0ef321494775c17ce16a241872602cab41b3ec7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e095227c758e4cbb8248991a687136cb8f0f6dfbe3b36be295a2c0128408ea(
    value: typing.Optional[GoogleRedisClusterZoneDistributionConfig],
) -> None:
    """Type checking stubs"""
    pass
