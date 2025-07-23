r'''
# `google_redis_cluster`

Refer to the Terraform Registry for docs: [`google_redis_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster).
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


class RedisCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster google_redis_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        shard_count: jsii.Number,
        authorization_mode: typing.Optional[builtins.str] = None,
        automated_backup_config: typing.Optional[typing.Union["RedisClusterAutomatedBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cross_cluster_replication_config: typing.Optional[typing.Union["RedisClusterCrossClusterReplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs_source: typing.Optional[typing.Union["RedisClusterGcsSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        maintenance_policy: typing.Optional[typing.Union["RedisClusterMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_backup_source: typing.Optional[typing.Union["RedisClusterManagedBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["RedisClusterPersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterPscConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["RedisClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        zone_distribution_config: typing.Optional[typing.Union["RedisClusterZoneDistributionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster google_redis_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param shard_count: Required. Number of shards for the Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#shard_count RedisCluster#shard_count}
        :param authorization_mode: Optional. The authorization mode of the Redis cluster. If not provided, auth feature is disabled for the cluster. Default value: "AUTH_MODE_DISABLED" Possible values: ["AUTH_MODE_UNSPECIFIED", "AUTH_MODE_IAM_AUTH", "AUTH_MODE_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#authorization_mode RedisCluster#authorization_mode}
        :param automated_backup_config: automated_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#automated_backup_config RedisCluster#automated_backup_config}
        :param cross_cluster_replication_config: cross_cluster_replication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#cross_cluster_replication_config RedisCluster#cross_cluster_replication_config}
        :param deletion_protection_enabled: Optional. Indicates if the cluster is deletion protected or not. If the value if set to true, any delete cluster operation will fail. Default value is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#deletion_protection_enabled RedisCluster#deletion_protection_enabled}
        :param gcs_source: gcs_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#gcs_source RedisCluster#gcs_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#id RedisCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key: The KMS key used to encrypt the at-rest data of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#kms_key RedisCluster#kms_key}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#maintenance_policy RedisCluster#maintenance_policy}
        :param managed_backup_source: managed_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#managed_backup_source RedisCluster#managed_backup_source}
        :param name: Unique name of the resource in this scope including project and location using the form: projects/{projectId}/locations/{locationId}/clusters/{clusterId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#name RedisCluster#name}
        :param node_type: The nodeType for the Redis cluster. If not provided, REDIS_HIGHMEM_MEDIUM will be used as default Possible values: ["REDIS_SHARED_CORE_NANO", "REDIS_HIGHMEM_MEDIUM", "REDIS_HIGHMEM_XLARGE", "REDIS_STANDARD_SMALL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#node_type RedisCluster#node_type}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#persistence_config RedisCluster#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#project RedisCluster#project}.
        :param psc_configs: psc_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#psc_configs RedisCluster#psc_configs}
        :param redis_configs: Configure Redis Cluster behavior using a subset of native Redis configuration parameters. Please check Memorystore documentation for the list of supported parameters: https://cloud.google.com/memorystore/docs/cluster/supported-instance-configurations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#redis_configs RedisCluster#redis_configs}
        :param region: The name of the region of the Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#region RedisCluster#region}
        :param replica_count: Optional. The number of replica nodes per shard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#replica_count RedisCluster#replica_count}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#timeouts RedisCluster#timeouts}
        :param transit_encryption_mode: Optional. The in-transit encryption for the Redis cluster. If not provided, encryption is disabled for the cluster. Default value: "TRANSIT_ENCRYPTION_MODE_DISABLED" Possible values: ["TRANSIT_ENCRYPTION_MODE_UNSPECIFIED", "TRANSIT_ENCRYPTION_MODE_DISABLED", "TRANSIT_ENCRYPTION_MODE_SERVER_AUTHENTICATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#transit_encryption_mode RedisCluster#transit_encryption_mode}
        :param zone_distribution_config: zone_distribution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#zone_distribution_config RedisCluster#zone_distribution_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1279b263e30e89b4adb662713bc653e88c407a80eac215ff514d1a7fb576e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RedisClusterConfig(
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
        '''Generates CDKTF code for importing a RedisCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RedisCluster to import.
        :param import_from_id: The id of the existing RedisCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RedisCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96dc43aef9a7a9b7e72df44214a098cbbcdf1b0ff1d39d211f72c56ca83d2b00)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutomatedBackupConfig")
    def put_automated_backup_config(
        self,
        *,
        fixed_frequency_schedule: typing.Union["RedisClusterAutomatedBackupConfigFixedFrequencySchedule", typing.Dict[builtins.str, typing.Any]],
        retention: builtins.str,
    ) -> None:
        '''
        :param fixed_frequency_schedule: fixed_frequency_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#fixed_frequency_schedule RedisCluster#fixed_frequency_schedule}
        :param retention: How long to keep automated backups before the backups are deleted. The value should be between 1 day and 365 days. If not specified, the default value is 35 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#retention RedisCluster#retention}
        '''
        value = RedisClusterAutomatedBackupConfig(
            fixed_frequency_schedule=fixed_frequency_schedule, retention=retention
        )

        return typing.cast(None, jsii.invoke(self, "putAutomatedBackupConfig", [value]))

    @jsii.member(jsii_name="putCrossClusterReplicationConfig")
    def put_cross_cluster_replication_config(
        self,
        *,
        cluster_role: typing.Optional[builtins.str] = None,
        primary_cluster: typing.Optional[typing.Union["RedisClusterCrossClusterReplicationConfigPrimaryCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterCrossClusterReplicationConfigSecondaryClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cluster_role: The role of the cluster in cross cluster replication. Supported values are:. 1. 'CLUSTER_ROLE_UNSPECIFIED': This is an independent cluster that has never participated in cross cluster replication. It allows both reads and writes. 1. 'NONE': This is an independent cluster that previously participated in cross cluster replication(either as a 'PRIMARY' or 'SECONDARY' cluster). It allows both reads and writes. 1. 'PRIMARY': This cluster serves as the replication source for secondary clusters that are replicating from it. Any data written to it is automatically replicated to its secondary clusters. It allows both reads and writes. 1. 'SECONDARY': This cluster replicates data from the primary cluster. It allows only reads. Possible values: ["CLUSTER_ROLE_UNSPECIFIED", "NONE", "PRIMARY", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#cluster_role RedisCluster#cluster_role}
        :param primary_cluster: primary_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#primary_cluster RedisCluster#primary_cluster}
        :param secondary_clusters: secondary_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#secondary_clusters RedisCluster#secondary_clusters}
        '''
        value = RedisClusterCrossClusterReplicationConfig(
            cluster_role=cluster_role,
            primary_cluster=primary_cluster,
            secondary_clusters=secondary_clusters,
        )

        return typing.cast(None, jsii.invoke(self, "putCrossClusterReplicationConfig", [value]))

    @jsii.member(jsii_name="putGcsSource")
    def put_gcs_source(self, *, uris: typing.Sequence[builtins.str]) -> None:
        '''
        :param uris: URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#uris RedisCluster#uris}
        '''
        value = RedisClusterGcsSource(uris=uris)

        return typing.cast(None, jsii.invoke(self, "putGcsSource", [value]))

    @jsii.member(jsii_name="putMaintenancePolicy")
    def put_maintenance_policy(
        self,
        *,
        weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#weekly_maintenance_window RedisCluster#weekly_maintenance_window}
        '''
        value = RedisClusterMaintenancePolicy(
            weekly_maintenance_window=weekly_maintenance_window
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenancePolicy", [value]))

    @jsii.member(jsii_name="putManagedBackupSource")
    def put_managed_backup_source(self, *, backup: builtins.str) -> None:
        '''
        :param backup: Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#backup RedisCluster#backup}
        '''
        value = RedisClusterManagedBackupSource(backup=backup)

        return typing.cast(None, jsii.invoke(self, "putManagedBackupSource", [value]))

    @jsii.member(jsii_name="putPersistenceConfig")
    def put_persistence_config(
        self,
        *,
        aof_config: typing.Optional[typing.Union["RedisClusterPersistenceConfigAofConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        rdb_config: typing.Optional[typing.Union["RedisClusterPersistenceConfigRdbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aof_config: aof_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#aof_config RedisCluster#aof_config}
        :param mode: Optional. Controls whether Persistence features are enabled. If not provided, the existing value will be used. - DISABLED: Persistence (both backup and restore) is disabled for the cluster. - RDB: RDB based Persistence is enabled. - AOF: AOF based Persistence is enabled. Possible values: ["PERSISTENCE_MODE_UNSPECIFIED", "DISABLED", "RDB", "AOF"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#mode RedisCluster#mode}
        :param rdb_config: rdb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#rdb_config RedisCluster#rdb_config}
        '''
        value = RedisClusterPersistenceConfig(
            aof_config=aof_config, mode=mode, rdb_config=rdb_config
        )

        return typing.cast(None, jsii.invoke(self, "putPersistenceConfig", [value]))

    @jsii.member(jsii_name="putPscConfigs")
    def put_psc_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterPscConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73056aee06e39178c1d7923cfb999b17d58284857f252bcd2fb4277cb2108380)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#create RedisCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#delete RedisCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#update RedisCluster#update}.
        '''
        value = RedisClusterTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putZoneDistributionConfig")
    def put_zone_distribution_config(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Immutable. The mode for zone distribution for Memorystore Redis cluster. If not provided, MULTI_ZONE will be used as default Possible values: ["MULTI_ZONE", "SINGLE_ZONE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#mode RedisCluster#mode}
        :param zone: Immutable. The zone for single zone Memorystore Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#zone RedisCluster#zone}
        '''
        value = RedisClusterZoneDistributionConfig(mode=mode, zone=zone)

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
    ) -> "RedisClusterAutomatedBackupConfigOutputReference":
        return typing.cast("RedisClusterAutomatedBackupConfigOutputReference", jsii.get(self, "automatedBackupConfig"))

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
    ) -> "RedisClusterCrossClusterReplicationConfigOutputReference":
        return typing.cast("RedisClusterCrossClusterReplicationConfigOutputReference", jsii.get(self, "crossClusterReplicationConfig"))

    @builtins.property
    @jsii.member(jsii_name="discoveryEndpoints")
    def discovery_endpoints(self) -> "RedisClusterDiscoveryEndpointsList":
        return typing.cast("RedisClusterDiscoveryEndpointsList", jsii.get(self, "discoveryEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="gcsSource")
    def gcs_source(self) -> "RedisClusterGcsSourceOutputReference":
        return typing.cast("RedisClusterGcsSourceOutputReference", jsii.get(self, "gcsSource"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicy")
    def maintenance_policy(self) -> "RedisClusterMaintenancePolicyOutputReference":
        return typing.cast("RedisClusterMaintenancePolicyOutputReference", jsii.get(self, "maintenancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceSchedule")
    def maintenance_schedule(self) -> "RedisClusterMaintenanceScheduleList":
        return typing.cast("RedisClusterMaintenanceScheduleList", jsii.get(self, "maintenanceSchedule"))

    @builtins.property
    @jsii.member(jsii_name="managedBackupSource")
    def managed_backup_source(self) -> "RedisClusterManagedBackupSourceOutputReference":
        return typing.cast("RedisClusterManagedBackupSourceOutputReference", jsii.get(self, "managedBackupSource"))

    @builtins.property
    @jsii.member(jsii_name="managedServerCa")
    def managed_server_ca(self) -> "RedisClusterManagedServerCaList":
        return typing.cast("RedisClusterManagedServerCaList", jsii.get(self, "managedServerCa"))

    @builtins.property
    @jsii.member(jsii_name="persistenceConfig")
    def persistence_config(self) -> "RedisClusterPersistenceConfigOutputReference":
        return typing.cast("RedisClusterPersistenceConfigOutputReference", jsii.get(self, "persistenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="preciseSizeGb")
    def precise_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "preciseSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="pscConfigs")
    def psc_configs(self) -> "RedisClusterPscConfigsList":
        return typing.cast("RedisClusterPscConfigsList", jsii.get(self, "pscConfigs"))

    @builtins.property
    @jsii.member(jsii_name="pscConnections")
    def psc_connections(self) -> "RedisClusterPscConnectionsList":
        return typing.cast("RedisClusterPscConnectionsList", jsii.get(self, "pscConnections"))

    @builtins.property
    @jsii.member(jsii_name="pscServiceAttachments")
    def psc_service_attachments(self) -> "RedisClusterPscServiceAttachmentsList":
        return typing.cast("RedisClusterPscServiceAttachmentsList", jsii.get(self, "pscServiceAttachments"))

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
    def state_info(self) -> "RedisClusterStateInfoList":
        return typing.cast("RedisClusterStateInfoList", jsii.get(self, "stateInfo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RedisClusterTimeoutsOutputReference":
        return typing.cast("RedisClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="zoneDistributionConfig")
    def zone_distribution_config(
        self,
    ) -> "RedisClusterZoneDistributionConfigOutputReference":
        return typing.cast("RedisClusterZoneDistributionConfigOutputReference", jsii.get(self, "zoneDistributionConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizationModeInput")
    def authorization_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="automatedBackupConfigInput")
    def automated_backup_config_input(
        self,
    ) -> typing.Optional["RedisClusterAutomatedBackupConfig"]:
        return typing.cast(typing.Optional["RedisClusterAutomatedBackupConfig"], jsii.get(self, "automatedBackupConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="crossClusterReplicationConfigInput")
    def cross_cluster_replication_config_input(
        self,
    ) -> typing.Optional["RedisClusterCrossClusterReplicationConfig"]:
        return typing.cast(typing.Optional["RedisClusterCrossClusterReplicationConfig"], jsii.get(self, "crossClusterReplicationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionEnabledInput")
    def deletion_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsSourceInput")
    def gcs_source_input(self) -> typing.Optional["RedisClusterGcsSource"]:
        return typing.cast(typing.Optional["RedisClusterGcsSource"], jsii.get(self, "gcsSourceInput"))

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
    ) -> typing.Optional["RedisClusterMaintenancePolicy"]:
        return typing.cast(typing.Optional["RedisClusterMaintenancePolicy"], jsii.get(self, "maintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="managedBackupSourceInput")
    def managed_backup_source_input(
        self,
    ) -> typing.Optional["RedisClusterManagedBackupSource"]:
        return typing.cast(typing.Optional["RedisClusterManagedBackupSource"], jsii.get(self, "managedBackupSourceInput"))

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
    ) -> typing.Optional["RedisClusterPersistenceConfig"]:
        return typing.cast(typing.Optional["RedisClusterPersistenceConfig"], jsii.get(self, "persistenceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pscConfigsInput")
    def psc_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterPscConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterPscConfigs"]]], jsii.get(self, "pscConfigsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RedisClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RedisClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionModeInput")
    def transit_encryption_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitEncryptionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneDistributionConfigInput")
    def zone_distribution_config_input(
        self,
    ) -> typing.Optional["RedisClusterZoneDistributionConfig"]:
        return typing.cast(typing.Optional["RedisClusterZoneDistributionConfig"], jsii.get(self, "zoneDistributionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationMode")
    def authorization_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationMode"))

    @authorization_mode.setter
    def authorization_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaac2f220b51f3f67b518419f8bbeddeef593ec6a8c5840a62c83ed528f18118)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b1ead5d805653aac0616483ade5eb3a8c4c34372fba592d688ba1ba8dde04e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce1013726b5f7e3ea08061fac21aa588fc248ada25589ff0fe46662fbc72139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35acdae521951c5e0f1458d8c4e39f73586020e35f34653b590ae5125cb22595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb291622a5350d8f06500fa5978273e7a6bb63c8a573a003d01aa6384018e2f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8771f3439d7db57341cb41d446eaa4294a4004f40c1350e2fa8b193889fa7048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f333d4f43b3b2933fc10c93d049529a410ed4b012a84fda09c0e7a596ccda16a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redisConfigs")
    def redis_configs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "redisConfigs"))

    @redis_configs.setter
    def redis_configs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3db4050d42d9e3a67fd9b5bec731aca251148cacd7870e21b2af68b95643bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisConfigs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b53dead1ccc2a65d93bf7bebcd349f895dbd10323017e9808c883c21f7b807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCount"))

    @replica_count.setter
    def replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae7679a6bfa55296546cdddb0f8b844167a7771c36342703546a9c14303ac64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shardCount")
    def shard_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shardCount"))

    @shard_count.setter
    def shard_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e268e2b984765e277bedd6d984d6dc5f99ee41ce0032d89f1613b0d86e0cb98e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shardCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionMode")
    def transit_encryption_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitEncryptionMode"))

    @transit_encryption_mode.setter
    def transit_encryption_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04317156b5d255b686379895ad5dc76666aa40e949de04c3451a3b35674e04af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitEncryptionMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterAutomatedBackupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "fixed_frequency_schedule": "fixedFrequencySchedule",
        "retention": "retention",
    },
)
class RedisClusterAutomatedBackupConfig:
    def __init__(
        self,
        *,
        fixed_frequency_schedule: typing.Union["RedisClusterAutomatedBackupConfigFixedFrequencySchedule", typing.Dict[builtins.str, typing.Any]],
        retention: builtins.str,
    ) -> None:
        '''
        :param fixed_frequency_schedule: fixed_frequency_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#fixed_frequency_schedule RedisCluster#fixed_frequency_schedule}
        :param retention: How long to keep automated backups before the backups are deleted. The value should be between 1 day and 365 days. If not specified, the default value is 35 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#retention RedisCluster#retention}
        '''
        if isinstance(fixed_frequency_schedule, dict):
            fixed_frequency_schedule = RedisClusterAutomatedBackupConfigFixedFrequencySchedule(**fixed_frequency_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97fef90420a3848f0114ba3ce0642dc670eadfdaf9a43e1ced4fcc79c30f57b)
            check_type(argname="argument fixed_frequency_schedule", value=fixed_frequency_schedule, expected_type=type_hints["fixed_frequency_schedule"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fixed_frequency_schedule": fixed_frequency_schedule,
            "retention": retention,
        }

    @builtins.property
    def fixed_frequency_schedule(
        self,
    ) -> "RedisClusterAutomatedBackupConfigFixedFrequencySchedule":
        '''fixed_frequency_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#fixed_frequency_schedule RedisCluster#fixed_frequency_schedule}
        '''
        result = self._values.get("fixed_frequency_schedule")
        assert result is not None, "Required property 'fixed_frequency_schedule' is missing"
        return typing.cast("RedisClusterAutomatedBackupConfigFixedFrequencySchedule", result)

    @builtins.property
    def retention(self) -> builtins.str:
        '''How long to keep automated backups before the backups are deleted.

        The value should be between 1 day and 365 days. If not specified, the default value is 35 days.
        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#retention RedisCluster#retention}
        '''
        result = self._values.get("retention")
        assert result is not None, "Required property 'retention' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterAutomatedBackupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterAutomatedBackupConfigFixedFrequencySchedule",
    jsii_struct_bases=[],
    name_mapping={"start_time": "startTime"},
)
class RedisClusterAutomatedBackupConfigFixedFrequencySchedule:
    def __init__(
        self,
        *,
        start_time: typing.Union["RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#start_time RedisCluster#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a8e0b4defcbb6d2cd94fbc43de8c3d5351e843b23d735d6d303f246bf1cbd8)
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_time": start_time,
        }

    @builtins.property
    def start_time(
        self,
    ) -> "RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#start_time RedisCluster#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterAutomatedBackupConfigFixedFrequencySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterAutomatedBackupConfigFixedFrequencyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterAutomatedBackupConfigFixedFrequencyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b5ee03ae806add08fa48a0484e379f6b683ef65cbf6e81a6e5ee05b4f687c34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(self, *, hours: jsii.Number) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#hours RedisCluster#hours}
        '''
        value = RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime(
            hours=hours
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference":
        return typing.cast("RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime"]:
        return typing.cast(typing.Optional["RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RedisClusterAutomatedBackupConfigFixedFrequencySchedule]:
        return typing.cast(typing.Optional[RedisClusterAutomatedBackupConfigFixedFrequencySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterAutomatedBackupConfigFixedFrequencySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0b9f5dd0bd3f5a3c7094037f10b47f2aee9114e9eb16579241d5da195da582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime",
    jsii_struct_bases=[],
    name_mapping={"hours": "hours"},
)
class RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime:
    def __init__(self, *, hours: jsii.Number) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#hours RedisCluster#hours}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e879ce83171dd84fc0310ee5acb026397c22c1adb73f4c99933048bc632b56)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hours": hours,
        }

    @builtins.property
    def hours(self) -> jsii.Number:
        '''Hours of a day in 24 hour format.

        Must be greater than or equal to 0 and typically must be less than or equal to 23.
        An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#hours RedisCluster#hours}
        '''
        result = self._values.get("hours")
        assert result is not None, "Required property 'hours' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a83efb656fa9cfb75db30d3b64d5b1a3cf75591e1c1b61338e66644588ebd0f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c162a6023ac9af8cb061f14673fec73153ff8733a4b0e2253e48d550158c233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime]:
        return typing.cast(typing.Optional[RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a298781769e022c559ce570e8f47f690d62bae87a08ffcb67b71da53aea2396e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisClusterAutomatedBackupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterAutomatedBackupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__951cd0393cc0bd48648e44ae5fa0070d05a60419609664402faa0d94722ca37a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFixedFrequencySchedule")
    def put_fixed_frequency_schedule(
        self,
        *,
        start_time: typing.Union[RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#start_time RedisCluster#start_time}
        '''
        value = RedisClusterAutomatedBackupConfigFixedFrequencySchedule(
            start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putFixedFrequencySchedule", [value]))

    @builtins.property
    @jsii.member(jsii_name="fixedFrequencySchedule")
    def fixed_frequency_schedule(
        self,
    ) -> RedisClusterAutomatedBackupConfigFixedFrequencyScheduleOutputReference:
        return typing.cast(RedisClusterAutomatedBackupConfigFixedFrequencyScheduleOutputReference, jsii.get(self, "fixedFrequencySchedule"))

    @builtins.property
    @jsii.member(jsii_name="fixedFrequencyScheduleInput")
    def fixed_frequency_schedule_input(
        self,
    ) -> typing.Optional[RedisClusterAutomatedBackupConfigFixedFrequencySchedule]:
        return typing.cast(typing.Optional[RedisClusterAutomatedBackupConfigFixedFrequencySchedule], jsii.get(self, "fixedFrequencyScheduleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__dab3759a43805f91f2dd8c2ceaaaedd99c823c62076dc23667d317fd2aeb62d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterAutomatedBackupConfig]:
        return typing.cast(typing.Optional[RedisClusterAutomatedBackupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterAutomatedBackupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75553589284069415d5e2fd1f4f4955dd4bc30aef738616c10de7489fe325a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterConfig",
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
class RedisClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        automated_backup_config: typing.Optional[typing.Union[RedisClusterAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        cross_cluster_replication_config: typing.Optional[typing.Union["RedisClusterCrossClusterReplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs_source: typing.Optional[typing.Union["RedisClusterGcsSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        maintenance_policy: typing.Optional[typing.Union["RedisClusterMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_backup_source: typing.Optional[typing.Union["RedisClusterManagedBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["RedisClusterPersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterPscConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["RedisClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        zone_distribution_config: typing.Optional[typing.Union["RedisClusterZoneDistributionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param shard_count: Required. Number of shards for the Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#shard_count RedisCluster#shard_count}
        :param authorization_mode: Optional. The authorization mode of the Redis cluster. If not provided, auth feature is disabled for the cluster. Default value: "AUTH_MODE_DISABLED" Possible values: ["AUTH_MODE_UNSPECIFIED", "AUTH_MODE_IAM_AUTH", "AUTH_MODE_DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#authorization_mode RedisCluster#authorization_mode}
        :param automated_backup_config: automated_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#automated_backup_config RedisCluster#automated_backup_config}
        :param cross_cluster_replication_config: cross_cluster_replication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#cross_cluster_replication_config RedisCluster#cross_cluster_replication_config}
        :param deletion_protection_enabled: Optional. Indicates if the cluster is deletion protected or not. If the value if set to true, any delete cluster operation will fail. Default value is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#deletion_protection_enabled RedisCluster#deletion_protection_enabled}
        :param gcs_source: gcs_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#gcs_source RedisCluster#gcs_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#id RedisCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key: The KMS key used to encrypt the at-rest data of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#kms_key RedisCluster#kms_key}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#maintenance_policy RedisCluster#maintenance_policy}
        :param managed_backup_source: managed_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#managed_backup_source RedisCluster#managed_backup_source}
        :param name: Unique name of the resource in this scope including project and location using the form: projects/{projectId}/locations/{locationId}/clusters/{clusterId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#name RedisCluster#name}
        :param node_type: The nodeType for the Redis cluster. If not provided, REDIS_HIGHMEM_MEDIUM will be used as default Possible values: ["REDIS_SHARED_CORE_NANO", "REDIS_HIGHMEM_MEDIUM", "REDIS_HIGHMEM_XLARGE", "REDIS_STANDARD_SMALL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#node_type RedisCluster#node_type}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#persistence_config RedisCluster#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#project RedisCluster#project}.
        :param psc_configs: psc_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#psc_configs RedisCluster#psc_configs}
        :param redis_configs: Configure Redis Cluster behavior using a subset of native Redis configuration parameters. Please check Memorystore documentation for the list of supported parameters: https://cloud.google.com/memorystore/docs/cluster/supported-instance-configurations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#redis_configs RedisCluster#redis_configs}
        :param region: The name of the region of the Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#region RedisCluster#region}
        :param replica_count: Optional. The number of replica nodes per shard. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#replica_count RedisCluster#replica_count}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#timeouts RedisCluster#timeouts}
        :param transit_encryption_mode: Optional. The in-transit encryption for the Redis cluster. If not provided, encryption is disabled for the cluster. Default value: "TRANSIT_ENCRYPTION_MODE_DISABLED" Possible values: ["TRANSIT_ENCRYPTION_MODE_UNSPECIFIED", "TRANSIT_ENCRYPTION_MODE_DISABLED", "TRANSIT_ENCRYPTION_MODE_SERVER_AUTHENTICATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#transit_encryption_mode RedisCluster#transit_encryption_mode}
        :param zone_distribution_config: zone_distribution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#zone_distribution_config RedisCluster#zone_distribution_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(automated_backup_config, dict):
            automated_backup_config = RedisClusterAutomatedBackupConfig(**automated_backup_config)
        if isinstance(cross_cluster_replication_config, dict):
            cross_cluster_replication_config = RedisClusterCrossClusterReplicationConfig(**cross_cluster_replication_config)
        if isinstance(gcs_source, dict):
            gcs_source = RedisClusterGcsSource(**gcs_source)
        if isinstance(maintenance_policy, dict):
            maintenance_policy = RedisClusterMaintenancePolicy(**maintenance_policy)
        if isinstance(managed_backup_source, dict):
            managed_backup_source = RedisClusterManagedBackupSource(**managed_backup_source)
        if isinstance(persistence_config, dict):
            persistence_config = RedisClusterPersistenceConfig(**persistence_config)
        if isinstance(timeouts, dict):
            timeouts = RedisClusterTimeouts(**timeouts)
        if isinstance(zone_distribution_config, dict):
            zone_distribution_config = RedisClusterZoneDistributionConfig(**zone_distribution_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a458fa87944e5c0b7c21b6c2f4d8dad96f277af351cd03e39ed0330c9d692230)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#shard_count RedisCluster#shard_count}
        '''
        result = self._values.get("shard_count")
        assert result is not None, "Required property 'shard_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def authorization_mode(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The authorization mode of the Redis cluster. If not provided, auth feature is disabled for the cluster. Default value: "AUTH_MODE_DISABLED" Possible values: ["AUTH_MODE_UNSPECIFIED", "AUTH_MODE_IAM_AUTH", "AUTH_MODE_DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#authorization_mode RedisCluster#authorization_mode}
        '''
        result = self._values.get("authorization_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automated_backup_config(
        self,
    ) -> typing.Optional[RedisClusterAutomatedBackupConfig]:
        '''automated_backup_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#automated_backup_config RedisCluster#automated_backup_config}
        '''
        result = self._values.get("automated_backup_config")
        return typing.cast(typing.Optional[RedisClusterAutomatedBackupConfig], result)

    @builtins.property
    def cross_cluster_replication_config(
        self,
    ) -> typing.Optional["RedisClusterCrossClusterReplicationConfig"]:
        '''cross_cluster_replication_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#cross_cluster_replication_config RedisCluster#cross_cluster_replication_config}
        '''
        result = self._values.get("cross_cluster_replication_config")
        return typing.cast(typing.Optional["RedisClusterCrossClusterReplicationConfig"], result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Indicates if the cluster is deletion protected or not.
        If the value if set to true, any delete cluster operation will fail.
        Default value is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#deletion_protection_enabled RedisCluster#deletion_protection_enabled}
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs_source(self) -> typing.Optional["RedisClusterGcsSource"]:
        '''gcs_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#gcs_source RedisCluster#gcs_source}
        '''
        result = self._values.get("gcs_source")
        return typing.cast(typing.Optional["RedisClusterGcsSource"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#id RedisCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The KMS key used to encrypt the at-rest data of the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#kms_key RedisCluster#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_policy(self) -> typing.Optional["RedisClusterMaintenancePolicy"]:
        '''maintenance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#maintenance_policy RedisCluster#maintenance_policy}
        '''
        result = self._values.get("maintenance_policy")
        return typing.cast(typing.Optional["RedisClusterMaintenancePolicy"], result)

    @builtins.property
    def managed_backup_source(
        self,
    ) -> typing.Optional["RedisClusterManagedBackupSource"]:
        '''managed_backup_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#managed_backup_source RedisCluster#managed_backup_source}
        '''
        result = self._values.get("managed_backup_source")
        return typing.cast(typing.Optional["RedisClusterManagedBackupSource"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Unique name of the resource in this scope including project and location using the form: projects/{projectId}/locations/{locationId}/clusters/{clusterId}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#name RedisCluster#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''The nodeType for the Redis cluster.

        If not provided, REDIS_HIGHMEM_MEDIUM will be used as default Possible values: ["REDIS_SHARED_CORE_NANO", "REDIS_HIGHMEM_MEDIUM", "REDIS_HIGHMEM_XLARGE", "REDIS_STANDARD_SMALL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#node_type RedisCluster#node_type}
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def persistence_config(self) -> typing.Optional["RedisClusterPersistenceConfig"]:
        '''persistence_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#persistence_config RedisCluster#persistence_config}
        '''
        result = self._values.get("persistence_config")
        return typing.cast(typing.Optional["RedisClusterPersistenceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#project RedisCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterPscConfigs"]]]:
        '''psc_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#psc_configs RedisCluster#psc_configs}
        '''
        result = self._values.get("psc_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterPscConfigs"]]], result)

    @builtins.property
    def redis_configs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Configure Redis Cluster behavior using a subset of native Redis configuration parameters.

        Please check Memorystore documentation for the list of supported parameters:
        https://cloud.google.com/memorystore/docs/cluster/supported-instance-configurations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#redis_configs RedisCluster#redis_configs}
        '''
        result = self._values.get("redis_configs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The name of the region of the Redis cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#region RedisCluster#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Optional. The number of replica nodes per shard.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#replica_count RedisCluster#replica_count}
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RedisClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#timeouts RedisCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RedisClusterTimeouts"], result)

    @builtins.property
    def transit_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The in-transit encryption for the Redis cluster.
        If not provided, encryption is disabled for the cluster. Default value: "TRANSIT_ENCRYPTION_MODE_DISABLED" Possible values: ["TRANSIT_ENCRYPTION_MODE_UNSPECIFIED", "TRANSIT_ENCRYPTION_MODE_DISABLED", "TRANSIT_ENCRYPTION_MODE_SERVER_AUTHENTICATION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#transit_encryption_mode RedisCluster#transit_encryption_mode}
        '''
        result = self._values.get("transit_encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_distribution_config(
        self,
    ) -> typing.Optional["RedisClusterZoneDistributionConfig"]:
        '''zone_distribution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#zone_distribution_config RedisCluster#zone_distribution_config}
        '''
        result = self._values.get("zone_distribution_config")
        return typing.cast(typing.Optional["RedisClusterZoneDistributionConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_role": "clusterRole",
        "primary_cluster": "primaryCluster",
        "secondary_clusters": "secondaryClusters",
    },
)
class RedisClusterCrossClusterReplicationConfig:
    def __init__(
        self,
        *,
        cluster_role: typing.Optional[builtins.str] = None,
        primary_cluster: typing.Optional[typing.Union["RedisClusterCrossClusterReplicationConfigPrimaryCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterCrossClusterReplicationConfigSecondaryClusters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cluster_role: The role of the cluster in cross cluster replication. Supported values are:. 1. 'CLUSTER_ROLE_UNSPECIFIED': This is an independent cluster that has never participated in cross cluster replication. It allows both reads and writes. 1. 'NONE': This is an independent cluster that previously participated in cross cluster replication(either as a 'PRIMARY' or 'SECONDARY' cluster). It allows both reads and writes. 1. 'PRIMARY': This cluster serves as the replication source for secondary clusters that are replicating from it. Any data written to it is automatically replicated to its secondary clusters. It allows both reads and writes. 1. 'SECONDARY': This cluster replicates data from the primary cluster. It allows only reads. Possible values: ["CLUSTER_ROLE_UNSPECIFIED", "NONE", "PRIMARY", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#cluster_role RedisCluster#cluster_role}
        :param primary_cluster: primary_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#primary_cluster RedisCluster#primary_cluster}
        :param secondary_clusters: secondary_clusters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#secondary_clusters RedisCluster#secondary_clusters}
        '''
        if isinstance(primary_cluster, dict):
            primary_cluster = RedisClusterCrossClusterReplicationConfigPrimaryCluster(**primary_cluster)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c14043ffda4d1df498295547ff6478d4c8a9486f6ff89438e8e2cfe8198203)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#cluster_role RedisCluster#cluster_role}
        '''
        result = self._values.get("cluster_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_cluster(
        self,
    ) -> typing.Optional["RedisClusterCrossClusterReplicationConfigPrimaryCluster"]:
        '''primary_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#primary_cluster RedisCluster#primary_cluster}
        '''
        result = self._values.get("primary_cluster")
        return typing.cast(typing.Optional["RedisClusterCrossClusterReplicationConfigPrimaryCluster"], result)

    @builtins.property
    def secondary_clusters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterCrossClusterReplicationConfigSecondaryClusters"]]]:
        '''secondary_clusters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#secondary_clusters RedisCluster#secondary_clusters}
        '''
        result = self._values.get("secondary_clusters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterCrossClusterReplicationConfigSecondaryClusters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterCrossClusterReplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigMembership",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterCrossClusterReplicationConfigMembership:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterCrossClusterReplicationConfigMembership(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterCrossClusterReplicationConfigMembershipList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigMembershipList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ff259fdf451d4aeb0ac419aa05dd56c6bc8a8c5401c81887c659c7cb8e24b07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterCrossClusterReplicationConfigMembershipOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e12a8131c649aa02c90d3e9ebb4f14616e3a0a5bad1394d318ec1624059b30)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterCrossClusterReplicationConfigMembershipOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56dd1fce8ff6606bac4fdf3ed83325190abc5aab63e26de655ac1660b8011aac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__490ac8034a29269228898cab21dec88cddb129795f0a2657c9e7242f00dfef6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f12dcfa9bc51e674895fe4edda4e2fbccb32778063c2351c8d576448aea89bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterCrossClusterReplicationConfigMembershipOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigMembershipOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bd61633f846d9b78c700a2d91a255eac377785839cd4ec90924e11108785636)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="primaryCluster")
    def primary_cluster(
        self,
    ) -> "RedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterList":
        return typing.cast("RedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterList", jsii.get(self, "primaryCluster"))

    @builtins.property
    @jsii.member(jsii_name="secondaryClusters")
    def secondary_clusters(
        self,
    ) -> "RedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersList":
        return typing.cast("RedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersList", jsii.get(self, "secondaryClusters"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RedisClusterCrossClusterReplicationConfigMembership]:
        return typing.cast(typing.Optional[RedisClusterCrossClusterReplicationConfigMembership], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterCrossClusterReplicationConfigMembership],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__863e123cc4f04e2672a6d809ee0cae73bc1d49620d27554c7a42743e5aa874a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0927800c83ba8b0016a6e684245dd232fb0de7b32e3be04af1e590313b79e92b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be1c7b6488eefde831d8009a07954327ab03cbb189ccf2159cacad3407f13a1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c275bfdf50ad8fe60023d22b78c850e18d073cd0ecbb4ff548f4585c824c0823)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5c09a584b07570c7726921534f23620576ddbf9edda7d4c6102ae140b39b4f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__761343638dc07d94dcfe4cecb03b7568696c2d4dd0b70e84c291d783cf197672)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8864bb5499fd496498f9243b49ac8359adffef0c24337a259ff649ab12213564)
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
    ) -> typing.Optional[RedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster]:
        return typing.cast(typing.Optional[RedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4fe85db95dce546e5bb6d10702589f34a75f8c3d90d677cc31e9524547d60da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa5b7d6141694aaee03af091a7b29c6832749323fb88878dd8f5c47a4bbe2664)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9630d78821a7a34f62fb8be04933ca8532a61638d4c16889b45aa4dc02cdc37)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3895126bb2a41990feb0c6637eda49ca0da3fe784d69d9a5dc6d82be88df3cd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80f19d1c7298e23673dc68cf3539be3ec5113ba0e1559dbd9c432de711ed8a92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de32d53e66fbe651ae364fbb34f312fb905676fbfa2c21445b0ef4aee44fb176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef54584a26e732cb55c8cdf19484a664e39981f9f97f7c090c3baee5c9767861)
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
    ) -> typing.Optional[RedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters]:
        return typing.cast(typing.Optional[RedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a19a55fad089711d084a9a832381bfaf080be713d5237eb07ef4ee801b6d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisClusterCrossClusterReplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d73cc64e88cddde1d62a4ea190b6946dce9746614cc3c450475005ec02142ab5)
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
        :param cluster: The full resource path of the primary cluster in the format: projects/{project}/locations/{region}/clusters/{cluster-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#cluster RedisCluster#cluster}
        '''
        value = RedisClusterCrossClusterReplicationConfigPrimaryCluster(
            cluster=cluster
        )

        return typing.cast(None, jsii.invoke(self, "putPrimaryCluster", [value]))

    @jsii.member(jsii_name="putSecondaryClusters")
    def put_secondary_clusters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterCrossClusterReplicationConfigSecondaryClusters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca726b836019922f4afb39198afea9fe23200bbba793c8d030e13476f1930638)
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
    def membership(self) -> RedisClusterCrossClusterReplicationConfigMembershipList:
        return typing.cast(RedisClusterCrossClusterReplicationConfigMembershipList, jsii.get(self, "membership"))

    @builtins.property
    @jsii.member(jsii_name="primaryCluster")
    def primary_cluster(
        self,
    ) -> "RedisClusterCrossClusterReplicationConfigPrimaryClusterOutputReference":
        return typing.cast("RedisClusterCrossClusterReplicationConfigPrimaryClusterOutputReference", jsii.get(self, "primaryCluster"))

    @builtins.property
    @jsii.member(jsii_name="secondaryClusters")
    def secondary_clusters(
        self,
    ) -> "RedisClusterCrossClusterReplicationConfigSecondaryClustersList":
        return typing.cast("RedisClusterCrossClusterReplicationConfigSecondaryClustersList", jsii.get(self, "secondaryClusters"))

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
    ) -> typing.Optional["RedisClusterCrossClusterReplicationConfigPrimaryCluster"]:
        return typing.cast(typing.Optional["RedisClusterCrossClusterReplicationConfigPrimaryCluster"], jsii.get(self, "primaryClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryClustersInput")
    def secondary_clusters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterCrossClusterReplicationConfigSecondaryClusters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterCrossClusterReplicationConfigSecondaryClusters"]]], jsii.get(self, "secondaryClustersInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterRole")
    def cluster_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterRole"))

    @cluster_role.setter
    def cluster_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6098e59be7823598e1f1367d6dd9b63e40193497480f3c6679f75a4ff1d3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RedisClusterCrossClusterReplicationConfig]:
        return typing.cast(typing.Optional[RedisClusterCrossClusterReplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterCrossClusterReplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4c79a7d59e60d15ca11ec6e446d67a0e5c98a95ea20d267a7d9a0574852da6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigPrimaryCluster",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster"},
)
class RedisClusterCrossClusterReplicationConfigPrimaryCluster:
    def __init__(self, *, cluster: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cluster: The full resource path of the primary cluster in the format: projects/{project}/locations/{region}/clusters/{cluster-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#cluster RedisCluster#cluster}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__706b9649d12aefac50254ba78e2f80eb387226d76b3289a47f5221c62fd40900)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster is not None:
            self._values["cluster"] = cluster

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''The full resource path of the primary cluster in the format: projects/{project}/locations/{region}/clusters/{cluster-id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#cluster RedisCluster#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterCrossClusterReplicationConfigPrimaryCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterCrossClusterReplicationConfigPrimaryClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigPrimaryClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c753257d24b5831e5449bcf6b2bca532ea5c605993b2cb8f40c803e57412fafa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ccb7a42ca226551bd92b28d2bdf43d73499620261c505c8f020a8acf5068233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RedisClusterCrossClusterReplicationConfigPrimaryCluster]:
        return typing.cast(typing.Optional[RedisClusterCrossClusterReplicationConfigPrimaryCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterCrossClusterReplicationConfigPrimaryCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52680e68ea12a383f8d0199d23f1121341723410d49a43e7bc2f3e153f47344d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigSecondaryClusters",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster"},
)
class RedisClusterCrossClusterReplicationConfigSecondaryClusters:
    def __init__(self, *, cluster: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cluster: The full resource path of the secondary cluster in the format: projects/{project}/locations/{region}/clusters/{cluster-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#cluster RedisCluster#cluster}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed4ef696017f4fa2747c2fd1d6c020004561590c05dfed3ee16a982ae27e32c)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster is not None:
            self._values["cluster"] = cluster

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''The full resource path of the secondary cluster in the format: projects/{project}/locations/{region}/clusters/{cluster-id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#cluster RedisCluster#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterCrossClusterReplicationConfigSecondaryClusters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterCrossClusterReplicationConfigSecondaryClustersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigSecondaryClustersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1c48e570e6baf7a0b0ca2e30d71851dc1f511df7a1f8a37ca93e2f27e0bef94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterCrossClusterReplicationConfigSecondaryClustersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824d1fdc3f2698d280bedd330a1b14209521debebf177c6b7bb48e2b5b9777f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterCrossClusterReplicationConfigSecondaryClustersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__932259df91fb47f7715e950bb3e92ef6c1991bc1b06e64ac909e08e8220b9f90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e5ec83f10889234c32d33983d0a16fef9674671120ecb1d88d22f1ad83d87d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__305065c6b27859a735bc7d8f969690169bd919c6c9bd5e5652c822ffaef1f551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterCrossClusterReplicationConfigSecondaryClusters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterCrossClusterReplicationConfigSecondaryClusters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterCrossClusterReplicationConfigSecondaryClusters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25269f9f2295c16e02f4e874ec272804b3e8bf901a7ef5cdf53d87b1ccf8cbed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisClusterCrossClusterReplicationConfigSecondaryClustersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterCrossClusterReplicationConfigSecondaryClustersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e411aec68d7177a9389e8570b56b6d239f810eeb135c36388e30e7e7eccee0b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3652cff7ed4f8bdb93366a4d544ef6c0ff6e010032154675e07021705efa11bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterCrossClusterReplicationConfigSecondaryClusters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterCrossClusterReplicationConfigSecondaryClusters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterCrossClusterReplicationConfigSecondaryClusters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f015d716429976c14c54128ad0ae5a0381195b672a9678370206767e1d0324b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterDiscoveryEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterDiscoveryEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterDiscoveryEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterDiscoveryEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterDiscoveryEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f03198e371961546a576200c15b3eae217957d70ffc6cdd0ec0e4508bcc31b41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterDiscoveryEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a425736680892e5fb887267e4107bacc1320a95436215e1eb8469db21bcd8f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterDiscoveryEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733f6e2a6ae8617c6b7cb9fe1f7e7516688fe773b03b67273956cb08582de99d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac926a0e38b788d49f43909d735ebf8c8f1b8ab5444cc7ff0f1149d221c89eca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de8fe0b48f83d2949ad888908e4e3a9d0f1ceeaa42010ef4c16886a91b6cc63d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterDiscoveryEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterDiscoveryEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b9fb584a660409768581a8dbaf3675357dd18ecb2db76aadfa928c663d0ec50)
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
    def psc_config(self) -> "RedisClusterDiscoveryEndpointsPscConfigList":
        return typing.cast("RedisClusterDiscoveryEndpointsPscConfigList", jsii.get(self, "pscConfig"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterDiscoveryEndpoints]:
        return typing.cast(typing.Optional[RedisClusterDiscoveryEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterDiscoveryEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bdf6b014d7ca1bd9b203ac01ea65a1a2aa9c2c2176bc0af06fc34ee7a09c412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterDiscoveryEndpointsPscConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterDiscoveryEndpointsPscConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterDiscoveryEndpointsPscConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterDiscoveryEndpointsPscConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterDiscoveryEndpointsPscConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fe9d79467f55093de2953a2ae3aa957efa07c7f0dc1e03623aea43f8736b29e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterDiscoveryEndpointsPscConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2ff621496f41e8b1559b4f6d27b60d9d84620273550fd6b5931a08e7e540f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterDiscoveryEndpointsPscConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ece6ffb81afd2e2e6df4efad800950ea605aa4eb63474114ddd38133f83b369)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ebc2c361ae1fc5234e7473010f8268b4226b187c44dae505657f82f7ed32a76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86a5ff2992eaf62eece49e687aa434513e6426f2d913218d48019128cab65398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterDiscoveryEndpointsPscConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterDiscoveryEndpointsPscConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da3df31806055b1530eb3c732818c78d6fb8241c5b45210c47dac6c53ba87f77)
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
    ) -> typing.Optional[RedisClusterDiscoveryEndpointsPscConfig]:
        return typing.cast(typing.Optional[RedisClusterDiscoveryEndpointsPscConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterDiscoveryEndpointsPscConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370c9d0b97b55e6c9e9c6b6478e7bd9c1dcf0bb39d97046931873315b3ddf687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterGcsSource",
    jsii_struct_bases=[],
    name_mapping={"uris": "uris"},
)
class RedisClusterGcsSource:
    def __init__(self, *, uris: typing.Sequence[builtins.str]) -> None:
        '''
        :param uris: URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#uris RedisCluster#uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef2cd4659c147aebe1a9043c0f27f0795a1c80e5bcc24c48656a980681efa28)
            check_type(argname="argument uris", value=uris, expected_type=type_hints["uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uris": uris,
        }

    @builtins.property
    def uris(self) -> typing.List[builtins.str]:
        '''URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#uris RedisCluster#uris}
        '''
        result = self._values.get("uris")
        assert result is not None, "Required property 'uris' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterGcsSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterGcsSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterGcsSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f56bad8fa8eadb003d758a9711b36d8cbfc4e9544a1f9c49abcee4389b8fc22c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__228b3a0bb5c377279d7f7375dd990be34d4f0af4758e3443c894dab682e34f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterGcsSource]:
        return typing.cast(typing.Optional[RedisClusterGcsSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RedisClusterGcsSource]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008dcbbc47b7b459c6ee6aef0e4820ef2750d6542d7c1dab8ef0d3d4627f3191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterMaintenancePolicy",
    jsii_struct_bases=[],
    name_mapping={"weekly_maintenance_window": "weeklyMaintenanceWindow"},
)
class RedisClusterMaintenancePolicy:
    def __init__(
        self,
        *,
        weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#weekly_maintenance_window RedisCluster#weekly_maintenance_window}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c624e870cb374b5ce5adad818175edf368bf2bdd5f1ef2e45eaf02f00745dfba)
            check_type(argname="argument weekly_maintenance_window", value=weekly_maintenance_window, expected_type=type_hints["weekly_maintenance_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if weekly_maintenance_window is not None:
            self._values["weekly_maintenance_window"] = weekly_maintenance_window

    @builtins.property
    def weekly_maintenance_window(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterMaintenancePolicyWeeklyMaintenanceWindow"]]]:
        '''weekly_maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#weekly_maintenance_window RedisCluster#weekly_maintenance_window}
        '''
        result = self._values.get("weekly_maintenance_window")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterMaintenancePolicyWeeklyMaintenanceWindow"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterMaintenancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterMaintenancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterMaintenancePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22bd0ace9a0107aab231f53991a4a1c32be76115b7b5e6e250ab927c71cdaedf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWeeklyMaintenanceWindow")
    def put_weekly_maintenance_window(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisClusterMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f529ac240a4c4bfd4022b00727059f461a37a8d52ba533e2be6abbb2ea561c6c)
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
    ) -> "RedisClusterMaintenancePolicyWeeklyMaintenanceWindowList":
        return typing.cast("RedisClusterMaintenancePolicyWeeklyMaintenanceWindowList", jsii.get(self, "weeklyMaintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="weeklyMaintenanceWindowInput")
    def weekly_maintenance_window_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterMaintenancePolicyWeeklyMaintenanceWindow"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisClusterMaintenancePolicyWeeklyMaintenanceWindow"]]], jsii.get(self, "weeklyMaintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterMaintenancePolicy]:
        return typing.cast(typing.Optional[RedisClusterMaintenancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterMaintenancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c376070f757953365345521d8d4778fb37ecd40a79b84c8e84e8923bffbf08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterMaintenancePolicyWeeklyMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "start_time": "startTime"},
)
class RedisClusterMaintenancePolicyWeeklyMaintenanceWindow:
    def __init__(
        self,
        *,
        day: builtins.str,
        start_time: typing.Union["RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day: Required. The day of week that maintenance updates occur. - DAY_OF_WEEK_UNSPECIFIED: The day of the week is unspecified. - MONDAY: Monday - TUESDAY: Tuesday - WEDNESDAY: Wednesday - THURSDAY: Thursday - FRIDAY: Friday - SATURDAY: Saturday - SUNDAY: Sunday Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#day RedisCluster#day}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#start_time RedisCluster#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c62024fd13e91d90eda273e3f3000e99a72ecdf9066581b0686071e586d282)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#day RedisCluster#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(
        self,
    ) -> "RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#start_time RedisCluster#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterMaintenancePolicyWeeklyMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterMaintenancePolicyWeeklyMaintenanceWindowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterMaintenancePolicyWeeklyMaintenanceWindowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f9b03c9309c4aae09a9db9177b47ff920c8c746350e0a1598099eda73827fd3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterMaintenancePolicyWeeklyMaintenanceWindowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6973fd6b3f368bf15af9c30b479c56933167450444c924298607522b6cf9d5c7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterMaintenancePolicyWeeklyMaintenanceWindowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9102dc041c42c4d323730803912caf82376c9487e431fe0282cf4946bcbd03e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2203d9dae638ee348ee88b7836195531a7fdd63e6053c3450a0597a96adc7a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e9fccdc5f8017d7587855df718d228b637033c6008e5dc2fccf8fc0b112747b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterMaintenancePolicyWeeklyMaintenanceWindow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterMaintenancePolicyWeeklyMaintenanceWindow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterMaintenancePolicyWeeklyMaintenanceWindow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e891197ac8d756ddf96f05df0119073c3800bb77cd7b15b56a2fbb01b10556c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisClusterMaintenancePolicyWeeklyMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8531c3b534441209d72c5512672815bb54dbd219c2bc8f01ec4284c9fe82f8c7)
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
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#hours RedisCluster#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#minutes RedisCluster#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#nanos RedisCluster#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#seconds RedisCluster#seconds}
        '''
        value = RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime(
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
    ) -> "RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference":
        return typing.cast("RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime"]:
        return typing.cast(typing.Optional["RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145e1e2f0f9c00d34a78d0515d4058f4790533451252c93c05fe44b58290bba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterMaintenancePolicyWeeklyMaintenanceWindow]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterMaintenancePolicyWeeklyMaintenanceWindow]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterMaintenancePolicyWeeklyMaintenanceWindow]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f3e75143d4a6ee770386e39ba7cccc90cf00aaa831f48d59d9db849bb4bbb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#hours RedisCluster#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#minutes RedisCluster#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#nanos RedisCluster#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#seconds RedisCluster#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ee21c5cc668116d803adcae8dea31d906c005f85a71706b9775aa72aeccea8b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#hours RedisCluster#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#minutes RedisCluster#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#nanos RedisCluster#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time.

        Must normally be from 0 to 59.
        An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#seconds RedisCluster#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__675c35b1c78268493d29a792f77a2272e93e7eb04af36388e06e77ea96862f75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b8bea6336700a755e48e7fccefddc53f5c52414ee477c8cd49a26a6484651a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03098f0823db84c8fe0c2150cc49662e596756eaaf4caee2bea1869cad6ea63a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3e8c9cf6590f54dab92f710243b7a7df675aa699b0b0e8c290f30212e0d4c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc656e8ce6fbc7353c3e0becceadc1e65e54495a68d12139b1bef95174df4b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime]:
        return typing.cast(typing.Optional[RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612a2dc829004dd113f97f4e31037e727aea66e5e146158277275d9e38847397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterMaintenanceSchedule",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterMaintenanceSchedule:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterMaintenanceSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterMaintenanceScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterMaintenanceScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5fabc9ddfea1f0d00e0b514f22b42ee64c69de1ee76db8b3e0bb8fa4863daf7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterMaintenanceScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe7167003366470f788ee56663ef8464887da4325473275313738de5e80e640a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterMaintenanceScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9c8fd2c57cf37f34ee9910bc70e05e069e1335894d9037ae6a45c82356adff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6256eaf355de64832c057dc0835a0005e992b99cad452c5ac2baddf5d6be71d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__820dc9dd3be51495182ad577e3bd59a5bce590f94837b834e6cfcf9cd4a01e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterMaintenanceScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterMaintenanceScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efbfaa2c24a2cb1c0d673c4a24a2b4c5d4f6392d5e95134a8519a44c7b299f63)
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
    def internal_value(self) -> typing.Optional[RedisClusterMaintenanceSchedule]:
        return typing.cast(typing.Optional[RedisClusterMaintenanceSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterMaintenanceSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246ffdffa83f94ff4f4692a5bcaf6222292475d565bd022b9cd667dbc78ca51d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterManagedBackupSource",
    jsii_struct_bases=[],
    name_mapping={"backup": "backup"},
)
class RedisClusterManagedBackupSource:
    def __init__(self, *, backup: builtins.str) -> None:
        '''
        :param backup: Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#backup RedisCluster#backup}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f183743dbbafc18e16216b039c957df141e3884e7e655c68be89d9dfa1ef06e)
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup": backup,
        }

    @builtins.property
    def backup(self) -> builtins.str:
        '''Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#backup RedisCluster#backup}
        '''
        result = self._values.get("backup")
        assert result is not None, "Required property 'backup' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterManagedBackupSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterManagedBackupSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterManagedBackupSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7a4e3a4556dd45c674d882bb43b1d1ccef940352c2f21df473c173e48e5df51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__397c13e7f7bfb1b074428fff07edd22daab66eb7cfa613e4f0742f9fd50a41ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterManagedBackupSource]:
        return typing.cast(typing.Optional[RedisClusterManagedBackupSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterManagedBackupSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f2328691f83cbc836e7a1877a40fa95c6af8ff3cb0dee03ff22a9859dbe585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterManagedServerCa",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterManagedServerCa:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterManagedServerCa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterManagedServerCaCaCerts",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterManagedServerCaCaCerts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterManagedServerCaCaCerts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterManagedServerCaCaCertsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterManagedServerCaCaCertsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acd682a7820e108e0e326c9ae361227c08a7a334222b67fe4e5ca91b986d8bdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterManagedServerCaCaCertsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40dc27085abc40fc4d557d3751215b72083962dde1098dae3b3dd761a32997c1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterManagedServerCaCaCertsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223438f9318daa402c6f88073f07ee52d103740ac16c2b457be40dbbd36d501d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea2005aac7543989764046db98d3e1bd19a54acad872d5d6e82aed0596f2097a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bd3e4700a93bcfd3f8a7155e8d0cd3cc607b875114a00bc00e9c6530396c98c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterManagedServerCaCaCertsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterManagedServerCaCaCertsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ebda0dcefed4762a1bbd8b325fbd6c377b47c5e49d932438dfc59298240d3e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="certificates")
    def certificates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "certificates"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterManagedServerCaCaCerts]:
        return typing.cast(typing.Optional[RedisClusterManagedServerCaCaCerts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterManagedServerCaCaCerts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eab89702b7bc2aca14fd18086e2923de6683219b0c53e03a1d0d307b66a4f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisClusterManagedServerCaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterManagedServerCaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba2081417d3de1bdde300ab97e82f73cab6bad4e186ddfef8c585783bae39b8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RedisClusterManagedServerCaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d3bd1382c920c8c78152923b03be0468d09d5b3d9e31d411cd717ebae151288)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterManagedServerCaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc392c99750e9a1bef687211ba8824739a1814cef1a969c37a9d974ecab6877)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fa8fbb6f30d5ee38003081e4d953993459d55bf99d2310239fca673af737971)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef5c316b7c1576d1990aa6f0f2cfd22b0ed085138051a17d886eb6426409e59e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterManagedServerCaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterManagedServerCaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3946f7f23c01210c57ef8cc4e1d237dd7e87d07b8f1672fd996be01b9bd19651)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="caCerts")
    def ca_certs(self) -> RedisClusterManagedServerCaCaCertsList:
        return typing.cast(RedisClusterManagedServerCaCaCertsList, jsii.get(self, "caCerts"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterManagedServerCa]:
        return typing.cast(typing.Optional[RedisClusterManagedServerCa], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterManagedServerCa],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3089aac35c02f4915614c3033226915f9d971d0d11c987df82f503be31ae6216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPersistenceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aof_config": "aofConfig",
        "mode": "mode",
        "rdb_config": "rdbConfig",
    },
)
class RedisClusterPersistenceConfig:
    def __init__(
        self,
        *,
        aof_config: typing.Optional[typing.Union["RedisClusterPersistenceConfigAofConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        rdb_config: typing.Optional[typing.Union["RedisClusterPersistenceConfigRdbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aof_config: aof_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#aof_config RedisCluster#aof_config}
        :param mode: Optional. Controls whether Persistence features are enabled. If not provided, the existing value will be used. - DISABLED: Persistence (both backup and restore) is disabled for the cluster. - RDB: RDB based Persistence is enabled. - AOF: AOF based Persistence is enabled. Possible values: ["PERSISTENCE_MODE_UNSPECIFIED", "DISABLED", "RDB", "AOF"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#mode RedisCluster#mode}
        :param rdb_config: rdb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#rdb_config RedisCluster#rdb_config}
        '''
        if isinstance(aof_config, dict):
            aof_config = RedisClusterPersistenceConfigAofConfig(**aof_config)
        if isinstance(rdb_config, dict):
            rdb_config = RedisClusterPersistenceConfigRdbConfig(**rdb_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c2962489f8142f3acf4901197fa015cc161fed42e984e3ab828dd92252de6f)
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
    def aof_config(self) -> typing.Optional["RedisClusterPersistenceConfigAofConfig"]:
        '''aof_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#aof_config RedisCluster#aof_config}
        '''
        result = self._values.get("aof_config")
        return typing.cast(typing.Optional["RedisClusterPersistenceConfigAofConfig"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Controls whether Persistence features are enabled. If not provided, the existing value will be used.

        - DISABLED: 	Persistence (both backup and restore) is disabled for the cluster.
        - RDB: RDB based Persistence is enabled.
        - AOF: AOF based Persistence is enabled. Possible values: ["PERSISTENCE_MODE_UNSPECIFIED", "DISABLED", "RDB", "AOF"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#mode RedisCluster#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_config(self) -> typing.Optional["RedisClusterPersistenceConfigRdbConfig"]:
        '''rdb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#rdb_config RedisCluster#rdb_config}
        '''
        result = self._values.get("rdb_config")
        return typing.cast(typing.Optional["RedisClusterPersistenceConfigRdbConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterPersistenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPersistenceConfigAofConfig",
    jsii_struct_bases=[],
    name_mapping={"append_fsync": "appendFsync"},
)
class RedisClusterPersistenceConfigAofConfig:
    def __init__(self, *, append_fsync: typing.Optional[builtins.str] = None) -> None:
        '''
        :param append_fsync: Optional. Available fsync modes. - NO - Do not explicitly call fsync(). Rely on OS defaults. - EVERYSEC - Call fsync() once per second in a background thread. A balance between performance and durability. - ALWAYS - Call fsync() for earch write command. Possible values: ["APPEND_FSYNC_UNSPECIFIED", "NO", "EVERYSEC", "ALWAYS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#append_fsync RedisCluster#append_fsync}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e643344fe3ff0dda94af918e9eba991358a43854a9dfedf080c5400d2bd3d254)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#append_fsync RedisCluster#append_fsync}
        '''
        result = self._values.get("append_fsync")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterPersistenceConfigAofConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterPersistenceConfigAofConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPersistenceConfigAofConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7f8ac7a77b480e22b39bf3770439df8bf085c88d64b16352e264a1a868cc7d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e41d8e40781cfe9814884a67ff780d68ab3087f52185f4d085f7c9011d6403fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appendFsync", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterPersistenceConfigAofConfig]:
        return typing.cast(typing.Optional[RedisClusterPersistenceConfigAofConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterPersistenceConfigAofConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ddf2401927a659663d69d3c4196acd075980c7b305334b97dc589b6d8532f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisClusterPersistenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPersistenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69c3e3371e068576b3cf06667921dcc7b1466dd8dd5031612c18d3f1f52be21b)
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
        :param append_fsync: Optional. Available fsync modes. - NO - Do not explicitly call fsync(). Rely on OS defaults. - EVERYSEC - Call fsync() once per second in a background thread. A balance between performance and durability. - ALWAYS - Call fsync() for earch write command. Possible values: ["APPEND_FSYNC_UNSPECIFIED", "NO", "EVERYSEC", "ALWAYS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#append_fsync RedisCluster#append_fsync}
        '''
        value = RedisClusterPersistenceConfigAofConfig(append_fsync=append_fsync)

        return typing.cast(None, jsii.invoke(self, "putAofConfig", [value]))

    @jsii.member(jsii_name="putRdbConfig")
    def put_rdb_config(
        self,
        *,
        rdb_snapshot_period: typing.Optional[builtins.str] = None,
        rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rdb_snapshot_period: Optional. Available snapshot periods for scheduling. - ONE_HOUR: Snapshot every 1 hour. - SIX_HOURS: Snapshot every 6 hours. - TWELVE_HOURS: Snapshot every 12 hours. - TWENTY_FOUR_HOURS: Snapshot every 24 hours. Possible values: ["SNAPSHOT_PERIOD_UNSPECIFIED", "ONE_HOUR", "SIX_HOURS", "TWELVE_HOURS", "TWENTY_FOUR_HOURS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#rdb_snapshot_period RedisCluster#rdb_snapshot_period}
        :param rdb_snapshot_start_time: The time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#rdb_snapshot_start_time RedisCluster#rdb_snapshot_start_time}
        '''
        value = RedisClusterPersistenceConfigRdbConfig(
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
    def aof_config(self) -> RedisClusterPersistenceConfigAofConfigOutputReference:
        return typing.cast(RedisClusterPersistenceConfigAofConfigOutputReference, jsii.get(self, "aofConfig"))

    @builtins.property
    @jsii.member(jsii_name="rdbConfig")
    def rdb_config(self) -> "RedisClusterPersistenceConfigRdbConfigOutputReference":
        return typing.cast("RedisClusterPersistenceConfigRdbConfigOutputReference", jsii.get(self, "rdbConfig"))

    @builtins.property
    @jsii.member(jsii_name="aofConfigInput")
    def aof_config_input(
        self,
    ) -> typing.Optional[RedisClusterPersistenceConfigAofConfig]:
        return typing.cast(typing.Optional[RedisClusterPersistenceConfigAofConfig], jsii.get(self, "aofConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbConfigInput")
    def rdb_config_input(
        self,
    ) -> typing.Optional["RedisClusterPersistenceConfigRdbConfig"]:
        return typing.cast(typing.Optional["RedisClusterPersistenceConfigRdbConfig"], jsii.get(self, "rdbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef78f8dcab0c6ae6cb5295c7722335af85320ba862214cf6de4ef5eaab2963d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterPersistenceConfig]:
        return typing.cast(typing.Optional[RedisClusterPersistenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterPersistenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42141cc0c77b8a60aa77cf8325ed84f14da74ac3093cb44cd307ae3fe6612611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPersistenceConfigRdbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "rdb_snapshot_period": "rdbSnapshotPeriod",
        "rdb_snapshot_start_time": "rdbSnapshotStartTime",
    },
)
class RedisClusterPersistenceConfigRdbConfig:
    def __init__(
        self,
        *,
        rdb_snapshot_period: typing.Optional[builtins.str] = None,
        rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rdb_snapshot_period: Optional. Available snapshot periods for scheduling. - ONE_HOUR: Snapshot every 1 hour. - SIX_HOURS: Snapshot every 6 hours. - TWELVE_HOURS: Snapshot every 12 hours. - TWENTY_FOUR_HOURS: Snapshot every 24 hours. Possible values: ["SNAPSHOT_PERIOD_UNSPECIFIED", "ONE_HOUR", "SIX_HOURS", "TWELVE_HOURS", "TWENTY_FOUR_HOURS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#rdb_snapshot_period RedisCluster#rdb_snapshot_period}
        :param rdb_snapshot_start_time: The time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#rdb_snapshot_start_time RedisCluster#rdb_snapshot_start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279942e90a3ca1209ec1f59fa14d88f968fc9042699307f41bf816412ae94bf0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#rdb_snapshot_period RedisCluster#rdb_snapshot_period}
        '''
        result = self._values.get("rdb_snapshot_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_snapshot_start_time(self) -> typing.Optional[builtins.str]:
        '''The time that the first snapshot was/will be attempted, and to which future snapshots will be aligned.

        If not provided, the current time will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#rdb_snapshot_start_time RedisCluster#rdb_snapshot_start_time}
        '''
        result = self._values.get("rdb_snapshot_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterPersistenceConfigRdbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterPersistenceConfigRdbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPersistenceConfigRdbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eeac47f464e4d75b2c827c2b55f864965018d894cdfefd3f7e70bb16ac0466be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b336b32ca8200f29388b7ee072d052661ef8845fd5a4076a015313c25139de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotStartTime")
    def rdb_snapshot_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdbSnapshotStartTime"))

    @rdb_snapshot_start_time.setter
    def rdb_snapshot_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39faca7d5fcfa2dc233388483896510c102bcf288dda947b6d1277fe8d985a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterPersistenceConfigRdbConfig]:
        return typing.cast(typing.Optional[RedisClusterPersistenceConfigRdbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterPersistenceConfigRdbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2f9c29c8d2ed4d0f9074da7758c2ce0404be084f6aa28897529aa8bf54e042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPscConfigs",
    jsii_struct_bases=[],
    name_mapping={"network": "network"},
)
class RedisClusterPscConfigs:
    def __init__(self, *, network: builtins.str) -> None:
        '''
        :param network: Required. The consumer network where the network address of the discovery endpoint will be reserved, in the form of projects/{network_project_id_or_number}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#network RedisCluster#network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de49c8bb81e1ab61bf816c864e73c59f5c0f21f65f596fa1ed7bea5cdd6d0c71)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network": network,
        }

    @builtins.property
    def network(self) -> builtins.str:
        '''Required. The consumer network where the network address of the discovery endpoint will be reserved, in the form of projects/{network_project_id_or_number}/global/networks/{network_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#network RedisCluster#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterPscConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterPscConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPscConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c28bd8546bbecca9dc227508b5a8968dd4bdddb38e543ad2ba7436a56762949f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RedisClusterPscConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a3a9e217e7261ab42e3c3213a8ae5b722ad56efd7f1bf4705ea932bab21b21)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterPscConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd0066adb9838d0b98dcb69c9d229ecd4a1ea454d90c21c0d26f5e90aa0b164)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54a551a3d9638c394b0f2396a29f0708ffec2cc3e41447b6c1459d15cfb50767)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b07c19b3d157a646b36de51ca2180b2295cf3016c0ac8d2d4b4e00961e27e01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterPscConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterPscConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterPscConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b32b4e78ab97c8179bc351f1483fa56a84d3de96f48640e55ff9b3dcaae5e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisClusterPscConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPscConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25533c30151a514f02c022488bd80bb0ea67c0d88352739cdecd75ac1adfada0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cdbc8cd5608a4d79a84655ddf574645c6bbb33e01e37863d48836c2794e287c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterPscConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterPscConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterPscConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81130e86d8dd540d74255597f1a57f244aecaa6239eefc1e735a104bfa2f448f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPscConnections",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterPscConnections:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterPscConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterPscConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPscConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7e8d125741da761411e2073ed399236d0e4f7ee95e0869e066b3372dd74c370)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RedisClusterPscConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e948b3c1756a47a10e1009af4492ca7df50bacedbb47150490eb2bfcaf7af0f3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterPscConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1d0f72b438c8454d605751ff7f14026242a206947a92a2e7d248f73754be96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b98e004e864dc759e70913f4ad70378bf752b6fef99c30c97fd5baecd25aaa9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5767c17d8145bdd3acb06cdf0bef838f33ddd1270d222a38946ba448bff473ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterPscConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPscConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ea872521602c5f18120ad90acc42e82abece9d937eea4fab9507665bfbf55e4)
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
    def internal_value(self) -> typing.Optional[RedisClusterPscConnections]:
        return typing.cast(typing.Optional[RedisClusterPscConnections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterPscConnections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0127d30b5784e397811cddf6af610013b3bcba84014d67476a3f619434d24bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPscServiceAttachments",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterPscServiceAttachments:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterPscServiceAttachments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterPscServiceAttachmentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPscServiceAttachmentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2573000eaff1e22f7a4605d6d95b985c7b032a628a3d787b1a0db07b9395befa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterPscServiceAttachmentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87d75b50ae4beb4ce41f591a88fda4ec5f1daa0fb63bd14f8776bd9dc179656)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterPscServiceAttachmentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10079e27900dec5882d1bd8d7b0ab12ffad11bca72417ded8ab14351610d205a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__435a44d51c2e93e4e17106eb8fdb9b98508d1a3a69898214693e9ad5ad4ecc15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eecd2d61a64dcec93bce362aa9ceec29d674402503ec5e8674871615e6245e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterPscServiceAttachmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterPscServiceAttachmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9953b235af5dcf9ae79b81d4477083dfc80663aa7a674f34f7b33823ccda1f4b)
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
    def internal_value(self) -> typing.Optional[RedisClusterPscServiceAttachments]:
        return typing.cast(typing.Optional[RedisClusterPscServiceAttachments], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterPscServiceAttachments],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72379507c6e76ca8bff77097e11a64907b2245bd558e7f580e0316ebcd7f5fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterStateInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterStateInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterStateInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterStateInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterStateInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e7975f4ade1eb58f2fa29be95ac3ddc89279ead8b68da2163ae2b2779c35c33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RedisClusterStateInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e6f983e674dfc8e2cd832c649186ea8d125877a056345dd9233064da1956d6c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterStateInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874277045801d880e82865b8c6d412f1ac5dacbb46fbd36f803f8be44ba1ea62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d53aacaef2dc0ee09aca17d796cf7ecc29d45382c40b44f8076f80b31d5ef31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f2952494cfd8cbddb3da519d56f0b003a05f89af969231ecefbe4892aa78683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterStateInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterStateInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8527c4eb0d119afbc93f63c52a0471e4dbb18e18ae5e760db718deb07c80d137)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="updateInfo")
    def update_info(self) -> "RedisClusterStateInfoUpdateInfoList":
        return typing.cast("RedisClusterStateInfoUpdateInfoList", jsii.get(self, "updateInfo"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterStateInfo]:
        return typing.cast(typing.Optional[RedisClusterStateInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RedisClusterStateInfo]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b51a764d65d60ea090f7dcaffa21f4da213a7e2188d5dd23ad460eead14dc59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterStateInfoUpdateInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisClusterStateInfoUpdateInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterStateInfoUpdateInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterStateInfoUpdateInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterStateInfoUpdateInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9209e41b9fc23291d05cfcb51583eb2da29ef5328d7407cbb492d300017daca0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisClusterStateInfoUpdateInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a043918a195ce8d5aef941a11f98129705acbac8dde77211e87ac541dcf4d836)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisClusterStateInfoUpdateInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7924605145a529c98f5f6089a90116dcba8f4f0963aa25cddfd8e30b350f4a65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37b24938133ed0977510b30293cf6553a8657bc79ce92ddd0c3f861585c8070b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44685122ef6b642ac48a4ae8ae8fa1e34356bcb9cb889574fc6452e1fc872822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisClusterStateInfoUpdateInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterStateInfoUpdateInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e7ed80f0c2bd6174b5b5132bb82f8a9ec696054cabe6164e66898ed76a872b9)
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
    def internal_value(self) -> typing.Optional[RedisClusterStateInfoUpdateInfo]:
        return typing.cast(typing.Optional[RedisClusterStateInfoUpdateInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterStateInfoUpdateInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69857c1f0fcda05ac958300d203030c97e7ae719a27e39b793f799f20b3dacf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class RedisClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#create RedisCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#delete RedisCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#update RedisCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f7a96b542d0edf0cf08d04da3a1548eaeea01dc7de6309b9bb4a71f518a4ab)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#create RedisCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#delete RedisCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#update RedisCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__addc905d01e2ce1a9c204f30a844174e680b68fe4a2f06147564d3036f643d09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0231e15156fc1ba0698511d1a7e84358c7172e71996212a1dfd096f591d5d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__339c592a33b25e479bb76b0036006c4ad5864fd32726b04faa86bbbd1f1ee261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c794bffe65180d5e07a60d6f9e0996dcb648368838ec8442fd8f57fdc4ae52c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51ced3d15e65b3f82a24e33b430cb111f323f534269e2c1c357e1360000e594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterZoneDistributionConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "zone": "zone"},
)
class RedisClusterZoneDistributionConfig:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Immutable. The mode for zone distribution for Memorystore Redis cluster. If not provided, MULTI_ZONE will be used as default Possible values: ["MULTI_ZONE", "SINGLE_ZONE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#mode RedisCluster#mode}
        :param zone: Immutable. The zone for single zone Memorystore Redis cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#zone RedisCluster#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721ae4062cdf34992370a344616853368db826fb221ebd33fc91c31ef0e7f492)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#mode RedisCluster#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Immutable. The zone for single zone Memorystore Redis cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_cluster#zone RedisCluster#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisClusterZoneDistributionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisClusterZoneDistributionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisCluster.RedisClusterZoneDistributionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e9e0ab591d52d32fd748e68ae6701917d1ef326578b4c3d5c2fff593099218b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fb080ca0a37ac745f608ec26a4f2f955d5a9c564fea498124b1951086bd2cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73caadbfa4152468bfaa7e949f182e67113746b288e4d3de6d8127da1a972dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisClusterZoneDistributionConfig]:
        return typing.cast(typing.Optional[RedisClusterZoneDistributionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisClusterZoneDistributionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe177aa560e6ddd8e04d980e64b3e581135e2a7afd75616b00c12ab831e306da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RedisCluster",
    "RedisClusterAutomatedBackupConfig",
    "RedisClusterAutomatedBackupConfigFixedFrequencySchedule",
    "RedisClusterAutomatedBackupConfigFixedFrequencyScheduleOutputReference",
    "RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime",
    "RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference",
    "RedisClusterAutomatedBackupConfigOutputReference",
    "RedisClusterConfig",
    "RedisClusterCrossClusterReplicationConfig",
    "RedisClusterCrossClusterReplicationConfigMembership",
    "RedisClusterCrossClusterReplicationConfigMembershipList",
    "RedisClusterCrossClusterReplicationConfigMembershipOutputReference",
    "RedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster",
    "RedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterList",
    "RedisClusterCrossClusterReplicationConfigMembershipPrimaryClusterOutputReference",
    "RedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters",
    "RedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersList",
    "RedisClusterCrossClusterReplicationConfigMembershipSecondaryClustersOutputReference",
    "RedisClusterCrossClusterReplicationConfigOutputReference",
    "RedisClusterCrossClusterReplicationConfigPrimaryCluster",
    "RedisClusterCrossClusterReplicationConfigPrimaryClusterOutputReference",
    "RedisClusterCrossClusterReplicationConfigSecondaryClusters",
    "RedisClusterCrossClusterReplicationConfigSecondaryClustersList",
    "RedisClusterCrossClusterReplicationConfigSecondaryClustersOutputReference",
    "RedisClusterDiscoveryEndpoints",
    "RedisClusterDiscoveryEndpointsList",
    "RedisClusterDiscoveryEndpointsOutputReference",
    "RedisClusterDiscoveryEndpointsPscConfig",
    "RedisClusterDiscoveryEndpointsPscConfigList",
    "RedisClusterDiscoveryEndpointsPscConfigOutputReference",
    "RedisClusterGcsSource",
    "RedisClusterGcsSourceOutputReference",
    "RedisClusterMaintenancePolicy",
    "RedisClusterMaintenancePolicyOutputReference",
    "RedisClusterMaintenancePolicyWeeklyMaintenanceWindow",
    "RedisClusterMaintenancePolicyWeeklyMaintenanceWindowList",
    "RedisClusterMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
    "RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    "RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
    "RedisClusterMaintenanceSchedule",
    "RedisClusterMaintenanceScheduleList",
    "RedisClusterMaintenanceScheduleOutputReference",
    "RedisClusterManagedBackupSource",
    "RedisClusterManagedBackupSourceOutputReference",
    "RedisClusterManagedServerCa",
    "RedisClusterManagedServerCaCaCerts",
    "RedisClusterManagedServerCaCaCertsList",
    "RedisClusterManagedServerCaCaCertsOutputReference",
    "RedisClusterManagedServerCaList",
    "RedisClusterManagedServerCaOutputReference",
    "RedisClusterPersistenceConfig",
    "RedisClusterPersistenceConfigAofConfig",
    "RedisClusterPersistenceConfigAofConfigOutputReference",
    "RedisClusterPersistenceConfigOutputReference",
    "RedisClusterPersistenceConfigRdbConfig",
    "RedisClusterPersistenceConfigRdbConfigOutputReference",
    "RedisClusterPscConfigs",
    "RedisClusterPscConfigsList",
    "RedisClusterPscConfigsOutputReference",
    "RedisClusterPscConnections",
    "RedisClusterPscConnectionsList",
    "RedisClusterPscConnectionsOutputReference",
    "RedisClusterPscServiceAttachments",
    "RedisClusterPscServiceAttachmentsList",
    "RedisClusterPscServiceAttachmentsOutputReference",
    "RedisClusterStateInfo",
    "RedisClusterStateInfoList",
    "RedisClusterStateInfoOutputReference",
    "RedisClusterStateInfoUpdateInfo",
    "RedisClusterStateInfoUpdateInfoList",
    "RedisClusterStateInfoUpdateInfoOutputReference",
    "RedisClusterTimeouts",
    "RedisClusterTimeoutsOutputReference",
    "RedisClusterZoneDistributionConfig",
    "RedisClusterZoneDistributionConfigOutputReference",
]

publication.publish()

def _typecheckingstub__0a1279b263e30e89b4adb662713bc653e88c407a80eac215ff514d1a7fb576e8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    shard_count: jsii.Number,
    authorization_mode: typing.Optional[builtins.str] = None,
    automated_backup_config: typing.Optional[typing.Union[RedisClusterAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_cluster_replication_config: typing.Optional[typing.Union[RedisClusterCrossClusterReplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs_source: typing.Optional[typing.Union[RedisClusterGcsSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    maintenance_policy: typing.Optional[typing.Union[RedisClusterMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_backup_source: typing.Optional[typing.Union[RedisClusterManagedBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[RedisClusterPersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterPscConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[RedisClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
    zone_distribution_config: typing.Optional[typing.Union[RedisClusterZoneDistributionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__96dc43aef9a7a9b7e72df44214a098cbbcdf1b0ff1d39d211f72c56ca83d2b00(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73056aee06e39178c1d7923cfb999b17d58284857f252bcd2fb4277cb2108380(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterPscConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaac2f220b51f3f67b518419f8bbeddeef593ec6a8c5840a62c83ed528f18118(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b1ead5d805653aac0616483ade5eb3a8c4c34372fba592d688ba1ba8dde04e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce1013726b5f7e3ea08061fac21aa588fc248ada25589ff0fe46662fbc72139(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35acdae521951c5e0f1458d8c4e39f73586020e35f34653b590ae5125cb22595(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb291622a5350d8f06500fa5978273e7a6bb63c8a573a003d01aa6384018e2f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8771f3439d7db57341cb41d446eaa4294a4004f40c1350e2fa8b193889fa7048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f333d4f43b3b2933fc10c93d049529a410ed4b012a84fda09c0e7a596ccda16a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3db4050d42d9e3a67fd9b5bec731aca251148cacd7870e21b2af68b95643bc1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b53dead1ccc2a65d93bf7bebcd349f895dbd10323017e9808c883c21f7b807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae7679a6bfa55296546cdddb0f8b844167a7771c36342703546a9c14303ac64(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e268e2b984765e277bedd6d984d6dc5f99ee41ce0032d89f1613b0d86e0cb98e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04317156b5d255b686379895ad5dc76666aa40e949de04c3451a3b35674e04af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97fef90420a3848f0114ba3ce0642dc670eadfdaf9a43e1ced4fcc79c30f57b(
    *,
    fixed_frequency_schedule: typing.Union[RedisClusterAutomatedBackupConfigFixedFrequencySchedule, typing.Dict[builtins.str, typing.Any]],
    retention: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a8e0b4defcbb6d2cd94fbc43de8c3d5351e843b23d735d6d303f246bf1cbd8(
    *,
    start_time: typing.Union[RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5ee03ae806add08fa48a0484e379f6b683ef65cbf6e81a6e5ee05b4f687c34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0b9f5dd0bd3f5a3c7094037f10b47f2aee9114e9eb16579241d5da195da582(
    value: typing.Optional[RedisClusterAutomatedBackupConfigFixedFrequencySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e879ce83171dd84fc0310ee5acb026397c22c1adb73f4c99933048bc632b56(
    *,
    hours: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83efb656fa9cfb75db30d3b64d5b1a3cf75591e1c1b61338e66644588ebd0f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c162a6023ac9af8cb061f14673fec73153ff8733a4b0e2253e48d550158c233(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a298781769e022c559ce570e8f47f690d62bae87a08ffcb67b71da53aea2396e(
    value: typing.Optional[RedisClusterAutomatedBackupConfigFixedFrequencyScheduleStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951cd0393cc0bd48648e44ae5fa0070d05a60419609664402faa0d94722ca37a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab3759a43805f91f2dd8c2ceaaaedd99c823c62076dc23667d317fd2aeb62d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75553589284069415d5e2fd1f4f4955dd4bc30aef738616c10de7489fe325a8(
    value: typing.Optional[RedisClusterAutomatedBackupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a458fa87944e5c0b7c21b6c2f4d8dad96f277af351cd03e39ed0330c9d692230(
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
    automated_backup_config: typing.Optional[typing.Union[RedisClusterAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_cluster_replication_config: typing.Optional[typing.Union[RedisClusterCrossClusterReplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs_source: typing.Optional[typing.Union[RedisClusterGcsSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    maintenance_policy: typing.Optional[typing.Union[RedisClusterMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_backup_source: typing.Optional[typing.Union[RedisClusterManagedBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[RedisClusterPersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterPscConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[RedisClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
    zone_distribution_config: typing.Optional[typing.Union[RedisClusterZoneDistributionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c14043ffda4d1df498295547ff6478d4c8a9486f6ff89438e8e2cfe8198203(
    *,
    cluster_role: typing.Optional[builtins.str] = None,
    primary_cluster: typing.Optional[typing.Union[RedisClusterCrossClusterReplicationConfigPrimaryCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    secondary_clusters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterCrossClusterReplicationConfigSecondaryClusters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff259fdf451d4aeb0ac419aa05dd56c6bc8a8c5401c81887c659c7cb8e24b07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e12a8131c649aa02c90d3e9ebb4f14616e3a0a5bad1394d318ec1624059b30(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56dd1fce8ff6606bac4fdf3ed83325190abc5aab63e26de655ac1660b8011aac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490ac8034a29269228898cab21dec88cddb129795f0a2657c9e7242f00dfef6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12dcfa9bc51e674895fe4edda4e2fbccb32778063c2351c8d576448aea89bc1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd61633f846d9b78c700a2d91a255eac377785839cd4ec90924e11108785636(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863e123cc4f04e2672a6d809ee0cae73bc1d49620d27554c7a42743e5aa874a7(
    value: typing.Optional[RedisClusterCrossClusterReplicationConfigMembership],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0927800c83ba8b0016a6e684245dd232fb0de7b32e3be04af1e590313b79e92b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be1c7b6488eefde831d8009a07954327ab03cbb189ccf2159cacad3407f13a1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c275bfdf50ad8fe60023d22b78c850e18d073cd0ecbb4ff548f4585c824c0823(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c09a584b07570c7726921534f23620576ddbf9edda7d4c6102ae140b39b4f7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761343638dc07d94dcfe4cecb03b7568696c2d4dd0b70e84c291d783cf197672(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8864bb5499fd496498f9243b49ac8359adffef0c24337a259ff649ab12213564(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fe85db95dce546e5bb6d10702589f34a75f8c3d90d677cc31e9524547d60da(
    value: typing.Optional[RedisClusterCrossClusterReplicationConfigMembershipPrimaryCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5b7d6141694aaee03af091a7b29c6832749323fb88878dd8f5c47a4bbe2664(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9630d78821a7a34f62fb8be04933ca8532a61638d4c16889b45aa4dc02cdc37(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3895126bb2a41990feb0c6637eda49ca0da3fe784d69d9a5dc6d82be88df3cd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f19d1c7298e23673dc68cf3539be3ec5113ba0e1559dbd9c432de711ed8a92(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de32d53e66fbe651ae364fbb34f312fb905676fbfa2c21445b0ef4aee44fb176(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef54584a26e732cb55c8cdf19484a664e39981f9f97f7c090c3baee5c9767861(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a19a55fad089711d084a9a832381bfaf080be713d5237eb07ef4ee801b6d20(
    value: typing.Optional[RedisClusterCrossClusterReplicationConfigMembershipSecondaryClusters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73cc64e88cddde1d62a4ea190b6946dce9746614cc3c450475005ec02142ab5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca726b836019922f4afb39198afea9fe23200bbba793c8d030e13476f1930638(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterCrossClusterReplicationConfigSecondaryClusters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6098e59be7823598e1f1367d6dd9b63e40193497480f3c6679f75a4ff1d3f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4c79a7d59e60d15ca11ec6e446d67a0e5c98a95ea20d267a7d9a0574852da6(
    value: typing.Optional[RedisClusterCrossClusterReplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__706b9649d12aefac50254ba78e2f80eb387226d76b3289a47f5221c62fd40900(
    *,
    cluster: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c753257d24b5831e5449bcf6b2bca532ea5c605993b2cb8f40c803e57412fafa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ccb7a42ca226551bd92b28d2bdf43d73499620261c505c8f020a8acf5068233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52680e68ea12a383f8d0199d23f1121341723410d49a43e7bc2f3e153f47344d(
    value: typing.Optional[RedisClusterCrossClusterReplicationConfigPrimaryCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed4ef696017f4fa2747c2fd1d6c020004561590c05dfed3ee16a982ae27e32c(
    *,
    cluster: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c48e570e6baf7a0b0ca2e30d71851dc1f511df7a1f8a37ca93e2f27e0bef94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824d1fdc3f2698d280bedd330a1b14209521debebf177c6b7bb48e2b5b9777f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__932259df91fb47f7715e950bb3e92ef6c1991bc1b06e64ac909e08e8220b9f90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5ec83f10889234c32d33983d0a16fef9674671120ecb1d88d22f1ad83d87d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305065c6b27859a735bc7d8f969690169bd919c6c9bd5e5652c822ffaef1f551(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25269f9f2295c16e02f4e874ec272804b3e8bf901a7ef5cdf53d87b1ccf8cbed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterCrossClusterReplicationConfigSecondaryClusters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e411aec68d7177a9389e8570b56b6d239f810eeb135c36388e30e7e7eccee0b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3652cff7ed4f8bdb93366a4d544ef6c0ff6e010032154675e07021705efa11bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f015d716429976c14c54128ad0ae5a0381195b672a9678370206767e1d0324b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterCrossClusterReplicationConfigSecondaryClusters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03198e371961546a576200c15b3eae217957d70ffc6cdd0ec0e4508bcc31b41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a425736680892e5fb887267e4107bacc1320a95436215e1eb8469db21bcd8f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733f6e2a6ae8617c6b7cb9fe1f7e7516688fe773b03b67273956cb08582de99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac926a0e38b788d49f43909d735ebf8c8f1b8ab5444cc7ff0f1149d221c89eca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8fe0b48f83d2949ad888908e4e3a9d0f1ceeaa42010ef4c16886a91b6cc63d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9fb584a660409768581a8dbaf3675357dd18ecb2db76aadfa928c663d0ec50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bdf6b014d7ca1bd9b203ac01ea65a1a2aa9c2c2176bc0af06fc34ee7a09c412(
    value: typing.Optional[RedisClusterDiscoveryEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe9d79467f55093de2953a2ae3aa957efa07c7f0dc1e03623aea43f8736b29e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2ff621496f41e8b1559b4f6d27b60d9d84620273550fd6b5931a08e7e540f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ece6ffb81afd2e2e6df4efad800950ea605aa4eb63474114ddd38133f83b369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebc2c361ae1fc5234e7473010f8268b4226b187c44dae505657f82f7ed32a76(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a5ff2992eaf62eece49e687aa434513e6426f2d913218d48019128cab65398(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3df31806055b1530eb3c732818c78d6fb8241c5b45210c47dac6c53ba87f77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370c9d0b97b55e6c9e9c6b6478e7bd9c1dcf0bb39d97046931873315b3ddf687(
    value: typing.Optional[RedisClusterDiscoveryEndpointsPscConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef2cd4659c147aebe1a9043c0f27f0795a1c80e5bcc24c48656a980681efa28(
    *,
    uris: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f56bad8fa8eadb003d758a9711b36d8cbfc4e9544a1f9c49abcee4389b8fc22c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228b3a0bb5c377279d7f7375dd990be34d4f0af4758e3443c894dab682e34f30(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008dcbbc47b7b459c6ee6aef0e4820ef2750d6542d7c1dab8ef0d3d4627f3191(
    value: typing.Optional[RedisClusterGcsSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c624e870cb374b5ce5adad818175edf368bf2bdd5f1ef2e45eaf02f00745dfba(
    *,
    weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22bd0ace9a0107aab231f53991a4a1c32be76115b7b5e6e250ab927c71cdaedf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f529ac240a4c4bfd4022b00727059f461a37a8d52ba533e2be6abbb2ea561c6c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisClusterMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c376070f757953365345521d8d4778fb37ecd40a79b84c8e84e8923bffbf08(
    value: typing.Optional[RedisClusterMaintenancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c62024fd13e91d90eda273e3f3000e99a72ecdf9066581b0686071e586d282(
    *,
    day: builtins.str,
    start_time: typing.Union[RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9b03c9309c4aae09a9db9177b47ff920c8c746350e0a1598099eda73827fd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6973fd6b3f368bf15af9c30b479c56933167450444c924298607522b6cf9d5c7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9102dc041c42c4d323730803912caf82376c9487e431fe0282cf4946bcbd03e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2203d9dae638ee348ee88b7836195531a7fdd63e6053c3450a0597a96adc7a3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9fccdc5f8017d7587855df718d228b637033c6008e5dc2fccf8fc0b112747b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e891197ac8d756ddf96f05df0119073c3800bb77cd7b15b56a2fbb01b10556c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterMaintenancePolicyWeeklyMaintenanceWindow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8531c3b534441209d72c5512672815bb54dbd219c2bc8f01ec4284c9fe82f8c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145e1e2f0f9c00d34a78d0515d4058f4790533451252c93c05fe44b58290bba6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f3e75143d4a6ee770386e39ba7cccc90cf00aaa831f48d59d9db849bb4bbb9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterMaintenancePolicyWeeklyMaintenanceWindow]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee21c5cc668116d803adcae8dea31d906c005f85a71706b9775aa72aeccea8b(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675c35b1c78268493d29a792f77a2272e93e7eb04af36388e06e77ea96862f75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8bea6336700a755e48e7fccefddc53f5c52414ee477c8cd49a26a6484651a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03098f0823db84c8fe0c2150cc49662e596756eaaf4caee2bea1869cad6ea63a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3e8c9cf6590f54dab92f710243b7a7df675aa699b0b0e8c290f30212e0d4c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc656e8ce6fbc7353c3e0becceadc1e65e54495a68d12139b1bef95174df4b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612a2dc829004dd113f97f4e31037e727aea66e5e146158277275d9e38847397(
    value: typing.Optional[RedisClusterMaintenancePolicyWeeklyMaintenanceWindowStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5fabc9ddfea1f0d00e0b514f22b42ee64c69de1ee76db8b3e0bb8fa4863daf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7167003366470f788ee56663ef8464887da4325473275313738de5e80e640a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9c8fd2c57cf37f34ee9910bc70e05e069e1335894d9037ae6a45c82356adff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6256eaf355de64832c057dc0835a0005e992b99cad452c5ac2baddf5d6be71d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820dc9dd3be51495182ad577e3bd59a5bce590f94837b834e6cfcf9cd4a01e3d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbfaa2c24a2cb1c0d673c4a24a2b4c5d4f6392d5e95134a8519a44c7b299f63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246ffdffa83f94ff4f4692a5bcaf6222292475d565bd022b9cd667dbc78ca51d(
    value: typing.Optional[RedisClusterMaintenanceSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f183743dbbafc18e16216b039c957df141e3884e7e655c68be89d9dfa1ef06e(
    *,
    backup: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a4e3a4556dd45c674d882bb43b1d1ccef940352c2f21df473c173e48e5df51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397c13e7f7bfb1b074428fff07edd22daab66eb7cfa613e4f0742f9fd50a41ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f2328691f83cbc836e7a1877a40fa95c6af8ff3cb0dee03ff22a9859dbe585(
    value: typing.Optional[RedisClusterManagedBackupSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd682a7820e108e0e326c9ae361227c08a7a334222b67fe4e5ca91b986d8bdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40dc27085abc40fc4d557d3751215b72083962dde1098dae3b3dd761a32997c1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223438f9318daa402c6f88073f07ee52d103740ac16c2b457be40dbbd36d501d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2005aac7543989764046db98d3e1bd19a54acad872d5d6e82aed0596f2097a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd3e4700a93bcfd3f8a7155e8d0cd3cc607b875114a00bc00e9c6530396c98c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebda0dcefed4762a1bbd8b325fbd6c377b47c5e49d932438dfc59298240d3e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eab89702b7bc2aca14fd18086e2923de6683219b0c53e03a1d0d307b66a4f1f(
    value: typing.Optional[RedisClusterManagedServerCaCaCerts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2081417d3de1bdde300ab97e82f73cab6bad4e186ddfef8c585783bae39b8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3bd1382c920c8c78152923b03be0468d09d5b3d9e31d411cd717ebae151288(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc392c99750e9a1bef687211ba8824739a1814cef1a969c37a9d974ecab6877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa8fbb6f30d5ee38003081e4d953993459d55bf99d2310239fca673af737971(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5c316b7c1576d1990aa6f0f2cfd22b0ed085138051a17d886eb6426409e59e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3946f7f23c01210c57ef8cc4e1d237dd7e87d07b8f1672fd996be01b9bd19651(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3089aac35c02f4915614c3033226915f9d971d0d11c987df82f503be31ae6216(
    value: typing.Optional[RedisClusterManagedServerCa],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c2962489f8142f3acf4901197fa015cc161fed42e984e3ab828dd92252de6f(
    *,
    aof_config: typing.Optional[typing.Union[RedisClusterPersistenceConfigAofConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    rdb_config: typing.Optional[typing.Union[RedisClusterPersistenceConfigRdbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e643344fe3ff0dda94af918e9eba991358a43854a9dfedf080c5400d2bd3d254(
    *,
    append_fsync: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f8ac7a77b480e22b39bf3770439df8bf085c88d64b16352e264a1a868cc7d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41d8e40781cfe9814884a67ff780d68ab3087f52185f4d085f7c9011d6403fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ddf2401927a659663d69d3c4196acd075980c7b305334b97dc589b6d8532f6(
    value: typing.Optional[RedisClusterPersistenceConfigAofConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c3e3371e068576b3cf06667921dcc7b1466dd8dd5031612c18d3f1f52be21b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef78f8dcab0c6ae6cb5295c7722335af85320ba862214cf6de4ef5eaab2963d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42141cc0c77b8a60aa77cf8325ed84f14da74ac3093cb44cd307ae3fe6612611(
    value: typing.Optional[RedisClusterPersistenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279942e90a3ca1209ec1f59fa14d88f968fc9042699307f41bf816412ae94bf0(
    *,
    rdb_snapshot_period: typing.Optional[builtins.str] = None,
    rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeac47f464e4d75b2c827c2b55f864965018d894cdfefd3f7e70bb16ac0466be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b336b32ca8200f29388b7ee072d052661ef8845fd5a4076a015313c25139de0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39faca7d5fcfa2dc233388483896510c102bcf288dda947b6d1277fe8d985a63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2f9c29c8d2ed4d0f9074da7758c2ce0404be084f6aa28897529aa8bf54e042(
    value: typing.Optional[RedisClusterPersistenceConfigRdbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de49c8bb81e1ab61bf816c864e73c59f5c0f21f65f596fa1ed7bea5cdd6d0c71(
    *,
    network: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28bd8546bbecca9dc227508b5a8968dd4bdddb38e543ad2ba7436a56762949f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a3a9e217e7261ab42e3c3213a8ae5b722ad56efd7f1bf4705ea932bab21b21(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd0066adb9838d0b98dcb69c9d229ecd4a1ea454d90c21c0d26f5e90aa0b164(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a551a3d9638c394b0f2396a29f0708ffec2cc3e41447b6c1459d15cfb50767(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b07c19b3d157a646b36de51ca2180b2295cf3016c0ac8d2d4b4e00961e27e01(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b32b4e78ab97c8179bc351f1483fa56a84d3de96f48640e55ff9b3dcaae5e11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisClusterPscConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25533c30151a514f02c022488bd80bb0ea67c0d88352739cdecd75ac1adfada0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cdbc8cd5608a4d79a84655ddf574645c6bbb33e01e37863d48836c2794e287c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81130e86d8dd540d74255597f1a57f244aecaa6239eefc1e735a104bfa2f448f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterPscConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e8d125741da761411e2073ed399236d0e4f7ee95e0869e066b3372dd74c370(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e948b3c1756a47a10e1009af4492ca7df50bacedbb47150490eb2bfcaf7af0f3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1d0f72b438c8454d605751ff7f14026242a206947a92a2e7d248f73754be96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b98e004e864dc759e70913f4ad70378bf752b6fef99c30c97fd5baecd25aaa9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5767c17d8145bdd3acb06cdf0bef838f33ddd1270d222a38946ba448bff473ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea872521602c5f18120ad90acc42e82abece9d937eea4fab9507665bfbf55e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0127d30b5784e397811cddf6af610013b3bcba84014d67476a3f619434d24bcc(
    value: typing.Optional[RedisClusterPscConnections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2573000eaff1e22f7a4605d6d95b985c7b032a628a3d787b1a0db07b9395befa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87d75b50ae4beb4ce41f591a88fda4ec5f1daa0fb63bd14f8776bd9dc179656(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10079e27900dec5882d1bd8d7b0ab12ffad11bca72417ded8ab14351610d205a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435a44d51c2e93e4e17106eb8fdb9b98508d1a3a69898214693e9ad5ad4ecc15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eecd2d61a64dcec93bce362aa9ceec29d674402503ec5e8674871615e6245e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9953b235af5dcf9ae79b81d4477083dfc80663aa7a674f34f7b33823ccda1f4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72379507c6e76ca8bff77097e11a64907b2245bd558e7f580e0316ebcd7f5fd0(
    value: typing.Optional[RedisClusterPscServiceAttachments],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7975f4ade1eb58f2fa29be95ac3ddc89279ead8b68da2163ae2b2779c35c33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6f983e674dfc8e2cd832c649186ea8d125877a056345dd9233064da1956d6c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874277045801d880e82865b8c6d412f1ac5dacbb46fbd36f803f8be44ba1ea62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d53aacaef2dc0ee09aca17d796cf7ecc29d45382c40b44f8076f80b31d5ef31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2952494cfd8cbddb3da519d56f0b003a05f89af969231ecefbe4892aa78683(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8527c4eb0d119afbc93f63c52a0471e4dbb18e18ae5e760db718deb07c80d137(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b51a764d65d60ea090f7dcaffa21f4da213a7e2188d5dd23ad460eead14dc59(
    value: typing.Optional[RedisClusterStateInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9209e41b9fc23291d05cfcb51583eb2da29ef5328d7407cbb492d300017daca0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a043918a195ce8d5aef941a11f98129705acbac8dde77211e87ac541dcf4d836(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7924605145a529c98f5f6089a90116dcba8f4f0963aa25cddfd8e30b350f4a65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b24938133ed0977510b30293cf6553a8657bc79ce92ddd0c3f861585c8070b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44685122ef6b642ac48a4ae8ae8fa1e34356bcb9cb889574fc6452e1fc872822(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7ed80f0c2bd6174b5b5132bb82f8a9ec696054cabe6164e66898ed76a872b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69857c1f0fcda05ac958300d203030c97e7ae719a27e39b793f799f20b3dacf(
    value: typing.Optional[RedisClusterStateInfoUpdateInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f7a96b542d0edf0cf08d04da3a1548eaeea01dc7de6309b9bb4a71f518a4ab(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__addc905d01e2ce1a9c204f30a844174e680b68fe4a2f06147564d3036f643d09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0231e15156fc1ba0698511d1a7e84358c7172e71996212a1dfd096f591d5d11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339c592a33b25e479bb76b0036006c4ad5864fd32726b04faa86bbbd1f1ee261(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c794bffe65180d5e07a60d6f9e0996dcb648368838ec8442fd8f57fdc4ae52c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51ced3d15e65b3f82a24e33b430cb111f323f534269e2c1c357e1360000e594(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721ae4062cdf34992370a344616853368db826fb221ebd33fc91c31ef0e7f492(
    *,
    mode: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9e0ab591d52d32fd748e68ae6701917d1ef326578b4c3d5c2fff593099218b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb080ca0a37ac745f608ec26a4f2f955d5a9c564fea498124b1951086bd2cac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73caadbfa4152468bfaa7e949f182e67113746b288e4d3de6d8127da1a972dc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe177aa560e6ddd8e04d980e64b3e581135e2a7afd75616b00c12ab831e306da(
    value: typing.Optional[RedisClusterZoneDistributionConfig],
) -> None:
    """Type checking stubs"""
    pass
