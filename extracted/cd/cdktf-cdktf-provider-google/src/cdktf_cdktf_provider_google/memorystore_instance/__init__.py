r'''
# `google_memorystore_instance`

Refer to the Terraform Registry for docs: [`google_memorystore_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance).
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


class MemorystoreInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance google_memorystore_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_id: builtins.str,
        location: builtins.str,
        shard_count: jsii.Number,
        authorization_mode: typing.Optional[builtins.str] = None,
        automated_backup_config: typing.Optional[typing.Union["MemorystoreInstanceAutomatedBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cross_instance_replication_config: typing.Optional[typing.Union["MemorystoreInstanceCrossInstanceReplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        desired_auto_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredAutoCreatedEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        desired_psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        gcs_source: typing.Optional[typing.Union["MemorystoreInstanceGcsSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_policy: typing.Optional[typing.Union["MemorystoreInstanceMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_backup_source: typing.Optional[typing.Union["MemorystoreInstanceManagedBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MemorystoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        zone_distribution_config: typing.Optional[typing.Union["MemorystoreInstanceZoneDistributionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance google_memorystore_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_id: Required. The ID to use for the instance, which will become the final component of the instance's resource name. This value is subject to the following restrictions: - Must be 4-63 characters in length - Must begin with a letter or digit - Must contain only lowercase letters, digits, and hyphens - Must not end with a hyphen - Must be unique within a location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#instance_id MemorystoreInstance#instance_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. See documentation for resource type 'memorystore.googleapis.com/CertificateAuthority'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#location MemorystoreInstance#location}
        :param shard_count: Required. Number of shards for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#shard_count MemorystoreInstance#shard_count}
        :param authorization_mode: Optional. Immutable. Authorization mode of the instance. Possible values: AUTH_DISABLED IAM_AUTH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#authorization_mode MemorystoreInstance#authorization_mode}
        :param automated_backup_config: automated_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#automated_backup_config MemorystoreInstance#automated_backup_config}
        :param cross_instance_replication_config: cross_instance_replication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#cross_instance_replication_config MemorystoreInstance#cross_instance_replication_config}
        :param deletion_protection_enabled: Optional. If set to true deletion of the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#deletion_protection_enabled MemorystoreInstance#deletion_protection_enabled}
        :param desired_auto_created_endpoints: desired_auto_created_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#desired_auto_created_endpoints MemorystoreInstance#desired_auto_created_endpoints}
        :param desired_psc_auto_connections: desired_psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#desired_psc_auto_connections MemorystoreInstance#desired_psc_auto_connections}
        :param engine_configs: Optional. User-provided engine configurations for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#engine_configs MemorystoreInstance#engine_configs}
        :param engine_version: Optional. Engine version of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#engine_version MemorystoreInstance#engine_version}
        :param gcs_source: gcs_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#gcs_source MemorystoreInstance#gcs_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#id MemorystoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key: The KMS key used to encrypt the at-rest data of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#kms_key MemorystoreInstance#kms_key}
        :param labels: Optional. Labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#labels MemorystoreInstance#labels}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#maintenance_policy MemorystoreInstance#maintenance_policy}
        :param managed_backup_source: managed_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#managed_backup_source MemorystoreInstance#managed_backup_source}
        :param mode: Optional. cluster or cluster-disabled. Possible values: CLUSTER CLUSTER_DISABLED Possible values: ["CLUSTER", "CLUSTER_DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param node_type: Optional. Machine type for individual nodes of the instance. Possible values: SHARED_CORE_NANO HIGHMEM_MEDIUM HIGHMEM_XLARGE STANDARD_SMALL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#node_type MemorystoreInstance#node_type}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#persistence_config MemorystoreInstance#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#project MemorystoreInstance#project}.
        :param replica_count: Optional. Number of replica nodes per shard. If omitted the default is 0 replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#replica_count MemorystoreInstance#replica_count}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#timeouts MemorystoreInstance#timeouts}
        :param transit_encryption_mode: Optional. Immutable. In-transit encryption mode of the instance. Possible values: TRANSIT_ENCRYPTION_DISABLED SERVER_AUTHENTICATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#transit_encryption_mode MemorystoreInstance#transit_encryption_mode}
        :param zone_distribution_config: zone_distribution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#zone_distribution_config MemorystoreInstance#zone_distribution_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2fb45bb8e1c847a4a17ca4c94c17a84d676c09dbde16423c0c0a689a1401a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MemorystoreInstanceConfig(
            instance_id=instance_id,
            location=location,
            shard_count=shard_count,
            authorization_mode=authorization_mode,
            automated_backup_config=automated_backup_config,
            cross_instance_replication_config=cross_instance_replication_config,
            deletion_protection_enabled=deletion_protection_enabled,
            desired_auto_created_endpoints=desired_auto_created_endpoints,
            desired_psc_auto_connections=desired_psc_auto_connections,
            engine_configs=engine_configs,
            engine_version=engine_version,
            gcs_source=gcs_source,
            id=id,
            kms_key=kms_key,
            labels=labels,
            maintenance_policy=maintenance_policy,
            managed_backup_source=managed_backup_source,
            mode=mode,
            node_type=node_type,
            persistence_config=persistence_config,
            project=project,
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
        '''Generates CDKTF code for importing a MemorystoreInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MemorystoreInstance to import.
        :param import_from_id: The id of the existing MemorystoreInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MemorystoreInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5999bf261933318d3928796bbc87858f3284b2b0856a80ba3908e3c78dcb6149)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutomatedBackupConfig")
    def put_automated_backup_config(
        self,
        *,
        fixed_frequency_schedule: typing.Union["MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule", typing.Dict[builtins.str, typing.Any]],
        retention: builtins.str,
    ) -> None:
        '''
        :param fixed_frequency_schedule: fixed_frequency_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#fixed_frequency_schedule MemorystoreInstance#fixed_frequency_schedule}
        :param retention: How long to keep automated backups before the backups are deleted. The value should be between 1 day and 365 days. If not specified, the default value is 35 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". The default_value is "3024000s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#retention MemorystoreInstance#retention}
        '''
        value = MemorystoreInstanceAutomatedBackupConfig(
            fixed_frequency_schedule=fixed_frequency_schedule, retention=retention
        )

        return typing.cast(None, jsii.invoke(self, "putAutomatedBackupConfig", [value]))

    @jsii.member(jsii_name="putCrossInstanceReplicationConfig")
    def put_cross_instance_replication_config(
        self,
        *,
        instance_role: typing.Optional[builtins.str] = None,
        primary_instance: typing.Optional[typing.Union["MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param instance_role: The instance role supports the following values: 1. 'INSTANCE_ROLE_UNSPECIFIED': This is an independent instance that has never participated in cross instance replication. It allows both reads and writes. 2. 'NONE': This is an independent instance that previously participated in cross instance replication(either as a 'PRIMARY' or 'SECONDARY' cluster). It allows both reads and writes. 3. 'PRIMARY': This instance serves as the replication source for secondary instance that are replicating from it. Any data written to it is automatically replicated to its secondary clusters. It allows both reads and writes. 4. 'SECONDARY': This instance replicates data from the primary instance. It allows only reads. Possible values: ["INSTANCE_ROLE_UNSPECIFIED", "NONE", "PRIMARY", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#instance_role MemorystoreInstance#instance_role}
        :param primary_instance: primary_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#primary_instance MemorystoreInstance#primary_instance}
        :param secondary_instances: secondary_instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#secondary_instances MemorystoreInstance#secondary_instances}
        '''
        value = MemorystoreInstanceCrossInstanceReplicationConfig(
            instance_role=instance_role,
            primary_instance=primary_instance,
            secondary_instances=secondary_instances,
        )

        return typing.cast(None, jsii.invoke(self, "putCrossInstanceReplicationConfig", [value]))

    @jsii.member(jsii_name="putDesiredAutoCreatedEndpoints")
    def put_desired_auto_created_endpoints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredAutoCreatedEndpoints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f4009209a626cdbbfd5b0a7d62a745bddcc82d5e80bc785bceca0db4fcb6c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDesiredAutoCreatedEndpoints", [value]))

    @jsii.member(jsii_name="putDesiredPscAutoConnections")
    def put_desired_psc_auto_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f8b3ca7a5c726269af10f8f3baa00f32352171a258c1c441fb545233681cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDesiredPscAutoConnections", [value]))

    @jsii.member(jsii_name="putGcsSource")
    def put_gcs_source(self, *, uris: typing.Sequence[builtins.str]) -> None:
        '''
        :param uris: URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#uris MemorystoreInstance#uris}
        '''
        value = MemorystoreInstanceGcsSource(uris=uris)

        return typing.cast(None, jsii.invoke(self, "putGcsSource", [value]))

    @jsii.member(jsii_name="putMaintenancePolicy")
    def put_maintenance_policy(
        self,
        *,
        weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#weekly_maintenance_window MemorystoreInstance#weekly_maintenance_window}
        '''
        value = MemorystoreInstanceMaintenancePolicy(
            weekly_maintenance_window=weekly_maintenance_window
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenancePolicy", [value]))

    @jsii.member(jsii_name="putManagedBackupSource")
    def put_managed_backup_source(self, *, backup: builtins.str) -> None:
        '''
        :param backup: Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#backup MemorystoreInstance#backup}
        '''
        value = MemorystoreInstanceManagedBackupSource(backup=backup)

        return typing.cast(None, jsii.invoke(self, "putManagedBackupSource", [value]))

    @jsii.member(jsii_name="putPersistenceConfig")
    def put_persistence_config(
        self,
        *,
        aof_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfigAofConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        rdb_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfigRdbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aof_config: aof_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#aof_config MemorystoreInstance#aof_config}
        :param mode: Optional. Current persistence mode. Possible values: DISABLED RDB AOF Possible values: ["DISABLED", "RDB", "AOF"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param rdb_config: rdb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#rdb_config MemorystoreInstance#rdb_config}
        '''
        value = MemorystoreInstancePersistenceConfig(
            aof_config=aof_config, mode=mode, rdb_config=rdb_config
        )

        return typing.cast(None, jsii.invoke(self, "putPersistenceConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#create MemorystoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#delete MemorystoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#update MemorystoreInstance#update}.
        '''
        value = MemorystoreInstanceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putZoneDistributionConfig")
    def put_zone_distribution_config(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Optional. Current zone distribution mode. Defaults to MULTI_ZONE. Possible values: MULTI_ZONE SINGLE_ZONE Possible values: ["MULTI_ZONE", "SINGLE_ZONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param zone: Optional. Defines zone where all resources will be allocated with SINGLE_ZONE mode. Ignored for MULTI_ZONE mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#zone MemorystoreInstance#zone}
        '''
        value = MemorystoreInstanceZoneDistributionConfig(mode=mode, zone=zone)

        return typing.cast(None, jsii.invoke(self, "putZoneDistributionConfig", [value]))

    @jsii.member(jsii_name="resetAuthorizationMode")
    def reset_authorization_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationMode", []))

    @jsii.member(jsii_name="resetAutomatedBackupConfig")
    def reset_automated_backup_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomatedBackupConfig", []))

    @jsii.member(jsii_name="resetCrossInstanceReplicationConfig")
    def reset_cross_instance_replication_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossInstanceReplicationConfig", []))

    @jsii.member(jsii_name="resetDeletionProtectionEnabled")
    def reset_deletion_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtectionEnabled", []))

    @jsii.member(jsii_name="resetDesiredAutoCreatedEndpoints")
    def reset_desired_auto_created_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredAutoCreatedEndpoints", []))

    @jsii.member(jsii_name="resetDesiredPscAutoConnections")
    def reset_desired_psc_auto_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredPscAutoConnections", []))

    @jsii.member(jsii_name="resetEngineConfigs")
    def reset_engine_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEngineConfigs", []))

    @jsii.member(jsii_name="resetEngineVersion")
    def reset_engine_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEngineVersion", []))

    @jsii.member(jsii_name="resetGcsSource")
    def reset_gcs_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsSource", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaintenancePolicy")
    def reset_maintenance_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenancePolicy", []))

    @jsii.member(jsii_name="resetManagedBackupSource")
    def reset_managed_backup_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedBackupSource", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetNodeType")
    def reset_node_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeType", []))

    @jsii.member(jsii_name="resetPersistenceConfig")
    def reset_persistence_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersistenceConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    ) -> "MemorystoreInstanceAutomatedBackupConfigOutputReference":
        return typing.cast("MemorystoreInstanceAutomatedBackupConfigOutputReference", jsii.get(self, "automatedBackupConfig"))

    @builtins.property
    @jsii.member(jsii_name="backupCollection")
    def backup_collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupCollection"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="crossInstanceReplicationConfig")
    def cross_instance_replication_config(
        self,
    ) -> "MemorystoreInstanceCrossInstanceReplicationConfigOutputReference":
        return typing.cast("MemorystoreInstanceCrossInstanceReplicationConfigOutputReference", jsii.get(self, "crossInstanceReplicationConfig"))

    @builtins.property
    @jsii.member(jsii_name="desiredAutoCreatedEndpoints")
    def desired_auto_created_endpoints(
        self,
    ) -> "MemorystoreInstanceDesiredAutoCreatedEndpointsList":
        return typing.cast("MemorystoreInstanceDesiredAutoCreatedEndpointsList", jsii.get(self, "desiredAutoCreatedEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="desiredPscAutoConnections")
    def desired_psc_auto_connections(
        self,
    ) -> "MemorystoreInstanceDesiredPscAutoConnectionsList":
        return typing.cast("MemorystoreInstanceDesiredPscAutoConnectionsList", jsii.get(self, "desiredPscAutoConnections"))

    @builtins.property
    @jsii.member(jsii_name="discoveryEndpoints")
    def discovery_endpoints(self) -> "MemorystoreInstanceDiscoveryEndpointsList":
        return typing.cast("MemorystoreInstanceDiscoveryEndpointsList", jsii.get(self, "discoveryEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> "MemorystoreInstanceEndpointsList":
        return typing.cast("MemorystoreInstanceEndpointsList", jsii.get(self, "endpoints"))

    @builtins.property
    @jsii.member(jsii_name="gcsSource")
    def gcs_source(self) -> "MemorystoreInstanceGcsSourceOutputReference":
        return typing.cast("MemorystoreInstanceGcsSourceOutputReference", jsii.get(self, "gcsSource"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicy")
    def maintenance_policy(
        self,
    ) -> "MemorystoreInstanceMaintenancePolicyOutputReference":
        return typing.cast("MemorystoreInstanceMaintenancePolicyOutputReference", jsii.get(self, "maintenancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceSchedule")
    def maintenance_schedule(self) -> "MemorystoreInstanceMaintenanceScheduleList":
        return typing.cast("MemorystoreInstanceMaintenanceScheduleList", jsii.get(self, "maintenanceSchedule"))

    @builtins.property
    @jsii.member(jsii_name="managedBackupSource")
    def managed_backup_source(
        self,
    ) -> "MemorystoreInstanceManagedBackupSourceOutputReference":
        return typing.cast("MemorystoreInstanceManagedBackupSourceOutputReference", jsii.get(self, "managedBackupSource"))

    @builtins.property
    @jsii.member(jsii_name="managedServerCa")
    def managed_server_ca(self) -> "MemorystoreInstanceManagedServerCaList":
        return typing.cast("MemorystoreInstanceManagedServerCaList", jsii.get(self, "managedServerCa"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "MemorystoreInstanceNodeConfigList":
        return typing.cast("MemorystoreInstanceNodeConfigList", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="persistenceConfig")
    def persistence_config(
        self,
    ) -> "MemorystoreInstancePersistenceConfigOutputReference":
        return typing.cast("MemorystoreInstancePersistenceConfigOutputReference", jsii.get(self, "persistenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="pscAttachmentDetails")
    def psc_attachment_details(self) -> "MemorystoreInstancePscAttachmentDetailsList":
        return typing.cast("MemorystoreInstancePscAttachmentDetailsList", jsii.get(self, "pscAttachmentDetails"))

    @builtins.property
    @jsii.member(jsii_name="pscAutoConnections")
    def psc_auto_connections(self) -> "MemorystoreInstancePscAutoConnectionsList":
        return typing.cast("MemorystoreInstancePscAutoConnectionsList", jsii.get(self, "pscAutoConnections"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateInfo")
    def state_info(self) -> "MemorystoreInstanceStateInfoList":
        return typing.cast("MemorystoreInstanceStateInfoList", jsii.get(self, "stateInfo"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MemorystoreInstanceTimeoutsOutputReference":
        return typing.cast("MemorystoreInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="zoneDistributionConfig")
    def zone_distribution_config(
        self,
    ) -> "MemorystoreInstanceZoneDistributionConfigOutputReference":
        return typing.cast("MemorystoreInstanceZoneDistributionConfigOutputReference", jsii.get(self, "zoneDistributionConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizationModeInput")
    def authorization_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="automatedBackupConfigInput")
    def automated_backup_config_input(
        self,
    ) -> typing.Optional["MemorystoreInstanceAutomatedBackupConfig"]:
        return typing.cast(typing.Optional["MemorystoreInstanceAutomatedBackupConfig"], jsii.get(self, "automatedBackupConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="crossInstanceReplicationConfigInput")
    def cross_instance_replication_config_input(
        self,
    ) -> typing.Optional["MemorystoreInstanceCrossInstanceReplicationConfig"]:
        return typing.cast(typing.Optional["MemorystoreInstanceCrossInstanceReplicationConfig"], jsii.get(self, "crossInstanceReplicationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionEnabledInput")
    def deletion_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredAutoCreatedEndpointsInput")
    def desired_auto_created_endpoints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredAutoCreatedEndpoints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredAutoCreatedEndpoints"]]], jsii.get(self, "desiredAutoCreatedEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredPscAutoConnectionsInput")
    def desired_psc_auto_connections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredPscAutoConnections"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredPscAutoConnections"]]], jsii.get(self, "desiredPscAutoConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="engineConfigsInput")
    def engine_configs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "engineConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="engineVersionInput")
    def engine_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsSourceInput")
    def gcs_source_input(self) -> typing.Optional["MemorystoreInstanceGcsSource"]:
        return typing.cast(typing.Optional["MemorystoreInstanceGcsSource"], jsii.get(self, "gcsSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

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
    @jsii.member(jsii_name="maintenancePolicyInput")
    def maintenance_policy_input(
        self,
    ) -> typing.Optional["MemorystoreInstanceMaintenancePolicy"]:
        return typing.cast(typing.Optional["MemorystoreInstanceMaintenancePolicy"], jsii.get(self, "maintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="managedBackupSourceInput")
    def managed_backup_source_input(
        self,
    ) -> typing.Optional["MemorystoreInstanceManagedBackupSource"]:
        return typing.cast(typing.Optional["MemorystoreInstanceManagedBackupSource"], jsii.get(self, "managedBackupSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeInput")
    def node_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="persistenceConfigInput")
    def persistence_config_input(
        self,
    ) -> typing.Optional["MemorystoreInstancePersistenceConfig"]:
        return typing.cast(typing.Optional["MemorystoreInstancePersistenceConfig"], jsii.get(self, "persistenceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MemorystoreInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MemorystoreInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionModeInput")
    def transit_encryption_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitEncryptionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneDistributionConfigInput")
    def zone_distribution_config_input(
        self,
    ) -> typing.Optional["MemorystoreInstanceZoneDistributionConfig"]:
        return typing.cast(typing.Optional["MemorystoreInstanceZoneDistributionConfig"], jsii.get(self, "zoneDistributionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationMode")
    def authorization_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationMode"))

    @authorization_mode.setter
    def authorization_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314163717def6def7427963860283520f9dae21947b9b85d7d11fb3da38fca6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ba6264442e0d3675fa984b8b6b73e92d785805cef96cf0a3e097b7e68ff6677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineConfigs")
    def engine_configs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "engineConfigs"))

    @engine_configs.setter
    def engine_configs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3709f2e023f297982b4d562e66862abda06d692dfbecb17dd4614b2db11dbee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineConfigs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5f7066f3cf0b7fed9af12493ee42a710453ed4048d245c452cb4d04027cc6bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbea60c334c216a49ce5e969a6de927630d8c5271ca623c55ba8b40afe7a92c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4253d7579842b6b9565cc68381fdcb973f54b9a506a8141692920f85289e8262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51aeb45248e2ba7925a013657285f5cc4a8bef4be1cab01c88a4fee2241754a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6030b8fd7c5d1d6d400509880ccfe5bc117c8168aa5bae4064d98e3adee2b668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19b2d8726834b58afc9f9651887c5dd44f463ffcbca9bfe3b616dcded38ec05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac46b8400839740879734134c86ef3aa4eaad4955c332b0e83e2c34d6fd7b614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9676613b4ff73e9197c5fba4306e8db26fc31a56a1241e4f06e8c88f10a198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4b97fab2d84a7e93d96ed1be06b4edf72ce55bc8c0a051c4fb31135dfac647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCount"))

    @replica_count.setter
    def replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608afdbc5e8b92a5d21cba1c94b90e60110b9f8bab447520a2c4260dc1f20d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shardCount")
    def shard_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shardCount"))

    @shard_count.setter
    def shard_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930a9d6aa4b5980cff31b999170c74a4ebcd4a96c4200cec381071f91a734648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shardCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionMode")
    def transit_encryption_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitEncryptionMode"))

    @transit_encryption_mode.setter
    def transit_encryption_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da65f8b6ec7ad35a3e5044080b42d086ef89128afead8dde501886ac59719e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitEncryptionMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceAutomatedBackupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "fixed_frequency_schedule": "fixedFrequencySchedule",
        "retention": "retention",
    },
)
class MemorystoreInstanceAutomatedBackupConfig:
    def __init__(
        self,
        *,
        fixed_frequency_schedule: typing.Union["MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule", typing.Dict[builtins.str, typing.Any]],
        retention: builtins.str,
    ) -> None:
        '''
        :param fixed_frequency_schedule: fixed_frequency_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#fixed_frequency_schedule MemorystoreInstance#fixed_frequency_schedule}
        :param retention: How long to keep automated backups before the backups are deleted. The value should be between 1 day and 365 days. If not specified, the default value is 35 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". The default_value is "3024000s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#retention MemorystoreInstance#retention}
        '''
        if isinstance(fixed_frequency_schedule, dict):
            fixed_frequency_schedule = MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule(**fixed_frequency_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5f89ea37f9ca07bc16e80f7569ff4a485fbce491256cacb50fd3f750f14bd8)
            check_type(argname="argument fixed_frequency_schedule", value=fixed_frequency_schedule, expected_type=type_hints["fixed_frequency_schedule"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fixed_frequency_schedule": fixed_frequency_schedule,
            "retention": retention,
        }

    @builtins.property
    def fixed_frequency_schedule(
        self,
    ) -> "MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule":
        '''fixed_frequency_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#fixed_frequency_schedule MemorystoreInstance#fixed_frequency_schedule}
        '''
        result = self._values.get("fixed_frequency_schedule")
        assert result is not None, "Required property 'fixed_frequency_schedule' is missing"
        return typing.cast("MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule", result)

    @builtins.property
    def retention(self) -> builtins.str:
        '''How long to keep automated backups before the backups are deleted.

        The value should be between 1 day and 365 days. If not specified, the default value is 35 days.
        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". The default_value is "3024000s"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#retention MemorystoreInstance#retention}
        '''
        result = self._values.get("retention")
        assert result is not None, "Required property 'retention' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceAutomatedBackupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule",
    jsii_struct_bases=[],
    name_mapping={"start_time": "startTime"},
)
class MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule:
    def __init__(
        self,
        *,
        start_time: typing.Union["MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#start_time MemorystoreInstance#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864aeb1a20493b57c05cf60f8e4de9ae2d218311b738106e34bc5ac70c5938a0)
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_time": start_time,
        }

    @builtins.property
    def start_time(
        self,
    ) -> "MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#start_time MemorystoreInstance#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__916c0081f1035f7c2c1ffb92b6e298ea6df4090a3e096cfe769cb71b5daa5ad0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(self, *, hours: jsii.Number) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#hours MemorystoreInstance#hours}
        '''
        value = MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime(
            hours=hours
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference":
        return typing.cast("MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime"]:
        return typing.cast(typing.Optional["MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule]:
        return typing.cast(typing.Optional[MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff5717e582b46b1dbbe2bd324c4750b9e66049ade3b45119fe3255ec8e01bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime",
    jsii_struct_bases=[],
    name_mapping={"hours": "hours"},
)
class MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime:
    def __init__(self, *, hours: jsii.Number) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#hours MemorystoreInstance#hours}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0913ec7042d3b4fb773d953757b7e761434f3f64757abe856f5e2669b93ed07f)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hours": hours,
        }

    @builtins.property
    def hours(self) -> jsii.Number:
        '''Hours of a day in 24 hour format.

        Must be greater than or equal to 0 and typically must be less than or equal to 23.
        An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#hours MemorystoreInstance#hours}
        '''
        result = self._values.get("hours")
        assert result is not None, "Required property 'hours' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c314b417b9f7d5e5dc7a727886094854ba1c8a1b9ed10f3ec810dca8e2d2cb2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0a9e11a25d01a75501d144fc9c41533cc62dc716fe3b419eec2df9380b9785c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime]:
        return typing.cast(typing.Optional[MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d3050590d17e9e2744b8fb1b8e1deb7b7bad3d9171d0059101af96fd9a7d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceAutomatedBackupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceAutomatedBackupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f750a4c81ffddbdcdd83f2bf577d9292a7662e62ca120798e8cc30217bef84d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFixedFrequencySchedule")
    def put_fixed_frequency_schedule(
        self,
        *,
        start_time: typing.Union[MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#start_time MemorystoreInstance#start_time}
        '''
        value = MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule(
            start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putFixedFrequencySchedule", [value]))

    @builtins.property
    @jsii.member(jsii_name="fixedFrequencySchedule")
    def fixed_frequency_schedule(
        self,
    ) -> MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleOutputReference:
        return typing.cast(MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleOutputReference, jsii.get(self, "fixedFrequencySchedule"))

    @builtins.property
    @jsii.member(jsii_name="fixedFrequencyScheduleInput")
    def fixed_frequency_schedule_input(
        self,
    ) -> typing.Optional[MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule]:
        return typing.cast(typing.Optional[MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule], jsii.get(self, "fixedFrequencyScheduleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__11f63c93406e490c2d73dba90069fba20b10b7d4237a3550e22ca82c1f6f243b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceAutomatedBackupConfig]:
        return typing.cast(typing.Optional[MemorystoreInstanceAutomatedBackupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceAutomatedBackupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12da0130765c7718dd205ed6db6a5f2c2d21c95bd70c51be67023da66c4149f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_id": "instanceId",
        "location": "location",
        "shard_count": "shardCount",
        "authorization_mode": "authorizationMode",
        "automated_backup_config": "automatedBackupConfig",
        "cross_instance_replication_config": "crossInstanceReplicationConfig",
        "deletion_protection_enabled": "deletionProtectionEnabled",
        "desired_auto_created_endpoints": "desiredAutoCreatedEndpoints",
        "desired_psc_auto_connections": "desiredPscAutoConnections",
        "engine_configs": "engineConfigs",
        "engine_version": "engineVersion",
        "gcs_source": "gcsSource",
        "id": "id",
        "kms_key": "kmsKey",
        "labels": "labels",
        "maintenance_policy": "maintenancePolicy",
        "managed_backup_source": "managedBackupSource",
        "mode": "mode",
        "node_type": "nodeType",
        "persistence_config": "persistenceConfig",
        "project": "project",
        "replica_count": "replicaCount",
        "timeouts": "timeouts",
        "transit_encryption_mode": "transitEncryptionMode",
        "zone_distribution_config": "zoneDistributionConfig",
    },
)
class MemorystoreInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_id: builtins.str,
        location: builtins.str,
        shard_count: jsii.Number,
        authorization_mode: typing.Optional[builtins.str] = None,
        automated_backup_config: typing.Optional[typing.Union[MemorystoreInstanceAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        cross_instance_replication_config: typing.Optional[typing.Union["MemorystoreInstanceCrossInstanceReplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        desired_auto_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredAutoCreatedEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        desired_psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceDesiredPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        gcs_source: typing.Optional[typing.Union["MemorystoreInstanceGcsSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_policy: typing.Optional[typing.Union["MemorystoreInstanceMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_backup_source: typing.Optional[typing.Union["MemorystoreInstanceManagedBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MemorystoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        zone_distribution_config: typing.Optional[typing.Union["MemorystoreInstanceZoneDistributionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_id: Required. The ID to use for the instance, which will become the final component of the instance's resource name. This value is subject to the following restrictions: - Must be 4-63 characters in length - Must begin with a letter or digit - Must contain only lowercase letters, digits, and hyphens - Must not end with a hyphen - Must be unique within a location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#instance_id MemorystoreInstance#instance_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. See documentation for resource type 'memorystore.googleapis.com/CertificateAuthority'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#location MemorystoreInstance#location}
        :param shard_count: Required. Number of shards for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#shard_count MemorystoreInstance#shard_count}
        :param authorization_mode: Optional. Immutable. Authorization mode of the instance. Possible values: AUTH_DISABLED IAM_AUTH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#authorization_mode MemorystoreInstance#authorization_mode}
        :param automated_backup_config: automated_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#automated_backup_config MemorystoreInstance#automated_backup_config}
        :param cross_instance_replication_config: cross_instance_replication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#cross_instance_replication_config MemorystoreInstance#cross_instance_replication_config}
        :param deletion_protection_enabled: Optional. If set to true deletion of the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#deletion_protection_enabled MemorystoreInstance#deletion_protection_enabled}
        :param desired_auto_created_endpoints: desired_auto_created_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#desired_auto_created_endpoints MemorystoreInstance#desired_auto_created_endpoints}
        :param desired_psc_auto_connections: desired_psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#desired_psc_auto_connections MemorystoreInstance#desired_psc_auto_connections}
        :param engine_configs: Optional. User-provided engine configurations for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#engine_configs MemorystoreInstance#engine_configs}
        :param engine_version: Optional. Engine version of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#engine_version MemorystoreInstance#engine_version}
        :param gcs_source: gcs_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#gcs_source MemorystoreInstance#gcs_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#id MemorystoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key: The KMS key used to encrypt the at-rest data of the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#kms_key MemorystoreInstance#kms_key}
        :param labels: Optional. Labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#labels MemorystoreInstance#labels}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#maintenance_policy MemorystoreInstance#maintenance_policy}
        :param managed_backup_source: managed_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#managed_backup_source MemorystoreInstance#managed_backup_source}
        :param mode: Optional. cluster or cluster-disabled. Possible values: CLUSTER CLUSTER_DISABLED Possible values: ["CLUSTER", "CLUSTER_DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param node_type: Optional. Machine type for individual nodes of the instance. Possible values: SHARED_CORE_NANO HIGHMEM_MEDIUM HIGHMEM_XLARGE STANDARD_SMALL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#node_type MemorystoreInstance#node_type}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#persistence_config MemorystoreInstance#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#project MemorystoreInstance#project}.
        :param replica_count: Optional. Number of replica nodes per shard. If omitted the default is 0 replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#replica_count MemorystoreInstance#replica_count}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#timeouts MemorystoreInstance#timeouts}
        :param transit_encryption_mode: Optional. Immutable. In-transit encryption mode of the instance. Possible values: TRANSIT_ENCRYPTION_DISABLED SERVER_AUTHENTICATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#transit_encryption_mode MemorystoreInstance#transit_encryption_mode}
        :param zone_distribution_config: zone_distribution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#zone_distribution_config MemorystoreInstance#zone_distribution_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(automated_backup_config, dict):
            automated_backup_config = MemorystoreInstanceAutomatedBackupConfig(**automated_backup_config)
        if isinstance(cross_instance_replication_config, dict):
            cross_instance_replication_config = MemorystoreInstanceCrossInstanceReplicationConfig(**cross_instance_replication_config)
        if isinstance(gcs_source, dict):
            gcs_source = MemorystoreInstanceGcsSource(**gcs_source)
        if isinstance(maintenance_policy, dict):
            maintenance_policy = MemorystoreInstanceMaintenancePolicy(**maintenance_policy)
        if isinstance(managed_backup_source, dict):
            managed_backup_source = MemorystoreInstanceManagedBackupSource(**managed_backup_source)
        if isinstance(persistence_config, dict):
            persistence_config = MemorystoreInstancePersistenceConfig(**persistence_config)
        if isinstance(timeouts, dict):
            timeouts = MemorystoreInstanceTimeouts(**timeouts)
        if isinstance(zone_distribution_config, dict):
            zone_distribution_config = MemorystoreInstanceZoneDistributionConfig(**zone_distribution_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de3252cb028a71fd621942b25263bfe393f97041bc2a312c902ff977d4131b2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument shard_count", value=shard_count, expected_type=type_hints["shard_count"])
            check_type(argname="argument authorization_mode", value=authorization_mode, expected_type=type_hints["authorization_mode"])
            check_type(argname="argument automated_backup_config", value=automated_backup_config, expected_type=type_hints["automated_backup_config"])
            check_type(argname="argument cross_instance_replication_config", value=cross_instance_replication_config, expected_type=type_hints["cross_instance_replication_config"])
            check_type(argname="argument deletion_protection_enabled", value=deletion_protection_enabled, expected_type=type_hints["deletion_protection_enabled"])
            check_type(argname="argument desired_auto_created_endpoints", value=desired_auto_created_endpoints, expected_type=type_hints["desired_auto_created_endpoints"])
            check_type(argname="argument desired_psc_auto_connections", value=desired_psc_auto_connections, expected_type=type_hints["desired_psc_auto_connections"])
            check_type(argname="argument engine_configs", value=engine_configs, expected_type=type_hints["engine_configs"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument gcs_source", value=gcs_source, expected_type=type_hints["gcs_source"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument maintenance_policy", value=maintenance_policy, expected_type=type_hints["maintenance_policy"])
            check_type(argname="argument managed_backup_source", value=managed_backup_source, expected_type=type_hints["managed_backup_source"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument persistence_config", value=persistence_config, expected_type=type_hints["persistence_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument replica_count", value=replica_count, expected_type=type_hints["replica_count"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument transit_encryption_mode", value=transit_encryption_mode, expected_type=type_hints["transit_encryption_mode"])
            check_type(argname="argument zone_distribution_config", value=zone_distribution_config, expected_type=type_hints["zone_distribution_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_id": instance_id,
            "location": location,
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
        if cross_instance_replication_config is not None:
            self._values["cross_instance_replication_config"] = cross_instance_replication_config
        if deletion_protection_enabled is not None:
            self._values["deletion_protection_enabled"] = deletion_protection_enabled
        if desired_auto_created_endpoints is not None:
            self._values["desired_auto_created_endpoints"] = desired_auto_created_endpoints
        if desired_psc_auto_connections is not None:
            self._values["desired_psc_auto_connections"] = desired_psc_auto_connections
        if engine_configs is not None:
            self._values["engine_configs"] = engine_configs
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if gcs_source is not None:
            self._values["gcs_source"] = gcs_source
        if id is not None:
            self._values["id"] = id
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if labels is not None:
            self._values["labels"] = labels
        if maintenance_policy is not None:
            self._values["maintenance_policy"] = maintenance_policy
        if managed_backup_source is not None:
            self._values["managed_backup_source"] = managed_backup_source
        if mode is not None:
            self._values["mode"] = mode
        if node_type is not None:
            self._values["node_type"] = node_type
        if persistence_config is not None:
            self._values["persistence_config"] = persistence_config
        if project is not None:
            self._values["project"] = project
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
    def instance_id(self) -> builtins.str:
        '''Required. The ID to use for the instance, which will become the final component of the instance's resource name.

        This value is subject to the following restrictions:

        - Must be 4-63 characters in length
        - Must begin with a letter or digit
        - Must contain only lowercase letters, digits, and hyphens
        - Must not end with a hyphen
        - Must be unique within a location

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#instance_id MemorystoreInstance#instance_id}
        '''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'.

        It identifies the resource within its parent collection as described in https://google.aip.dev/122. See documentation for resource type 'memorystore.googleapis.com/CertificateAuthority'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#location MemorystoreInstance#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shard_count(self) -> jsii.Number:
        '''Required. Number of shards for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#shard_count MemorystoreInstance#shard_count}
        '''
        result = self._values.get("shard_count")
        assert result is not None, "Required property 'shard_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def authorization_mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Immutable. Authorization mode of the instance. Possible values:  AUTH_DISABLED IAM_AUTH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#authorization_mode MemorystoreInstance#authorization_mode}
        '''
        result = self._values.get("authorization_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automated_backup_config(
        self,
    ) -> typing.Optional[MemorystoreInstanceAutomatedBackupConfig]:
        '''automated_backup_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#automated_backup_config MemorystoreInstance#automated_backup_config}
        '''
        result = self._values.get("automated_backup_config")
        return typing.cast(typing.Optional[MemorystoreInstanceAutomatedBackupConfig], result)

    @builtins.property
    def cross_instance_replication_config(
        self,
    ) -> typing.Optional["MemorystoreInstanceCrossInstanceReplicationConfig"]:
        '''cross_instance_replication_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#cross_instance_replication_config MemorystoreInstance#cross_instance_replication_config}
        '''
        result = self._values.get("cross_instance_replication_config")
        return typing.cast(typing.Optional["MemorystoreInstanceCrossInstanceReplicationConfig"], result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If set to true deletion of the instance will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#deletion_protection_enabled MemorystoreInstance#deletion_protection_enabled}
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def desired_auto_created_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredAutoCreatedEndpoints"]]]:
        '''desired_auto_created_endpoints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#desired_auto_created_endpoints MemorystoreInstance#desired_auto_created_endpoints}
        '''
        result = self._values.get("desired_auto_created_endpoints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredAutoCreatedEndpoints"]]], result)

    @builtins.property
    def desired_psc_auto_connections(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredPscAutoConnections"]]]:
        '''desired_psc_auto_connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#desired_psc_auto_connections MemorystoreInstance#desired_psc_auto_connections}
        '''
        result = self._values.get("desired_psc_auto_connections")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceDesiredPscAutoConnections"]]], result)

    @builtins.property
    def engine_configs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. User-provided engine configurations for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#engine_configs MemorystoreInstance#engine_configs}
        '''
        result = self._values.get("engine_configs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''Optional. Engine version of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#engine_version MemorystoreInstance#engine_version}
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcs_source(self) -> typing.Optional["MemorystoreInstanceGcsSource"]:
        '''gcs_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#gcs_source MemorystoreInstance#gcs_source}
        '''
        result = self._values.get("gcs_source")
        return typing.cast(typing.Optional["MemorystoreInstanceGcsSource"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#id MemorystoreInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The KMS key used to encrypt the at-rest data of the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#kms_key MemorystoreInstance#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Labels to represent user-provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#labels MemorystoreInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def maintenance_policy(
        self,
    ) -> typing.Optional["MemorystoreInstanceMaintenancePolicy"]:
        '''maintenance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#maintenance_policy MemorystoreInstance#maintenance_policy}
        '''
        result = self._values.get("maintenance_policy")
        return typing.cast(typing.Optional["MemorystoreInstanceMaintenancePolicy"], result)

    @builtins.property
    def managed_backup_source(
        self,
    ) -> typing.Optional["MemorystoreInstanceManagedBackupSource"]:
        '''managed_backup_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#managed_backup_source MemorystoreInstance#managed_backup_source}
        '''
        result = self._values.get("managed_backup_source")
        return typing.cast(typing.Optional["MemorystoreInstanceManagedBackupSource"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Optional. cluster or cluster-disabled.   Possible values:  CLUSTER  CLUSTER_DISABLED Possible values: ["CLUSTER", "CLUSTER_DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Machine type for individual nodes of the instance.   Possible values:  SHARED_CORE_NANO HIGHMEM_MEDIUM HIGHMEM_XLARGE STANDARD_SMALL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#node_type MemorystoreInstance#node_type}
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def persistence_config(
        self,
    ) -> typing.Optional["MemorystoreInstancePersistenceConfig"]:
        '''persistence_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#persistence_config MemorystoreInstance#persistence_config}
        '''
        result = self._values.get("persistence_config")
        return typing.cast(typing.Optional["MemorystoreInstancePersistenceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#project MemorystoreInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Optional. Number of replica nodes per shard. If omitted the default is 0 replicas.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#replica_count MemorystoreInstance#replica_count}
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MemorystoreInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#timeouts MemorystoreInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MemorystoreInstanceTimeouts"], result)

    @builtins.property
    def transit_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Immutable. In-transit encryption mode of the instance.   Possible values:  TRANSIT_ENCRYPTION_DISABLED SERVER_AUTHENTICATION.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#transit_encryption_mode MemorystoreInstance#transit_encryption_mode}
        '''
        result = self._values.get("transit_encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_distribution_config(
        self,
    ) -> typing.Optional["MemorystoreInstanceZoneDistributionConfig"]:
        '''zone_distribution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#zone_distribution_config MemorystoreInstance#zone_distribution_config}
        '''
        result = self._values.get("zone_distribution_config")
        return typing.cast(typing.Optional["MemorystoreInstanceZoneDistributionConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "instance_role": "instanceRole",
        "primary_instance": "primaryInstance",
        "secondary_instances": "secondaryInstances",
    },
)
class MemorystoreInstanceCrossInstanceReplicationConfig:
    def __init__(
        self,
        *,
        instance_role: typing.Optional[builtins.str] = None,
        primary_instance: typing.Optional[typing.Union["MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param instance_role: The instance role supports the following values: 1. 'INSTANCE_ROLE_UNSPECIFIED': This is an independent instance that has never participated in cross instance replication. It allows both reads and writes. 2. 'NONE': This is an independent instance that previously participated in cross instance replication(either as a 'PRIMARY' or 'SECONDARY' cluster). It allows both reads and writes. 3. 'PRIMARY': This instance serves as the replication source for secondary instance that are replicating from it. Any data written to it is automatically replicated to its secondary clusters. It allows both reads and writes. 4. 'SECONDARY': This instance replicates data from the primary instance. It allows only reads. Possible values: ["INSTANCE_ROLE_UNSPECIFIED", "NONE", "PRIMARY", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#instance_role MemorystoreInstance#instance_role}
        :param primary_instance: primary_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#primary_instance MemorystoreInstance#primary_instance}
        :param secondary_instances: secondary_instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#secondary_instances MemorystoreInstance#secondary_instances}
        '''
        if isinstance(primary_instance, dict):
            primary_instance = MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance(**primary_instance)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853faaead48f4ef26fbb4f70dc009a6f2fa10ec79880656c3976870390c0057b)
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument primary_instance", value=primary_instance, expected_type=type_hints["primary_instance"])
            check_type(argname="argument secondary_instances", value=secondary_instances, expected_type=type_hints["secondary_instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if primary_instance is not None:
            self._values["primary_instance"] = primary_instance
        if secondary_instances is not None:
            self._values["secondary_instances"] = secondary_instances

    @builtins.property
    def instance_role(self) -> typing.Optional[builtins.str]:
        '''The instance role supports the following values: 1.

        'INSTANCE_ROLE_UNSPECIFIED': This is an independent instance that has never participated in cross instance replication. It allows both reads and writes.
        2. 'NONE': This is an independent instance that previously participated in cross instance replication(either as a 'PRIMARY' or 'SECONDARY' cluster). It allows both reads and writes.
        3. 'PRIMARY': This instance serves as the replication source for secondary instance that are replicating from it. Any data written to it is automatically replicated to its secondary clusters. It allows both reads and writes.
        4. 'SECONDARY': This instance replicates data from the primary instance. It allows only reads. Possible values: ["INSTANCE_ROLE_UNSPECIFIED", "NONE", "PRIMARY", "SECONDARY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#instance_role MemorystoreInstance#instance_role}
        '''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_instance(
        self,
    ) -> typing.Optional["MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance"]:
        '''primary_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#primary_instance MemorystoreInstance#primary_instance}
        '''
        result = self._values.get("primary_instance")
        return typing.cast(typing.Optional["MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance"], result)

    @builtins.property
    def secondary_instances(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances"]]]:
        '''secondary_instances block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#secondary_instances MemorystoreInstance#secondary_instances}
        '''
        result = self._values.get("secondary_instances")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceCrossInstanceReplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigMembership",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceCrossInstanceReplicationConfigMembership:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceCrossInstanceReplicationConfigMembership(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceCrossInstanceReplicationConfigMembershipList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigMembershipList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f98975b928e0e1b7af8187777f46d62025604709a78a7976a4202078dade948e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceCrossInstanceReplicationConfigMembershipOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27df2ca09fe8c197d85fc70129fc7f3d22b8e900e3a7b2f28af60a03de2dea18)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceCrossInstanceReplicationConfigMembershipOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a4bbe6c5a37c628e9a835d2d679dd03401ee2183a80ce26bfac1117d0d3d5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07acf2089aee836b4e57a23a1fa789e7fa6ef96beffb07ba026f754906c1b4cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__221290afab6ef21c018f04bcb846d330ad584f99e40400a1e3ae99611b50a12a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceCrossInstanceReplicationConfigMembershipOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigMembershipOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b264427f7965665b9c3b3e5cf5633535f826e13bc9911ec16a53145e969ae241)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="primaryInstance")
    def primary_instance(
        self,
    ) -> "MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceList":
        return typing.cast("MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceList", jsii.get(self, "primaryInstance"))

    @builtins.property
    @jsii.member(jsii_name="secondaryInstance")
    def secondary_instance(
        self,
    ) -> "MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceList":
        return typing.cast("MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceList", jsii.get(self, "secondaryInstance"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembership]:
        return typing.cast(typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembership], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembership],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cccf76af579790e34ca956919047a1f2f409198a4062a52c61f6b8d1100e69f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f27c76cf1961fa4f844ae6bb7c4df53eedfcbfd53dd31c11719a4f21a373ea1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513a137f48038e6e93ee5abd8b481f36753e4ec097897bd688eb12d1beeae1be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac803fef3786f53ec373f2434d32e288386d68d9196fc64a328f900016171fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4366755ef6d595284c6ed4a2df8077923b1d7a4842a74afe4a3e61d1f9cbcd6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3929eb9b3e7a6457fef269cba49796c0f417abfa5a3b6f06453ee614c4dc85e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40b238769a9efa0f01257ecf88d211c4d69c74f9df6fd25cb860d0a9761eb3f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance]:
        return typing.cast(typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29781e2f947390467c4f6d3d19cbcd9d88ce51993231519ec47c3219b8c8ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__401dfcccf886c0791b9c6a70daa7bfad77c67acba370988b62b2b3aab7f73c41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40beccf1da40621d736cba5fa45eb5cb5180946e02c040cae9ab0cf805b95f48)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c29118d087a40c823628e92a998516499bc36ac48cd1ee7d7ea4bfcdc8cff3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e19a775ab2b48edb610b8b182bed7335f6500896a6ed77d7f31b53716846c90e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77f937263b6e7759aba42a81f9707cb9abfcf80686d2f3bf759eca59e64fad7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c7a5ce132a669827a2fd2a1c2a08378d67fc856a7c9808bd0590d9540544229)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance]:
        return typing.cast(typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bec252d7f1fd2b0a87ea90aeddaff45c57dfc2a6c236c333a81222c81295c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceCrossInstanceReplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b948293c9086e16b9c18eaced9c7b20c4b8579b9f543f335878cfb291565fd6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrimaryInstance")
    def put_primary_instance(
        self,
        *,
        instance: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance: The full resource path of the primary instance in the format: projects/{project}/locations/{region}/instances/{instance-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#instance MemorystoreInstance#instance}
        '''
        value = MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance(
            instance=instance
        )

        return typing.cast(None, jsii.invoke(self, "putPrimaryInstance", [value]))

    @jsii.member(jsii_name="putSecondaryInstances")
    def put_secondary_instances(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176cd83e6af6ffb272caf2c3fb22ed05db3947179e901d809bc4d8913d2f5e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecondaryInstances", [value]))

    @jsii.member(jsii_name="resetInstanceRole")
    def reset_instance_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceRole", []))

    @jsii.member(jsii_name="resetPrimaryInstance")
    def reset_primary_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryInstance", []))

    @jsii.member(jsii_name="resetSecondaryInstances")
    def reset_secondary_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryInstances", []))

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(
        self,
    ) -> MemorystoreInstanceCrossInstanceReplicationConfigMembershipList:
        return typing.cast(MemorystoreInstanceCrossInstanceReplicationConfigMembershipList, jsii.get(self, "membership"))

    @builtins.property
    @jsii.member(jsii_name="primaryInstance")
    def primary_instance(
        self,
    ) -> "MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstanceOutputReference":
        return typing.cast("MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstanceOutputReference", jsii.get(self, "primaryInstance"))

    @builtins.property
    @jsii.member(jsii_name="secondaryInstances")
    def secondary_instances(
        self,
    ) -> "MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesList":
        return typing.cast("MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesList", jsii.get(self, "secondaryInstances"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="instanceRoleInput")
    def instance_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryInstanceInput")
    def primary_instance_input(
        self,
    ) -> typing.Optional["MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance"]:
        return typing.cast(typing.Optional["MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance"], jsii.get(self, "primaryInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryInstancesInput")
    def secondary_instances_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances"]]], jsii.get(self, "secondaryInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceRole")
    def instance_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceRole"))

    @instance_role.setter
    def instance_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab5532764c6f5170bbffb137f37e0ed4866a3a9ac0a77b5f54ab288947093ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfig]:
        return typing.cast(typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e97eddd748daf879badd9d4a1273b275452f7a66a86507c8825d340f72d265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance",
    jsii_struct_bases=[],
    name_mapping={"instance": "instance"},
)
class MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance:
    def __init__(self, *, instance: typing.Optional[builtins.str] = None) -> None:
        '''
        :param instance: The full resource path of the primary instance in the format: projects/{project}/locations/{region}/instances/{instance-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#instance MemorystoreInstance#instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d377fae5c6a0c9762f727755ce9d211b5ee031c84af1a1f2ed7a1ccbf50141)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance is not None:
            self._values["instance"] = instance

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''The full resource path of the primary instance in the format: projects/{project}/locations/{region}/instances/{instance-id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#instance MemorystoreInstance#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__856116e806da7122cbb01d4e1c008490c686519eb19ce13d6078bbbf86151b35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstance")
    def reset_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstance", []))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c9ea09c6e7fbd832c005890a4cf3f5f6dc83290c7c3220d945ea410887afea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance]:
        return typing.cast(typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0afc56938fc7709efe5f6f3e954260a68b40126190f3be48d32ce2092d401a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances",
    jsii_struct_bases=[],
    name_mapping={"instance": "instance"},
)
class MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances:
    def __init__(self, *, instance: typing.Optional[builtins.str] = None) -> None:
        '''
        :param instance: The full resource path of the Nth instance in the format: projects/{project}/locations/{region}/instance/{instance-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#instance MemorystoreInstance#instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3aa051a57d67b220e81216be639aa1510684b82c307425435389f1847e10c7)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance is not None:
            self._values["instance"] = instance

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''The full resource path of the Nth instance in the format: projects/{project}/locations/{region}/instance/{instance-id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#instance MemorystoreInstance#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec985953cc255b131040e73897ca8e0bd7001ac2b9ea3becf15b86c16c4e5c40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207980592db4fc7519dc08db24e78858b2a42fe67123d3096b31c7ce7eebf49a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20acfaa988939e820bf6c8f3774784b4f46da7b72a1705c51ca559edd9dd183)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bb8465622bbd44e6c51bab2ed32fd11a3140bd8250a441012fdaa89f91261b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7a71564e71b348f8b6a3e738c8d8e5c93155026e81b5dd79bcef2c10a8ddd25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b514d9b8ee40341a405fd424090561447ba33e255764a2439e4474b94753e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b08d5bd470af15d73228962f2cb3c6907c9520419baa6eb5eaa37bbc7ca15bd5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInstance")
    def reset_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstance", []))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="instanceInput")
    def instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceInput"))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aaf3bdf6959f79330d4f20ff400124f2742a9a38be45dc06f6f7697274f80a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428f1fe142774980157577d6b4da5ed81cb921b8403d3d1d0f02c5cc6ab9f2e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDesiredAutoCreatedEndpoints",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "project_id": "projectId"},
)
class MemorystoreInstanceDesiredAutoCreatedEndpoints:
    def __init__(self, *, network: builtins.str, project_id: builtins.str) -> None:
        '''
        :param network: Required. The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#network MemorystoreInstance#network}
        :param project_id: Required. The consumer project_id where the forwarding rule is created from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#project_id MemorystoreInstance#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70cd5bcdc0811921b1042b3a05dd9e0a9f66ba221f76be1e78f97cc7ebe7776)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network": network,
            "project_id": project_id,
        }

    @builtins.property
    def network(self) -> builtins.str:
        '''Required. The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#network MemorystoreInstance#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Required. The consumer project_id where the forwarding rule is created from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#project_id MemorystoreInstance#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceDesiredAutoCreatedEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceDesiredAutoCreatedEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDesiredAutoCreatedEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8832ab285e6ec986d3bff0dc456024ee0e3789f53b93873e07d9f4a96edf5ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceDesiredAutoCreatedEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b404b1fcd9608c9325e01c93c00a43336debe9e206f019a7f54465a0fc98f0f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceDesiredAutoCreatedEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cea4ef9e5e35cd2cdd718e2c32f151ad8a74c283e1d998db5278fdb1a4d471)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8928f119ab875563ded1fd2d479a57b9a8e757c8b810672290fe4f67499f5bc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46c8cb54041e286ff579754a80161716033a02b1ede0a796ca94712b690527c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredAutoCreatedEndpoints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredAutoCreatedEndpoints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredAutoCreatedEndpoints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e419a2f7cec740139e8124e9702046740a099a958389556d1baed78fb77f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceDesiredAutoCreatedEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDesiredAutoCreatedEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b83058cee35a773f9936e1eabc1a4a5cc47f3796e4f40eb3f477a77321412187)
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
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a8147a69b1af46e6f58088d5a2e76c247ac089434971185dc817513394980c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5673d110cefc4b12094637445ebe4881b7b7b3f830f1e538cf4764a0667f46dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredAutoCreatedEndpoints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredAutoCreatedEndpoints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredAutoCreatedEndpoints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c58e70d6fc94f67616bbbf9a2a83c5076ca21d4b5b89ee46a5c5adf2369a0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDesiredPscAutoConnections",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "project_id": "projectId"},
)
class MemorystoreInstanceDesiredPscAutoConnections:
    def __init__(self, *, network: builtins.str, project_id: builtins.str) -> None:
        '''
        :param network: Required. The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#network MemorystoreInstance#network}
        :param project_id: Required. The consumer project_id where the forwarding rule is created from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#project_id MemorystoreInstance#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76db34ada6b358af4632b8cec3b794296d03488bdf8a6fb3ac955d2f5c08246e)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network": network,
            "project_id": project_id,
        }

    @builtins.property
    def network(self) -> builtins.str:
        '''Required. The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#network MemorystoreInstance#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Required. The consumer project_id where the forwarding rule is created from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#project_id MemorystoreInstance#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceDesiredPscAutoConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceDesiredPscAutoConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDesiredPscAutoConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5a5a75ff50325fba2758481f90765d870da191bd3af52eee6f94a98035dca62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceDesiredPscAutoConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50482b1aa741c93f4c6ec9ff8a290de853258a5ac40e479a554b3b79b1cd7e24)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceDesiredPscAutoConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa568015bcb6ccad30db9a1a550040fe52200208912fbd505efbd0d1f20b05d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b214daa5a189121307b9d45d1aeb027c7e1f4cd8dd1ac214c7428569fb9d69b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d83ee45ef1aca3818fc3ad0c4536451c3e9a01ac50fc6e88f9bc534f2f19f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredPscAutoConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredPscAutoConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredPscAutoConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d54229755f3398b74c9e12cd8c73d8b2d1bdb05dd7e9a1e739fd717058b1336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceDesiredPscAutoConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDesiredPscAutoConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7cd4cbebb36e6eca7e5816b1a852356264f90b6b49e20e43e8b748346482ce0)
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
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64a0ede266977ce99fa5acbe1777c0ee6082d7a95a5a3f8e087d6ed6b1e850d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ab0617e10e8cd10e3333cbc00d1f066c1689807413fbb348f32190fe724f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredPscAutoConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredPscAutoConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredPscAutoConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4476f1b5395acc9434ce8168c8dfad05119eca700f0d99ec7a06e9806caece42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDiscoveryEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceDiscoveryEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceDiscoveryEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceDiscoveryEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDiscoveryEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a07eec391684704b3b66f0aab3c60e54184f419c967e99afed83d9c386b97d04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceDiscoveryEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b3956559536c29e4ae6deb2fa6edfae137a486fc5f7aa7fd4f0f0ef6a34a1f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceDiscoveryEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee06425654db2d0ba270286ed5fd96229e17d5d47c7427d5aa694ddfa2750fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ee1b2745accf7ae8a05bc86617348257045e0d8c381598d4ae41cc261e07eb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd596310fbf52060c13c4c21d9512b7c84fa0a7d308414eb9df264b75196ea02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceDiscoveryEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceDiscoveryEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d5e410e24c343a5594a58338eda10e1d78c71fac87688106cd96352f0de65b5)
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
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceDiscoveryEndpoints]:
        return typing.cast(typing.Optional[MemorystoreInstanceDiscoveryEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceDiscoveryEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d145318fb59423f668a373fac1969d57653ef62847b28419a65aa101c14167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceEndpointsConnections",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceEndpointsConnections:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceEndpointsConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceEndpointsConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceEndpointsConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__569baab77087c50d4d9750c40430c851b604113da3e93b2f28159982ad67d1be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceEndpointsConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0d68d61cd79615108945830182999dc730e2b9829c210167236496cf4e1dd5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceEndpointsConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7855fb217573ad4f81412fcc02dd3ec8b2a62a177f6ae2f6d26987b7714de0a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60250598f6ce93761fcc471cc6d77f96d2a9a4fd1c7334d45bb40805132d5937)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b915031012f523b81a8aa1de07f85233baf10d4df57db6245d6dbd5fd999ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceEndpointsConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceEndpointsConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__caf95c7a373f156175302694b3510e33a3993391dd7bc4a189800966909aef68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pscAutoConnection")
    def psc_auto_connection(
        self,
    ) -> "MemorystoreInstanceEndpointsConnectionsPscAutoConnectionList":
        return typing.cast("MemorystoreInstanceEndpointsConnectionsPscAutoConnectionList", jsii.get(self, "pscAutoConnection"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceEndpointsConnections]:
        return typing.cast(typing.Optional[MemorystoreInstanceEndpointsConnections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceEndpointsConnections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42669e16c95220ae9cc7c3180129931d6caad4a772a52bde0d3b7edfeef6aa26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceEndpointsConnectionsPscAutoConnection",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceEndpointsConnectionsPscAutoConnection:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceEndpointsConnectionsPscAutoConnection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceEndpointsConnectionsPscAutoConnectionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceEndpointsConnectionsPscAutoConnectionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e37a803726ea95cd4df306775fba46807590d89982e1aca6a37de559457f1c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceEndpointsConnectionsPscAutoConnectionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0a432ff60e9e9b2660420600a0adce82966bf57cfae39e644ecc62e312568db)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceEndpointsConnectionsPscAutoConnectionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa7e25e27060548a4c08a808acfe79ec1c019715364a11dca3e3852259726c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae914ef00342d4dfa515773e7905da04c197e6639d22742c977f1c59221d002c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__706191fbfaf0a8098671290ca96d668a215ece67897cacf0e827ddd67cd90e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceEndpointsConnectionsPscAutoConnectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceEndpointsConnectionsPscAutoConnectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7f0171edb100f2162592badcc5040260e1eef5b9997c2ac4f4d2f1210e98935)
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
    @jsii.member(jsii_name="forwardingRule")
    def forwarding_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingRule"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionId")
    def psc_connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionId"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceEndpointsConnectionsPscAutoConnection]:
        return typing.cast(typing.Optional[MemorystoreInstanceEndpointsConnectionsPscAutoConnection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceEndpointsConnectionsPscAutoConnection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501de06dc6d0dcdde8a09fc18b1764ccff1bb58d793c0df2fc267b09a0864b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82eb0f7306c4471a6a45f87fd85261cc309a98298c4df0364b9e29baded20090)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MemorystoreInstanceEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8a6c0c5ca0b5dd4fdcab25678e76efe75b418398e836181dd187b501452b67)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c388225ac4a6f07b901aabae58f187d4f788b4b6c90fc67c43a30f8a38537d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__251798396ad6872d1090d84badf34e06f16c0a163819e6afb57bb60f9701f90d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1066825067f6d3dd6cf00f4ece5f54ee5257f0e9e31cab7de49bc2b74d5dc34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc759bb49e3eff1ff1d0bcde2609d4bd0acc2bcb464f10761d08b47070668056)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> MemorystoreInstanceEndpointsConnectionsList:
        return typing.cast(MemorystoreInstanceEndpointsConnectionsList, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceEndpoints]:
        return typing.cast(typing.Optional[MemorystoreInstanceEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__017d79ad179d19a3b9cd28efd6fb4cc6f8256b63cf6c3c2046b96e631cc7de18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceGcsSource",
    jsii_struct_bases=[],
    name_mapping={"uris": "uris"},
)
class MemorystoreInstanceGcsSource:
    def __init__(self, *, uris: typing.Sequence[builtins.str]) -> None:
        '''
        :param uris: URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#uris MemorystoreInstance#uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b749c4f7ba1b6cf572e7eb69b71583f33f518271bb9305139d877d37020f9a)
            check_type(argname="argument uris", value=uris, expected_type=type_hints["uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uris": uris,
        }

    @builtins.property
    def uris(self) -> typing.List[builtins.str]:
        '''URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#uris MemorystoreInstance#uris}
        '''
        result = self._values.get("uris")
        assert result is not None, "Required property 'uris' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceGcsSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceGcsSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceGcsSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1442d3635ea133caf1c71306bb92ebaa77b2c34249c7b638c504a15121b6262)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c7b283de9728a8eb4636885385e708d3c16c9ec1702f03e5cec424a467a1b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceGcsSource]:
        return typing.cast(typing.Optional[MemorystoreInstanceGcsSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceGcsSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeab0de4aa9287b59f676eca476d2158f3bd7a6860dfe6fcfe8b76ecc8ce6d00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceMaintenancePolicy",
    jsii_struct_bases=[],
    name_mapping={"weekly_maintenance_window": "weeklyMaintenanceWindow"},
)
class MemorystoreInstanceMaintenancePolicy:
    def __init__(
        self,
        *,
        weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#weekly_maintenance_window MemorystoreInstance#weekly_maintenance_window}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42103fc76fcee89e33455c0ca69698a7e3bab09897451b8ba0165de79e38a5c7)
            check_type(argname="argument weekly_maintenance_window", value=weekly_maintenance_window, expected_type=type_hints["weekly_maintenance_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if weekly_maintenance_window is not None:
            self._values["weekly_maintenance_window"] = weekly_maintenance_window

    @builtins.property
    def weekly_maintenance_window(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]]:
        '''weekly_maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#weekly_maintenance_window MemorystoreInstance#weekly_maintenance_window}
        '''
        result = self._values.get("weekly_maintenance_window")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceMaintenancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceMaintenancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceMaintenancePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab709311a80cc550686668f507afeb8aaf3048672f301c2f32c03b0e77b1f3be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWeeklyMaintenanceWindow")
    def put_weekly_maintenance_window(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d3470d922b6c2aa325a615b7d24fd81ac72d2512405ca2de9784359fcf5868)
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
    ) -> "MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowList":
        return typing.cast("MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowList", jsii.get(self, "weeklyMaintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="weeklyMaintenanceWindowInput")
    def weekly_maintenance_window_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]], jsii.get(self, "weeklyMaintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceMaintenancePolicy]:
        return typing.cast(typing.Optional[MemorystoreInstanceMaintenancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceMaintenancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a74af11704c460b6fb7747d281f08ba2188522f3f14a93d2996e56b8c162b3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "start_time": "startTime"},
)
class MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow:
    def __init__(
        self,
        *,
        day: builtins.str,
        start_time: typing.Union["MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day: The day of week that maintenance updates occur. - DAY_OF_WEEK_UNSPECIFIED: The day of the week is unspecified. - MONDAY: Monday - TUESDAY: Tuesday - WEDNESDAY: Wednesday - THURSDAY: Thursday - FRIDAY: Friday - SATURDAY: Saturday - SUNDAY: Sunday Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#day MemorystoreInstance#day}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#start_time MemorystoreInstance#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53dbed1c0ff4112f5d9cc7276efe98bcbafa15d0bbdbe3714e55f43893d840b0)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "start_time": start_time,
        }

    @builtins.property
    def day(self) -> builtins.str:
        '''The day of week that maintenance updates occur.

        - DAY_OF_WEEK_UNSPECIFIED: The day of the week is unspecified.
        - MONDAY: Monday
        - TUESDAY: Tuesday
        - WEDNESDAY: Wednesday
        - THURSDAY: Thursday
        - FRIDAY: Friday
        - SATURDAY: Saturday
        - SUNDAY: Sunday Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#day MemorystoreInstance#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(
        self,
    ) -> "MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#start_time MemorystoreInstance#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5232dbd241ef3219b697180983251e869ced82a0ac3df3ac3f9d01d1ec399130)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fc2b7d1adb884012ab8a68450c3966b56f13803629fb5d3f7e8a2d1f039e20a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514e6f5a20b5d988fc329540dc317af64e2f3f2aa59e93d554519bda38d0519b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aae6a7214a85b21ecc96967bb5bfe85d6413ad979c6915a310f284d0b82d6ff2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4529a082ab0ab910b326845d9c00e58325b1722e37de67caa476e373c422cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65585b1b4094d3d8ecda814e319eb1dd123dca831543c574736a9ae6797cdfc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcebdda875548409eb0211f622643289e5705e50ca9b23be88b15eb16793c7bf)
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
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#hours MemorystoreInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#minutes MemorystoreInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#nanos MemorystoreInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#seconds MemorystoreInstance#seconds}
        '''
        value = MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(
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
    ) -> "MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference":
        return typing.cast("MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime"]:
        return typing.cast(typing.Optional["MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a2024d4c592842d2570c47cd90edf888c7c257ba3f2d9c8657b26879f114ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f8f6aa987e28e18ab3e8e8a358ae07934147fe758859c8957a9d769165f0c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#hours MemorystoreInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#minutes MemorystoreInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#nanos MemorystoreInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#seconds MemorystoreInstance#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ed2aa4ac8f9e1070d576cd026bce68c49d268f4a07351d02da29e4659db6c7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#hours MemorystoreInstance#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#minutes MemorystoreInstance#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#nanos MemorystoreInstance#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time.

        Must normally be from 0 to 59.
        An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#seconds MemorystoreInstance#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f00b4bfe81a53fa825404ea8b911dcff4d40bbecd6d4d3083153e3ed4a67407)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9d4f5f5ecf5bd0af527c16e713cd2b0fe9a051a81393c1be418b7d096e8818d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9101f62fd4b5cacf1a71b50a5dc6787554633c4e953fa7d24ee9bb80c4dbcc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898e496052ec3efc4afdd6841a893ee33b2929d8d32a13049f684161e61a64d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bf226e42d0565dfbf549230fd4656b80d9d934fe55ce31cb43cbeb0832474c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime]:
        return typing.cast(typing.Optional[MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4fbd6062340bd83ea020d9dbf131ba1812f992bd9759e356e9301b5e217fbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceMaintenanceSchedule",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceMaintenanceSchedule:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceMaintenanceSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceMaintenanceScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceMaintenanceScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f5c81f5fcfb1f5d853e5a53e01fc5d7ba83777bd73b704daa87ee08eaf75ce6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceMaintenanceScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24db4982fab47f9ba6f69cfa6be71e125651e87338842762e1ba96cd09766365)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceMaintenanceScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df924542b576ecb47d80c0b0995c5e1646ca280ffd88626b97ea6a871432762)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2df8b67bb6d2a7b2ab3d2d74fe09e25daaff05082d13c3fb78e306b60f78a66a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b12443fbf40727a74cc5e90aa5705d36eb9f8c8c04bc4859d912cdd1a21754f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceMaintenanceScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceMaintenanceScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0302f435959574247dab30bca18db06d49367737314e3d9632c3da7556c81a09)
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
    def internal_value(self) -> typing.Optional[MemorystoreInstanceMaintenanceSchedule]:
        return typing.cast(typing.Optional[MemorystoreInstanceMaintenanceSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceMaintenanceSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b604673f659d5a5a92776881f3552364553ae6d35d717107049f16f170944e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceManagedBackupSource",
    jsii_struct_bases=[],
    name_mapping={"backup": "backup"},
)
class MemorystoreInstanceManagedBackupSource:
    def __init__(self, *, backup: builtins.str) -> None:
        '''
        :param backup: Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#backup MemorystoreInstance#backup}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa4cda62d6205ac9b3e26d23c6a61453ab37d6e7745576c8cd274d9a2045153)
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup": backup,
        }

    @builtins.property
    def backup(self) -> builtins.str:
        '''Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#backup MemorystoreInstance#backup}
        '''
        result = self._values.get("backup")
        assert result is not None, "Required property 'backup' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceManagedBackupSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceManagedBackupSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceManagedBackupSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9aeaf37c80cc34f9d00eb6d63c22347b96c395d1e077f2df5cccaf0c5d721a77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__378f92fd7f8cd452d16fed40144a0d80447dc5aa7824b282fb9cb57283ba82d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceManagedBackupSource]:
        return typing.cast(typing.Optional[MemorystoreInstanceManagedBackupSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceManagedBackupSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6e3ec255958c5f8ec8fd68161fafb46fbc3bb608f3a627680da4501122921f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceManagedServerCa",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceManagedServerCa:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceManagedServerCa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceManagedServerCaCaCerts",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceManagedServerCaCaCerts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceManagedServerCaCaCerts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceManagedServerCaCaCertsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceManagedServerCaCaCertsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b289ab67ef53a1846e793bc2a70f9b30fcf38525849dfacbc8fc3db5288d5b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceManagedServerCaCaCertsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5102f612867cbb963ee9f3018d465371e3449cdf1c9812c881e0cea49b0e1263)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceManagedServerCaCaCertsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1932246cde019f28f1a882e800c3dec9c09f30512dda9d03f957b82bf0c8617d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dfebb4f1b1fbca6a9280644e82af4ecfe5ab7be16fbcf9b586d3459975fe81e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23a983d05a4a63c4a07b5b89e905c3e8ddbd19c921a2fdfe6db42908c9dde18d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceManagedServerCaCaCertsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceManagedServerCaCaCertsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff387257281919e9543b84a6b78a49ce537ef974b634a10706804fce51a6d9c1)
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
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceManagedServerCaCaCerts]:
        return typing.cast(typing.Optional[MemorystoreInstanceManagedServerCaCaCerts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceManagedServerCaCaCerts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a14b0f075b7af7547b90623e19a5379bd83754900010da0f4ff9433e6f8d3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceManagedServerCaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceManagedServerCaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81b6b09025c93de591b1c8cd4eafd7d38c910df04955b43467fc236283bb335a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceManagedServerCaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105f9eb15b52253eaa4e10f6b9778b4ea6dadf494e9e79fc90b3a3b2637282d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceManagedServerCaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1166112a50fa615f7b6c13c3c9e85725a158155c31798b5db8f3e0683afa9dac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f1bf1309feecc1de50f057e139c4b7092aed4ed579724d478529d353a3c35fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__452139d50a6336a76ebc7925171d1359ff196838677de9f3d51a36db062a0fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceManagedServerCaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceManagedServerCaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08c48ec83613d63d2c493f8fdda09e07db093141e10006d0f1d5f8b5649326e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="caCerts")
    def ca_certs(self) -> MemorystoreInstanceManagedServerCaCaCertsList:
        return typing.cast(MemorystoreInstanceManagedServerCaCaCertsList, jsii.get(self, "caCerts"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceManagedServerCa]:
        return typing.cast(typing.Optional[MemorystoreInstanceManagedServerCa], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceManagedServerCa],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b205d155875aee81e9e5ce378083cbaab64b381027796dfa0dc6fa32eb7fdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceNodeConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceNodeConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceNodeConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceNodeConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b235a65d0ecfb283379eb19478d9ef9973f101b5e48e22608f66837fbf88e44d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MemorystoreInstanceNodeConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62fa3b688059a73d27cac7f8e488153ce08048e920c26898f4a1436fa406290)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceNodeConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f55f8334e7f6f94db59a7a9178782aa045b89a0679aecf63e63265f80351734d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a945acd2b62c9d2ab7809aa8f7bee21049a5dd42d7e3365151b87991cc271a7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c0b1a1a58df9b749b3b879bedef3c32e92cbe7845d9001583f5862431a271b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb6d37e39e2583c013ea71c4d94f8630ec51f93ee1d01dd4154ab2319e85b38d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="sizeGb")
    def size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGb"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceNodeConfig]:
        return typing.cast(typing.Optional[MemorystoreInstanceNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752f3f0e9ad4955b683394cc173a47f938a89f7142fee4d4fa3d91c35d783aad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aof_config": "aofConfig",
        "mode": "mode",
        "rdb_config": "rdbConfig",
    },
)
class MemorystoreInstancePersistenceConfig:
    def __init__(
        self,
        *,
        aof_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfigAofConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        rdb_config: typing.Optional[typing.Union["MemorystoreInstancePersistenceConfigRdbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aof_config: aof_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#aof_config MemorystoreInstance#aof_config}
        :param mode: Optional. Current persistence mode. Possible values: DISABLED RDB AOF Possible values: ["DISABLED", "RDB", "AOF"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param rdb_config: rdb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#rdb_config MemorystoreInstance#rdb_config}
        '''
        if isinstance(aof_config, dict):
            aof_config = MemorystoreInstancePersistenceConfigAofConfig(**aof_config)
        if isinstance(rdb_config, dict):
            rdb_config = MemorystoreInstancePersistenceConfigRdbConfig(**rdb_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9414844fbf7265eb139df17a1a5d3d7ffb5ea373cae0c371773ba8f2a189e147)
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
    ) -> typing.Optional["MemorystoreInstancePersistenceConfigAofConfig"]:
        '''aof_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#aof_config MemorystoreInstance#aof_config}
        '''
        result = self._values.get("aof_config")
        return typing.cast(typing.Optional["MemorystoreInstancePersistenceConfigAofConfig"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Current persistence mode.   Possible values: DISABLED RDB AOF Possible values: ["DISABLED", "RDB", "AOF"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_config(
        self,
    ) -> typing.Optional["MemorystoreInstancePersistenceConfigRdbConfig"]:
        '''rdb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#rdb_config MemorystoreInstance#rdb_config}
        '''
        result = self._values.get("rdb_config")
        return typing.cast(typing.Optional["MemorystoreInstancePersistenceConfigRdbConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstancePersistenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfigAofConfig",
    jsii_struct_bases=[],
    name_mapping={"append_fsync": "appendFsync"},
)
class MemorystoreInstancePersistenceConfigAofConfig:
    def __init__(self, *, append_fsync: typing.Optional[builtins.str] = None) -> None:
        '''
        :param append_fsync: Optional. The fsync mode. Possible values: NEVER EVERY_SEC ALWAYS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#append_fsync MemorystoreInstance#append_fsync}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b54e3ca144d7d6c06914605ba866043ec9bcd168b3ba038f7788a3f7b84ef38)
            check_type(argname="argument append_fsync", value=append_fsync, expected_type=type_hints["append_fsync"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if append_fsync is not None:
            self._values["append_fsync"] = append_fsync

    @builtins.property
    def append_fsync(self) -> typing.Optional[builtins.str]:
        '''Optional. The fsync mode.   Possible values:  NEVER EVERY_SEC ALWAYS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#append_fsync MemorystoreInstance#append_fsync}
        '''
        result = self._values.get("append_fsync")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstancePersistenceConfigAofConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstancePersistenceConfigAofConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfigAofConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__068bcc0536a632e29160ddf193998f8e244e48fb374dd2695a06f75e6a3da6d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d13b73b72c6d179fdf76e26fefbe2c0a45ab792e67503cac5061502ef3ebb613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appendFsync", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstancePersistenceConfigAofConfig]:
        return typing.cast(typing.Optional[MemorystoreInstancePersistenceConfigAofConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstancePersistenceConfigAofConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d62526aa04f462a8bf8dca0cad341a17c28c0275158d3985797a3361c3c79bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstancePersistenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3ec9221129d2c0e7ba383cd2ae710eedcb54b2aad4aa70a2bec769a45d579c5)
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
        :param append_fsync: Optional. The fsync mode. Possible values: NEVER EVERY_SEC ALWAYS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#append_fsync MemorystoreInstance#append_fsync}
        '''
        value = MemorystoreInstancePersistenceConfigAofConfig(
            append_fsync=append_fsync
        )

        return typing.cast(None, jsii.invoke(self, "putAofConfig", [value]))

    @jsii.member(jsii_name="putRdbConfig")
    def put_rdb_config(
        self,
        *,
        rdb_snapshot_period: typing.Optional[builtins.str] = None,
        rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rdb_snapshot_period: Optional. Period between RDB snapshots. Possible values: ONE_HOUR SIX_HOURS TWELVE_HOURS TWENTY_FOUR_HOURS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#rdb_snapshot_period MemorystoreInstance#rdb_snapshot_period}
        :param rdb_snapshot_start_time: Optional. Time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#rdb_snapshot_start_time MemorystoreInstance#rdb_snapshot_start_time}
        '''
        value = MemorystoreInstancePersistenceConfigRdbConfig(
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
    def aof_config(
        self,
    ) -> MemorystoreInstancePersistenceConfigAofConfigOutputReference:
        return typing.cast(MemorystoreInstancePersistenceConfigAofConfigOutputReference, jsii.get(self, "aofConfig"))

    @builtins.property
    @jsii.member(jsii_name="rdbConfig")
    def rdb_config(
        self,
    ) -> "MemorystoreInstancePersistenceConfigRdbConfigOutputReference":
        return typing.cast("MemorystoreInstancePersistenceConfigRdbConfigOutputReference", jsii.get(self, "rdbConfig"))

    @builtins.property
    @jsii.member(jsii_name="aofConfigInput")
    def aof_config_input(
        self,
    ) -> typing.Optional[MemorystoreInstancePersistenceConfigAofConfig]:
        return typing.cast(typing.Optional[MemorystoreInstancePersistenceConfigAofConfig], jsii.get(self, "aofConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbConfigInput")
    def rdb_config_input(
        self,
    ) -> typing.Optional["MemorystoreInstancePersistenceConfigRdbConfig"]:
        return typing.cast(typing.Optional["MemorystoreInstancePersistenceConfigRdbConfig"], jsii.get(self, "rdbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f6c3070e821d5b4e6415ff5b5f1ef1da16a827567e7b1db51088088d8ed32e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstancePersistenceConfig]:
        return typing.cast(typing.Optional[MemorystoreInstancePersistenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstancePersistenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81c6253caed7197ff8b4d7f5de291b29f642a5d8831b19f2acc190bf0e52171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfigRdbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "rdb_snapshot_period": "rdbSnapshotPeriod",
        "rdb_snapshot_start_time": "rdbSnapshotStartTime",
    },
)
class MemorystoreInstancePersistenceConfigRdbConfig:
    def __init__(
        self,
        *,
        rdb_snapshot_period: typing.Optional[builtins.str] = None,
        rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rdb_snapshot_period: Optional. Period between RDB snapshots. Possible values: ONE_HOUR SIX_HOURS TWELVE_HOURS TWENTY_FOUR_HOURS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#rdb_snapshot_period MemorystoreInstance#rdb_snapshot_period}
        :param rdb_snapshot_start_time: Optional. Time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#rdb_snapshot_start_time MemorystoreInstance#rdb_snapshot_start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7db1332c63344ecd106396a78ef3aca1c1d1aa37a8f2a6679c26a5287e60c1b)
            check_type(argname="argument rdb_snapshot_period", value=rdb_snapshot_period, expected_type=type_hints["rdb_snapshot_period"])
            check_type(argname="argument rdb_snapshot_start_time", value=rdb_snapshot_start_time, expected_type=type_hints["rdb_snapshot_start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rdb_snapshot_period is not None:
            self._values["rdb_snapshot_period"] = rdb_snapshot_period
        if rdb_snapshot_start_time is not None:
            self._values["rdb_snapshot_start_time"] = rdb_snapshot_start_time

    @builtins.property
    def rdb_snapshot_period(self) -> typing.Optional[builtins.str]:
        '''Optional. Period between RDB snapshots.   Possible values:  ONE_HOUR SIX_HOURS TWELVE_HOURS TWENTY_FOUR_HOURS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#rdb_snapshot_period MemorystoreInstance#rdb_snapshot_period}
        '''
        result = self._values.get("rdb_snapshot_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_snapshot_start_time(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Time that the first snapshot was/will be attempted, and to which future
        snapshots will be aligned. If not provided, the current time will be
        used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#rdb_snapshot_start_time MemorystoreInstance#rdb_snapshot_start_time}
        '''
        result = self._values.get("rdb_snapshot_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstancePersistenceConfigRdbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstancePersistenceConfigRdbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePersistenceConfigRdbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9bb3725df1ccc4e463860ffdf14983714ebeb0604837eb6c38ec7243a0e2887)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88283cf8512976da15737eb287396b0a0b16aca2c62c04b3ce03fa22f8fc93b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotStartTime")
    def rdb_snapshot_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdbSnapshotStartTime"))

    @rdb_snapshot_start_time.setter
    def rdb_snapshot_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f8bb3176258d4d065ebc6cba1cf00280508244b266a94bff2591ae1edc9fea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstancePersistenceConfigRdbConfig]:
        return typing.cast(typing.Optional[MemorystoreInstancePersistenceConfigRdbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstancePersistenceConfigRdbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be216345b93f500c49669530fd7df3e06fb462779ce4748e1ed58273112abfe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePscAttachmentDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstancePscAttachmentDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstancePscAttachmentDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstancePscAttachmentDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePscAttachmentDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1906cf45a64d15daf4c1df560afe990418f06f31ec52be5908b06b2fa7b5b51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstancePscAttachmentDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0aeb689214ec55f698c1ebc4bcb43a216424edaea64e32089e27277913c4885)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstancePscAttachmentDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8696134f06feb90b9b13e458178a5c6e55b50245dca74644ee551035d23a2c18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__713172f205358d039984c64b900299d20cf425868cd9edfd5b3144f09c42ea59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__463b2532d5fadb043854db80169eb6ecf1f8940520f9703ef80eb51d9469c93e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstancePscAttachmentDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePscAttachmentDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ac332815f1e1b3ce887799aca1dda9a999803bee7692c50c70ac5baad68a554)
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
    ) -> typing.Optional[MemorystoreInstancePscAttachmentDetails]:
        return typing.cast(typing.Optional[MemorystoreInstancePscAttachmentDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstancePscAttachmentDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa037ebf09f0633a4f1669b351df2b3fa6caddb9f9d2f9d3e487606ce2040857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePscAutoConnections",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstancePscAutoConnections:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstancePscAutoConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstancePscAutoConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePscAutoConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36b6b230a2494df4f2c3dfb4a94c4036acf58d4593978cf67999c82d05563996)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstancePscAutoConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e726538e2ca4ec0285ca02774cf4d4cf09602cd9530dc34e917fefc3bc7bb9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstancePscAutoConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2a1beefb527f323ce88fa135d54bf6100d0096f8dffa0d59df6afcfd03d970)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34347ebd5ea54b15bcd1da860c0915eb3415ccf4ee16d94d1785d28d9c5c32ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fccef096778a353341a88796f2b143979f10d8e608342b2d7f0af478033b9a2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstancePscAutoConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstancePscAutoConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7544ccf3b7409b50fb57ef537ca9506bf1c1cf4577fefc4f32b78ff94c074cf7)
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
    @jsii.member(jsii_name="forwardingRule")
    def forwarding_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardingRule"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionId")
    def psc_connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionId"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionStatus")
    def psc_connection_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionStatus"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstancePscAutoConnections]:
        return typing.cast(typing.Optional[MemorystoreInstancePscAutoConnections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstancePscAutoConnections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f995bbb332727706b9f077f3f2f4ef24769e21744182f7abbe4601951841cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceStateInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceStateInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceStateInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf660e4341e02329e199f83f60f3155acb64e2333f4dc45d98dafdd2bd05c1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MemorystoreInstanceStateInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8bd93d3c424fdf868151c1bb65f03ae31f3737851cf6a4059dc5e8e9922fc6d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceStateInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99a564e1a8e87c84ae384e0a03e4847e007f98d33a5a2e9efb1d90c758784e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5c41a8d4a08552be15f9fc8acb6e54d2c288b0ffb23dcd844c41612d4b269de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f84f2340d4339a960e65282a66c9d68e974c12dffb5bbe960a23e002357d3bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceStateInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f822742e887f4501b90646bff3dc2aca400aa1ffd3cc161069973a2be09f1ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="updateInfo")
    def update_info(self) -> "MemorystoreInstanceStateInfoUpdateInfoList":
        return typing.cast("MemorystoreInstanceStateInfoUpdateInfoList", jsii.get(self, "updateInfo"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemorystoreInstanceStateInfo]:
        return typing.cast(typing.Optional[MemorystoreInstanceStateInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceStateInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abd473b792faf2bfe074cf766ea539e701b0aff462a84f3b4c1c30b758e9cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfoUpdateInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemorystoreInstanceStateInfoUpdateInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceStateInfoUpdateInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceStateInfoUpdateInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfoUpdateInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca39fd862fa28c6771459e17324d473da43531c2b9436d404a4555524b48b5a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemorystoreInstanceStateInfoUpdateInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e49b627d0cf8f14c187e5ba9ff6a7a7f76b0fa9193d09d80cd78b9e57aa9e9b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemorystoreInstanceStateInfoUpdateInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f0853a7dafcffa99a6014e18ce7be7aca09305a5b48abfd7254af38d0915b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aac8d57ab93b9d3ab1d81ac9ad9fdd1632d49c804ab31c88809ed06beca3119d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0eb5e69ba11c33245e7f77d2218f93bbcda38423b71ab2345ebb2adc0b518963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemorystoreInstanceStateInfoUpdateInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceStateInfoUpdateInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40a3f94882bcc5f02bde866a481184eba294c2603c21dde2dabf0e137e61deec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="targetEngineVersion")
    def target_engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetEngineVersion"))

    @builtins.property
    @jsii.member(jsii_name="targetNodeType")
    def target_node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetNodeType"))

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
    def internal_value(self) -> typing.Optional[MemorystoreInstanceStateInfoUpdateInfo]:
        return typing.cast(typing.Optional[MemorystoreInstanceStateInfoUpdateInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceStateInfoUpdateInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a00f36a1febe806df0db7387da82f08da8a6c076925a25fda22af9b6eec6b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MemorystoreInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#create MemorystoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#delete MemorystoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#update MemorystoreInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34020f411c6a81ce19b1c60b8ddb0a35402efaae888d8996711dca20e6ed4fb4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#create MemorystoreInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#delete MemorystoreInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#update MemorystoreInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe659aaad8eca5a2bb17a8884e69bcfb527a96fb3b4426d0f0bd96d88b59302f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbd9dcde0564f5e6551552c74551cb673b193e3808880599708a09e972d98888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e0356560862ed62e131874219761f2b55f43a3f39629e59e878962171dbc83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9bd1c782bdc0caaf80fdd05553eb206f6ca983603a7b7a5cab9bcab143f79b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ad08ac4ae77cb7e45d30ba85a49c2dd55fdedc9327d470c418abd273312d90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceZoneDistributionConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "zone": "zone"},
)
class MemorystoreInstanceZoneDistributionConfig:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Optional. Current zone distribution mode. Defaults to MULTI_ZONE. Possible values: MULTI_ZONE SINGLE_ZONE Possible values: ["MULTI_ZONE", "SINGLE_ZONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        :param zone: Optional. Defines zone where all resources will be allocated with SINGLE_ZONE mode. Ignored for MULTI_ZONE mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#zone MemorystoreInstance#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ab258450e70cb8e297e157f1b64a4eeeddb1817eec3fa23d4215fd7fa2c505)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Current zone distribution mode. Defaults to MULTI_ZONE.   Possible values:  MULTI_ZONE SINGLE_ZONE Possible values: ["MULTI_ZONE", "SINGLE_ZONE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#mode MemorystoreInstance#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Optional. Defines zone where all resources will be allocated with SINGLE_ZONE mode. Ignored for MULTI_ZONE mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memorystore_instance#zone MemorystoreInstance#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemorystoreInstanceZoneDistributionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemorystoreInstanceZoneDistributionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memorystoreInstance.MemorystoreInstanceZoneDistributionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a9fde4a94263b67d257c19190b323d87c62969126edf85326fb471e6a07dafe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b253b164f077a6c2352baf0cd9a0bc406e04486bf47bb0f7f0e6a419928a12f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebf82efdd19426a53c5840978e92503b1b69d96fa121ce87b8ab5315e7f3beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemorystoreInstanceZoneDistributionConfig]:
        return typing.cast(typing.Optional[MemorystoreInstanceZoneDistributionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemorystoreInstanceZoneDistributionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03cdfc8f5febaee3dfe45f5da8e337c2aec578bd53f7a938d410d0111327e40e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MemorystoreInstance",
    "MemorystoreInstanceAutomatedBackupConfig",
    "MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule",
    "MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleOutputReference",
    "MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime",
    "MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference",
    "MemorystoreInstanceAutomatedBackupConfigOutputReference",
    "MemorystoreInstanceConfig",
    "MemorystoreInstanceCrossInstanceReplicationConfig",
    "MemorystoreInstanceCrossInstanceReplicationConfigMembership",
    "MemorystoreInstanceCrossInstanceReplicationConfigMembershipList",
    "MemorystoreInstanceCrossInstanceReplicationConfigMembershipOutputReference",
    "MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance",
    "MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceList",
    "MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceOutputReference",
    "MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance",
    "MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceList",
    "MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceOutputReference",
    "MemorystoreInstanceCrossInstanceReplicationConfigOutputReference",
    "MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance",
    "MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstanceOutputReference",
    "MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances",
    "MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesList",
    "MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesOutputReference",
    "MemorystoreInstanceDesiredAutoCreatedEndpoints",
    "MemorystoreInstanceDesiredAutoCreatedEndpointsList",
    "MemorystoreInstanceDesiredAutoCreatedEndpointsOutputReference",
    "MemorystoreInstanceDesiredPscAutoConnections",
    "MemorystoreInstanceDesiredPscAutoConnectionsList",
    "MemorystoreInstanceDesiredPscAutoConnectionsOutputReference",
    "MemorystoreInstanceDiscoveryEndpoints",
    "MemorystoreInstanceDiscoveryEndpointsList",
    "MemorystoreInstanceDiscoveryEndpointsOutputReference",
    "MemorystoreInstanceEndpoints",
    "MemorystoreInstanceEndpointsConnections",
    "MemorystoreInstanceEndpointsConnectionsList",
    "MemorystoreInstanceEndpointsConnectionsOutputReference",
    "MemorystoreInstanceEndpointsConnectionsPscAutoConnection",
    "MemorystoreInstanceEndpointsConnectionsPscAutoConnectionList",
    "MemorystoreInstanceEndpointsConnectionsPscAutoConnectionOutputReference",
    "MemorystoreInstanceEndpointsList",
    "MemorystoreInstanceEndpointsOutputReference",
    "MemorystoreInstanceGcsSource",
    "MemorystoreInstanceGcsSourceOutputReference",
    "MemorystoreInstanceMaintenancePolicy",
    "MemorystoreInstanceMaintenancePolicyOutputReference",
    "MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow",
    "MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowList",
    "MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
    "MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    "MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
    "MemorystoreInstanceMaintenanceSchedule",
    "MemorystoreInstanceMaintenanceScheduleList",
    "MemorystoreInstanceMaintenanceScheduleOutputReference",
    "MemorystoreInstanceManagedBackupSource",
    "MemorystoreInstanceManagedBackupSourceOutputReference",
    "MemorystoreInstanceManagedServerCa",
    "MemorystoreInstanceManagedServerCaCaCerts",
    "MemorystoreInstanceManagedServerCaCaCertsList",
    "MemorystoreInstanceManagedServerCaCaCertsOutputReference",
    "MemorystoreInstanceManagedServerCaList",
    "MemorystoreInstanceManagedServerCaOutputReference",
    "MemorystoreInstanceNodeConfig",
    "MemorystoreInstanceNodeConfigList",
    "MemorystoreInstanceNodeConfigOutputReference",
    "MemorystoreInstancePersistenceConfig",
    "MemorystoreInstancePersistenceConfigAofConfig",
    "MemorystoreInstancePersistenceConfigAofConfigOutputReference",
    "MemorystoreInstancePersistenceConfigOutputReference",
    "MemorystoreInstancePersistenceConfigRdbConfig",
    "MemorystoreInstancePersistenceConfigRdbConfigOutputReference",
    "MemorystoreInstancePscAttachmentDetails",
    "MemorystoreInstancePscAttachmentDetailsList",
    "MemorystoreInstancePscAttachmentDetailsOutputReference",
    "MemorystoreInstancePscAutoConnections",
    "MemorystoreInstancePscAutoConnectionsList",
    "MemorystoreInstancePscAutoConnectionsOutputReference",
    "MemorystoreInstanceStateInfo",
    "MemorystoreInstanceStateInfoList",
    "MemorystoreInstanceStateInfoOutputReference",
    "MemorystoreInstanceStateInfoUpdateInfo",
    "MemorystoreInstanceStateInfoUpdateInfoList",
    "MemorystoreInstanceStateInfoUpdateInfoOutputReference",
    "MemorystoreInstanceTimeouts",
    "MemorystoreInstanceTimeoutsOutputReference",
    "MemorystoreInstanceZoneDistributionConfig",
    "MemorystoreInstanceZoneDistributionConfigOutputReference",
]

publication.publish()

def _typecheckingstub__cc2fb45bb8e1c847a4a17ca4c94c17a84d676c09dbde16423c0c0a689a1401a6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_id: builtins.str,
    location: builtins.str,
    shard_count: jsii.Number,
    authorization_mode: typing.Optional[builtins.str] = None,
    automated_backup_config: typing.Optional[typing.Union[MemorystoreInstanceAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_instance_replication_config: typing.Optional[typing.Union[MemorystoreInstanceCrossInstanceReplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    desired_auto_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredAutoCreatedEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    desired_psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]]] = None,
    engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    gcs_source: typing.Optional[typing.Union[MemorystoreInstanceGcsSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_policy: typing.Optional[typing.Union[MemorystoreInstanceMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_backup_source: typing.Optional[typing.Union[MemorystoreInstanceManagedBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[MemorystoreInstancePersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MemorystoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
    zone_distribution_config: typing.Optional[typing.Union[MemorystoreInstanceZoneDistributionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5999bf261933318d3928796bbc87858f3284b2b0856a80ba3908e3c78dcb6149(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f4009209a626cdbbfd5b0a7d62a745bddcc82d5e80bc785bceca0db4fcb6c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredAutoCreatedEndpoints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f8b3ca7a5c726269af10f8f3baa00f32352171a258c1c441fb545233681cf6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314163717def6def7427963860283520f9dae21947b9b85d7d11fb3da38fca6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba6264442e0d3675fa984b8b6b73e92d785805cef96cf0a3e097b7e68ff6677(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3709f2e023f297982b4d562e66862abda06d692dfbecb17dd4614b2db11dbee2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f7066f3cf0b7fed9af12493ee42a710453ed4048d245c452cb4d04027cc6bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbea60c334c216a49ce5e969a6de927630d8c5271ca623c55ba8b40afe7a92c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4253d7579842b6b9565cc68381fdcb973f54b9a506a8141692920f85289e8262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51aeb45248e2ba7925a013657285f5cc4a8bef4be1cab01c88a4fee2241754a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6030b8fd7c5d1d6d400509880ccfe5bc117c8168aa5bae4064d98e3adee2b668(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19b2d8726834b58afc9f9651887c5dd44f463ffcbca9bfe3b616dcded38ec05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac46b8400839740879734134c86ef3aa4eaad4955c332b0e83e2c34d6fd7b614(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9676613b4ff73e9197c5fba4306e8db26fc31a56a1241e4f06e8c88f10a198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4b97fab2d84a7e93d96ed1be06b4edf72ce55bc8c0a051c4fb31135dfac647(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608afdbc5e8b92a5d21cba1c94b90e60110b9f8bab447520a2c4260dc1f20d41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930a9d6aa4b5980cff31b999170c74a4ebcd4a96c4200cec381071f91a734648(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da65f8b6ec7ad35a3e5044080b42d086ef89128afead8dde501886ac59719e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5f89ea37f9ca07bc16e80f7569ff4a485fbce491256cacb50fd3f750f14bd8(
    *,
    fixed_frequency_schedule: typing.Union[MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule, typing.Dict[builtins.str, typing.Any]],
    retention: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864aeb1a20493b57c05cf60f8e4de9ae2d218311b738106e34bc5ac70c5938a0(
    *,
    start_time: typing.Union[MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916c0081f1035f7c2c1ffb92b6e298ea6df4090a3e096cfe769cb71b5daa5ad0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff5717e582b46b1dbbe2bd324c4750b9e66049ade3b45119fe3255ec8e01bed(
    value: typing.Optional[MemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0913ec7042d3b4fb773d953757b7e761434f3f64757abe856f5e2669b93ed07f(
    *,
    hours: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c314b417b9f7d5e5dc7a727886094854ba1c8a1b9ed10f3ec810dca8e2d2cb2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a9e11a25d01a75501d144fc9c41533cc62dc716fe3b419eec2df9380b9785c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d3050590d17e9e2744b8fb1b8e1deb7b7bad3d9171d0059101af96fd9a7d20(
    value: typing.Optional[MemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f750a4c81ffddbdcdd83f2bf577d9292a7662e62ca120798e8cc30217bef84d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f63c93406e490c2d73dba90069fba20b10b7d4237a3550e22ca82c1f6f243b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12da0130765c7718dd205ed6db6a5f2c2d21c95bd70c51be67023da66c4149f1(
    value: typing.Optional[MemorystoreInstanceAutomatedBackupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de3252cb028a71fd621942b25263bfe393f97041bc2a312c902ff977d4131b2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_id: builtins.str,
    location: builtins.str,
    shard_count: jsii.Number,
    authorization_mode: typing.Optional[builtins.str] = None,
    automated_backup_config: typing.Optional[typing.Union[MemorystoreInstanceAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_instance_replication_config: typing.Optional[typing.Union[MemorystoreInstanceCrossInstanceReplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    desired_auto_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredAutoCreatedEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    desired_psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceDesiredPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]]] = None,
    engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    gcs_source: typing.Optional[typing.Union[MemorystoreInstanceGcsSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_policy: typing.Optional[typing.Union[MemorystoreInstanceMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_backup_source: typing.Optional[typing.Union[MemorystoreInstanceManagedBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[MemorystoreInstancePersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MemorystoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
    zone_distribution_config: typing.Optional[typing.Union[MemorystoreInstanceZoneDistributionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853faaead48f4ef26fbb4f70dc009a6f2fa10ec79880656c3976870390c0057b(
    *,
    instance_role: typing.Optional[builtins.str] = None,
    primary_instance: typing.Optional[typing.Union[MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    secondary_instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98975b928e0e1b7af8187777f46d62025604709a78a7976a4202078dade948e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27df2ca09fe8c197d85fc70129fc7f3d22b8e900e3a7b2f28af60a03de2dea18(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a4bbe6c5a37c628e9a835d2d679dd03401ee2183a80ce26bfac1117d0d3d5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07acf2089aee836b4e57a23a1fa789e7fa6ef96beffb07ba026f754906c1b4cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221290afab6ef21c018f04bcb846d330ad584f99e40400a1e3ae99611b50a12a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b264427f7965665b9c3b3e5cf5633535f826e13bc9911ec16a53145e969ae241(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cccf76af579790e34ca956919047a1f2f409198a4062a52c61f6b8d1100e69f5(
    value: typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembership],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27c76cf1961fa4f844ae6bb7c4df53eedfcbfd53dd31c11719a4f21a373ea1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513a137f48038e6e93ee5abd8b481f36753e4ec097897bd688eb12d1beeae1be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac803fef3786f53ec373f2434d32e288386d68d9196fc64a328f900016171fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4366755ef6d595284c6ed4a2df8077923b1d7a4842a74afe4a3e61d1f9cbcd6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3929eb9b3e7a6457fef269cba49796c0f417abfa5a3b6f06453ee614c4dc85e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b238769a9efa0f01257ecf88d211c4d69c74f9df6fd25cb860d0a9761eb3f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29781e2f947390467c4f6d3d19cbcd9d88ce51993231519ec47c3219b8c8ddf(
    value: typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401dfcccf886c0791b9c6a70daa7bfad77c67acba370988b62b2b3aab7f73c41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40beccf1da40621d736cba5fa45eb5cb5180946e02c040cae9ab0cf805b95f48(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c29118d087a40c823628e92a998516499bc36ac48cd1ee7d7ea4bfcdc8cff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19a775ab2b48edb610b8b182bed7335f6500896a6ed77d7f31b53716846c90e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f937263b6e7759aba42a81f9707cb9abfcf80686d2f3bf759eca59e64fad7e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7a5ce132a669827a2fd2a1c2a08378d67fc856a7c9808bd0590d9540544229(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bec252d7f1fd2b0a87ea90aeddaff45c57dfc2a6c236c333a81222c81295c80(
    value: typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b948293c9086e16b9c18eaced9c7b20c4b8579b9f543f335878cfb291565fd6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176cd83e6af6ffb272caf2c3fb22ed05db3947179e901d809bc4d8913d2f5e14(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab5532764c6f5170bbffb137f37e0ed4866a3a9ac0a77b5f54ab288947093ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e97eddd748daf879badd9d4a1273b275452f7a66a86507c8825d340f72d265(
    value: typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d377fae5c6a0c9762f727755ce9d211b5ee031c84af1a1f2ed7a1ccbf50141(
    *,
    instance: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856116e806da7122cbb01d4e1c008490c686519eb19ce13d6078bbbf86151b35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c9ea09c6e7fbd832c005890a4cf3f5f6dc83290c7c3220d945ea410887afea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0afc56938fc7709efe5f6f3e954260a68b40126190f3be48d32ce2092d401a(
    value: typing.Optional[MemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3aa051a57d67b220e81216be639aa1510684b82c307425435389f1847e10c7(
    *,
    instance: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec985953cc255b131040e73897ca8e0bd7001ac2b9ea3becf15b86c16c4e5c40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207980592db4fc7519dc08db24e78858b2a42fe67123d3096b31c7ce7eebf49a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20acfaa988939e820bf6c8f3774784b4f46da7b72a1705c51ca559edd9dd183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb8465622bbd44e6c51bab2ed32fd11a3140bd8250a441012fdaa89f91261b3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a71564e71b348f8b6a3e738c8d8e5c93155026e81b5dd79bcef2c10a8ddd25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b514d9b8ee40341a405fd424090561447ba33e255764a2439e4474b94753e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08d5bd470af15d73228962f2cb3c6907c9520419baa6eb5eaa37bbc7ca15bd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aaf3bdf6959f79330d4f20ff400124f2742a9a38be45dc06f6f7697274f80a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428f1fe142774980157577d6b4da5ed81cb921b8403d3d1d0f02c5cc6ab9f2e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70cd5bcdc0811921b1042b3a05dd9e0a9f66ba221f76be1e78f97cc7ebe7776(
    *,
    network: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8832ab285e6ec986d3bff0dc456024ee0e3789f53b93873e07d9f4a96edf5ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b404b1fcd9608c9325e01c93c00a43336debe9e206f019a7f54465a0fc98f0f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cea4ef9e5e35cd2cdd718e2c32f151ad8a74c283e1d998db5278fdb1a4d471(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8928f119ab875563ded1fd2d479a57b9a8e757c8b810672290fe4f67499f5bc4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c8cb54041e286ff579754a80161716033a02b1ede0a796ca94712b690527c7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e419a2f7cec740139e8124e9702046740a099a958389556d1baed78fb77f1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredAutoCreatedEndpoints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83058cee35a773f9936e1eabc1a4a5cc47f3796e4f40eb3f477a77321412187(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a8147a69b1af46e6f58088d5a2e76c247ac089434971185dc817513394980c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5673d110cefc4b12094637445ebe4881b7b7b3f830f1e538cf4764a0667f46dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c58e70d6fc94f67616bbbf9a2a83c5076ca21d4b5b89ee46a5c5adf2369a0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredAutoCreatedEndpoints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76db34ada6b358af4632b8cec3b794296d03488bdf8a6fb3ac955d2f5c08246e(
    *,
    network: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a5a75ff50325fba2758481f90765d870da191bd3af52eee6f94a98035dca62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50482b1aa741c93f4c6ec9ff8a290de853258a5ac40e479a554b3b79b1cd7e24(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa568015bcb6ccad30db9a1a550040fe52200208912fbd505efbd0d1f20b05d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b214daa5a189121307b9d45d1aeb027c7e1f4cd8dd1ac214c7428569fb9d69b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d83ee45ef1aca3818fc3ad0c4536451c3e9a01ac50fc6e88f9bc534f2f19f97(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d54229755f3398b74c9e12cd8c73d8b2d1bdb05dd7e9a1e739fd717058b1336(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceDesiredPscAutoConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cd4cbebb36e6eca7e5816b1a852356264f90b6b49e20e43e8b748346482ce0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64a0ede266977ce99fa5acbe1777c0ee6082d7a95a5a3f8e087d6ed6b1e850d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ab0617e10e8cd10e3333cbc00d1f066c1689807413fbb348f32190fe724f40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4476f1b5395acc9434ce8168c8dfad05119eca700f0d99ec7a06e9806caece42(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceDesiredPscAutoConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07eec391684704b3b66f0aab3c60e54184f419c967e99afed83d9c386b97d04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b3956559536c29e4ae6deb2fa6edfae137a486fc5f7aa7fd4f0f0ef6a34a1f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee06425654db2d0ba270286ed5fd96229e17d5d47c7427d5aa694ddfa2750fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee1b2745accf7ae8a05bc86617348257045e0d8c381598d4ae41cc261e07eb8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd596310fbf52060c13c4c21d9512b7c84fa0a7d308414eb9df264b75196ea02(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5e410e24c343a5594a58338eda10e1d78c71fac87688106cd96352f0de65b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d145318fb59423f668a373fac1969d57653ef62847b28419a65aa101c14167(
    value: typing.Optional[MemorystoreInstanceDiscoveryEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569baab77087c50d4d9750c40430c851b604113da3e93b2f28159982ad67d1be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0d68d61cd79615108945830182999dc730e2b9829c210167236496cf4e1dd5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7855fb217573ad4f81412fcc02dd3ec8b2a62a177f6ae2f6d26987b7714de0a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60250598f6ce93761fcc471cc6d77f96d2a9a4fd1c7334d45bb40805132d5937(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b915031012f523b81a8aa1de07f85233baf10d4df57db6245d6dbd5fd999ed8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf95c7a373f156175302694b3510e33a3993391dd7bc4a189800966909aef68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42669e16c95220ae9cc7c3180129931d6caad4a772a52bde0d3b7edfeef6aa26(
    value: typing.Optional[MemorystoreInstanceEndpointsConnections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e37a803726ea95cd4df306775fba46807590d89982e1aca6a37de559457f1c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a432ff60e9e9b2660420600a0adce82966bf57cfae39e644ecc62e312568db(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa7e25e27060548a4c08a808acfe79ec1c019715364a11dca3e3852259726c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae914ef00342d4dfa515773e7905da04c197e6639d22742c977f1c59221d002c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__706191fbfaf0a8098671290ca96d668a215ece67897cacf0e827ddd67cd90e86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f0171edb100f2162592badcc5040260e1eef5b9997c2ac4f4d2f1210e98935(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501de06dc6d0dcdde8a09fc18b1764ccff1bb58d793c0df2fc267b09a0864b9d(
    value: typing.Optional[MemorystoreInstanceEndpointsConnectionsPscAutoConnection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82eb0f7306c4471a6a45f87fd85261cc309a98298c4df0364b9e29baded20090(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8a6c0c5ca0b5dd4fdcab25678e76efe75b418398e836181dd187b501452b67(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c388225ac4a6f07b901aabae58f187d4f788b4b6c90fc67c43a30f8a38537d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251798396ad6872d1090d84badf34e06f16c0a163819e6afb57bb60f9701f90d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1066825067f6d3dd6cf00f4ece5f54ee5257f0e9e31cab7de49bc2b74d5dc34(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc759bb49e3eff1ff1d0bcde2609d4bd0acc2bcb464f10761d08b47070668056(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017d79ad179d19a3b9cd28efd6fb4cc6f8256b63cf6c3c2046b96e631cc7de18(
    value: typing.Optional[MemorystoreInstanceEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b749c4f7ba1b6cf572e7eb69b71583f33f518271bb9305139d877d37020f9a(
    *,
    uris: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1442d3635ea133caf1c71306bb92ebaa77b2c34249c7b638c504a15121b6262(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7b283de9728a8eb4636885385e708d3c16c9ec1702f03e5cec424a467a1b31(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeab0de4aa9287b59f676eca476d2158f3bd7a6860dfe6fcfe8b76ecc8ce6d00(
    value: typing.Optional[MemorystoreInstanceGcsSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42103fc76fcee89e33455c0ca69698a7e3bab09897451b8ba0165de79e38a5c7(
    *,
    weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab709311a80cc550686668f507afeb8aaf3048672f301c2f32c03b0e77b1f3be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d3470d922b6c2aa325a615b7d24fd81ac72d2512405ca2de9784359fcf5868(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a74af11704c460b6fb7747d281f08ba2188522f3f14a93d2996e56b8c162b3c(
    value: typing.Optional[MemorystoreInstanceMaintenancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53dbed1c0ff4112f5d9cc7276efe98bcbafa15d0bbdbe3714e55f43893d840b0(
    *,
    day: builtins.str,
    start_time: typing.Union[MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5232dbd241ef3219b697180983251e869ced82a0ac3df3ac3f9d01d1ec399130(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc2b7d1adb884012ab8a68450c3966b56f13803629fb5d3f7e8a2d1f039e20a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514e6f5a20b5d988fc329540dc317af64e2f3f2aa59e93d554519bda38d0519b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae6a7214a85b21ecc96967bb5bfe85d6413ad979c6915a310f284d0b82d6ff2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4529a082ab0ab910b326845d9c00e58325b1722e37de67caa476e373c422cfd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65585b1b4094d3d8ecda814e319eb1dd123dca831543c574736a9ae6797cdfc8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcebdda875548409eb0211f622643289e5705e50ca9b23be88b15eb16793c7bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a2024d4c592842d2570c47cd90edf888c7c257ba3f2d9c8657b26879f114ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f8f6aa987e28e18ab3e8e8a358ae07934147fe758859c8957a9d769165f0c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ed2aa4ac8f9e1070d576cd026bce68c49d268f4a07351d02da29e4659db6c7(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f00b4bfe81a53fa825404ea8b911dcff4d40bbecd6d4d3083153e3ed4a67407(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d4f5f5ecf5bd0af527c16e713cd2b0fe9a051a81393c1be418b7d096e8818d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9101f62fd4b5cacf1a71b50a5dc6787554633c4e953fa7d24ee9bb80c4dbcc4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898e496052ec3efc4afdd6841a893ee33b2929d8d32a13049f684161e61a64d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bf226e42d0565dfbf549230fd4656b80d9d934fe55ce31cb43cbeb0832474c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4fbd6062340bd83ea020d9dbf131ba1812f992bd9759e356e9301b5e217fbb(
    value: typing.Optional[MemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5c81f5fcfb1f5d853e5a53e01fc5d7ba83777bd73b704daa87ee08eaf75ce6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24db4982fab47f9ba6f69cfa6be71e125651e87338842762e1ba96cd09766365(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df924542b576ecb47d80c0b0995c5e1646ca280ffd88626b97ea6a871432762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df8b67bb6d2a7b2ab3d2d74fe09e25daaff05082d13c3fb78e306b60f78a66a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b12443fbf40727a74cc5e90aa5705d36eb9f8c8c04bc4859d912cdd1a21754f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0302f435959574247dab30bca18db06d49367737314e3d9632c3da7556c81a09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b604673f659d5a5a92776881f3552364553ae6d35d717107049f16f170944e26(
    value: typing.Optional[MemorystoreInstanceMaintenanceSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa4cda62d6205ac9b3e26d23c6a61453ab37d6e7745576c8cd274d9a2045153(
    *,
    backup: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aeaf37c80cc34f9d00eb6d63c22347b96c395d1e077f2df5cccaf0c5d721a77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378f92fd7f8cd452d16fed40144a0d80447dc5aa7824b282fb9cb57283ba82d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6e3ec255958c5f8ec8fd68161fafb46fbc3bb608f3a627680da4501122921f(
    value: typing.Optional[MemorystoreInstanceManagedBackupSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b289ab67ef53a1846e793bc2a70f9b30fcf38525849dfacbc8fc3db5288d5b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5102f612867cbb963ee9f3018d465371e3449cdf1c9812c881e0cea49b0e1263(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1932246cde019f28f1a882e800c3dec9c09f30512dda9d03f957b82bf0c8617d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dfebb4f1b1fbca6a9280644e82af4ecfe5ab7be16fbcf9b586d3459975fe81e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a983d05a4a63c4a07b5b89e905c3e8ddbd19c921a2fdfe6db42908c9dde18d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff387257281919e9543b84a6b78a49ce537ef974b634a10706804fce51a6d9c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a14b0f075b7af7547b90623e19a5379bd83754900010da0f4ff9433e6f8d3b4(
    value: typing.Optional[MemorystoreInstanceManagedServerCaCaCerts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b6b09025c93de591b1c8cd4eafd7d38c910df04955b43467fc236283bb335a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105f9eb15b52253eaa4e10f6b9778b4ea6dadf494e9e79fc90b3a3b2637282d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1166112a50fa615f7b6c13c3c9e85725a158155c31798b5db8f3e0683afa9dac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1bf1309feecc1de50f057e139c4b7092aed4ed579724d478529d353a3c35fc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452139d50a6336a76ebc7925171d1359ff196838677de9f3d51a36db062a0fd1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c48ec83613d63d2c493f8fdda09e07db093141e10006d0f1d5f8b5649326e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b205d155875aee81e9e5ce378083cbaab64b381027796dfa0dc6fa32eb7fdd(
    value: typing.Optional[MemorystoreInstanceManagedServerCa],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b235a65d0ecfb283379eb19478d9ef9973f101b5e48e22608f66837fbf88e44d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62fa3b688059a73d27cac7f8e488153ce08048e920c26898f4a1436fa406290(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f55f8334e7f6f94db59a7a9178782aa045b89a0679aecf63e63265f80351734d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a945acd2b62c9d2ab7809aa8f7bee21049a5dd42d7e3365151b87991cc271a7e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0b1a1a58df9b749b3b879bedef3c32e92cbe7845d9001583f5862431a271b2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6d37e39e2583c013ea71c4d94f8630ec51f93ee1d01dd4154ab2319e85b38d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752f3f0e9ad4955b683394cc173a47f938a89f7142fee4d4fa3d91c35d783aad(
    value: typing.Optional[MemorystoreInstanceNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9414844fbf7265eb139df17a1a5d3d7ffb5ea373cae0c371773ba8f2a189e147(
    *,
    aof_config: typing.Optional[typing.Union[MemorystoreInstancePersistenceConfigAofConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    rdb_config: typing.Optional[typing.Union[MemorystoreInstancePersistenceConfigRdbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b54e3ca144d7d6c06914605ba866043ec9bcd168b3ba038f7788a3f7b84ef38(
    *,
    append_fsync: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068bcc0536a632e29160ddf193998f8e244e48fb374dd2695a06f75e6a3da6d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13b73b72c6d179fdf76e26fefbe2c0a45ab792e67503cac5061502ef3ebb613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d62526aa04f462a8bf8dca0cad341a17c28c0275158d3985797a3361c3c79bc(
    value: typing.Optional[MemorystoreInstancePersistenceConfigAofConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ec9221129d2c0e7ba383cd2ae710eedcb54b2aad4aa70a2bec769a45d579c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f6c3070e821d5b4e6415ff5b5f1ef1da16a827567e7b1db51088088d8ed32e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81c6253caed7197ff8b4d7f5de291b29f642a5d8831b19f2acc190bf0e52171(
    value: typing.Optional[MemorystoreInstancePersistenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7db1332c63344ecd106396a78ef3aca1c1d1aa37a8f2a6679c26a5287e60c1b(
    *,
    rdb_snapshot_period: typing.Optional[builtins.str] = None,
    rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bb3725df1ccc4e463860ffdf14983714ebeb0604837eb6c38ec7243a0e2887(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88283cf8512976da15737eb287396b0a0b16aca2c62c04b3ce03fa22f8fc93b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f8bb3176258d4d065ebc6cba1cf00280508244b266a94bff2591ae1edc9fea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be216345b93f500c49669530fd7df3e06fb462779ce4748e1ed58273112abfe0(
    value: typing.Optional[MemorystoreInstancePersistenceConfigRdbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1906cf45a64d15daf4c1df560afe990418f06f31ec52be5908b06b2fa7b5b51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0aeb689214ec55f698c1ebc4bcb43a216424edaea64e32089e27277913c4885(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8696134f06feb90b9b13e458178a5c6e55b50245dca74644ee551035d23a2c18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713172f205358d039984c64b900299d20cf425868cd9edfd5b3144f09c42ea59(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463b2532d5fadb043854db80169eb6ecf1f8940520f9703ef80eb51d9469c93e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac332815f1e1b3ce887799aca1dda9a999803bee7692c50c70ac5baad68a554(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa037ebf09f0633a4f1669b351df2b3fa6caddb9f9d2f9d3e487606ce2040857(
    value: typing.Optional[MemorystoreInstancePscAttachmentDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b6b230a2494df4f2c3dfb4a94c4036acf58d4593978cf67999c82d05563996(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e726538e2ca4ec0285ca02774cf4d4cf09602cd9530dc34e917fefc3bc7bb9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2a1beefb527f323ce88fa135d54bf6100d0096f8dffa0d59df6afcfd03d970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34347ebd5ea54b15bcd1da860c0915eb3415ccf4ee16d94d1785d28d9c5c32ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccef096778a353341a88796f2b143979f10d8e608342b2d7f0af478033b9a2d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7544ccf3b7409b50fb57ef537ca9506bf1c1cf4577fefc4f32b78ff94c074cf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f995bbb332727706b9f077f3f2f4ef24769e21744182f7abbe4601951841cf(
    value: typing.Optional[MemorystoreInstancePscAutoConnections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf660e4341e02329e199f83f60f3155acb64e2333f4dc45d98dafdd2bd05c1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bd93d3c424fdf868151c1bb65f03ae31f3737851cf6a4059dc5e8e9922fc6d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99a564e1a8e87c84ae384e0a03e4847e007f98d33a5a2e9efb1d90c758784e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c41a8d4a08552be15f9fc8acb6e54d2c288b0ffb23dcd844c41612d4b269de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f84f2340d4339a960e65282a66c9d68e974c12dffb5bbe960a23e002357d3bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f822742e887f4501b90646bff3dc2aca400aa1ffd3cc161069973a2be09f1ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abd473b792faf2bfe074cf766ea539e701b0aff462a84f3b4c1c30b758e9cc5(
    value: typing.Optional[MemorystoreInstanceStateInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca39fd862fa28c6771459e17324d473da43531c2b9436d404a4555524b48b5a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e49b627d0cf8f14c187e5ba9ff6a7a7f76b0fa9193d09d80cd78b9e57aa9e9b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f0853a7dafcffa99a6014e18ce7be7aca09305a5b48abfd7254af38d0915b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac8d57ab93b9d3ab1d81ac9ad9fdd1632d49c804ab31c88809ed06beca3119d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb5e69ba11c33245e7f77d2218f93bbcda38423b71ab2345ebb2adc0b518963(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a3f94882bcc5f02bde866a481184eba294c2603c21dde2dabf0e137e61deec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a00f36a1febe806df0db7387da82f08da8a6c076925a25fda22af9b6eec6b1b(
    value: typing.Optional[MemorystoreInstanceStateInfoUpdateInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34020f411c6a81ce19b1c60b8ddb0a35402efaae888d8996711dca20e6ed4fb4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe659aaad8eca5a2bb17a8884e69bcfb527a96fb3b4426d0f0bd96d88b59302f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd9dcde0564f5e6551552c74551cb673b193e3808880599708a09e972d98888(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e0356560862ed62e131874219761f2b55f43a3f39629e59e878962171dbc83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bd1c782bdc0caaf80fdd05553eb206f6ca983603a7b7a5cab9bcab143f79b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ad08ac4ae77cb7e45d30ba85a49c2dd55fdedc9327d470c418abd273312d90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemorystoreInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ab258450e70cb8e297e157f1b64a4eeeddb1817eec3fa23d4215fd7fa2c505(
    *,
    mode: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9fde4a94263b67d257c19190b323d87c62969126edf85326fb471e6a07dafe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b253b164f077a6c2352baf0cd9a0bc406e04486bf47bb0f7f0e6a419928a12f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebf82efdd19426a53c5840978e92503b1b69d96fa121ce87b8ab5315e7f3beb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03cdfc8f5febaee3dfe45f5da8e337c2aec578bd53f7a938d410d0111327e40e(
    value: typing.Optional[MemorystoreInstanceZoneDistributionConfig],
) -> None:
    """Type checking stubs"""
    pass
