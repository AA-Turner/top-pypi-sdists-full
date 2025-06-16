r'''
# `google_memorystore_instance`

Refer to the Terraform Registry for docs: [`google_memorystore_instance`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance).
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


class GoogleMemorystoreInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance google_memorystore_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_id: builtins.str,
        location: builtins.str,
        shard_count: jsii.Number,
        authorization_mode: typing.Optional[builtins.str] = None,
        automated_backup_config: typing.Optional[typing.Union["GoogleMemorystoreInstanceAutomatedBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cross_instance_replication_config: typing.Optional[typing.Union["GoogleMemorystoreInstanceCrossInstanceReplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        desired_auto_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        desired_psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceDesiredPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        gcs_source: typing.Optional[typing.Union["GoogleMemorystoreInstanceGcsSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_policy: typing.Optional[typing.Union["GoogleMemorystoreInstanceMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_backup_source: typing.Optional[typing.Union["GoogleMemorystoreInstanceManagedBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["GoogleMemorystoreInstancePersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleMemorystoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        zone_distribution_config: typing.Optional[typing.Union["GoogleMemorystoreInstanceZoneDistributionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance google_memorystore_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_id: Required. The ID to use for the instance, which will become the final component of the instance's resource name. This value is subject to the following restrictions: - Must be 4-63 characters in length - Must begin with a letter or digit - Must contain only lowercase letters, digits, and hyphens - Must not end with a hyphen - Must be unique within a location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#instance_id GoogleMemorystoreInstance#instance_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. See documentation for resource type 'memorystore.googleapis.com/CertificateAuthority'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#location GoogleMemorystoreInstance#location}
        :param shard_count: Required. Number of shards for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#shard_count GoogleMemorystoreInstance#shard_count}
        :param authorization_mode: Optional. Immutable. Authorization mode of the instance. Possible values: AUTH_DISABLED IAM_AUTH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#authorization_mode GoogleMemorystoreInstance#authorization_mode}
        :param automated_backup_config: automated_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#automated_backup_config GoogleMemorystoreInstance#automated_backup_config}
        :param cross_instance_replication_config: cross_instance_replication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#cross_instance_replication_config GoogleMemorystoreInstance#cross_instance_replication_config}
        :param deletion_protection_enabled: Optional. If set to true deletion of the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#deletion_protection_enabled GoogleMemorystoreInstance#deletion_protection_enabled}
        :param desired_auto_created_endpoints: desired_auto_created_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#desired_auto_created_endpoints GoogleMemorystoreInstance#desired_auto_created_endpoints}
        :param desired_psc_auto_connections: desired_psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#desired_psc_auto_connections GoogleMemorystoreInstance#desired_psc_auto_connections}
        :param engine_configs: Optional. User-provided engine configurations for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#engine_configs GoogleMemorystoreInstance#engine_configs}
        :param engine_version: Optional. Engine version of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#engine_version GoogleMemorystoreInstance#engine_version}
        :param gcs_source: gcs_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#gcs_source GoogleMemorystoreInstance#gcs_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#id GoogleMemorystoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#labels GoogleMemorystoreInstance#labels}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#maintenance_policy GoogleMemorystoreInstance#maintenance_policy}
        :param managed_backup_source: managed_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#managed_backup_source GoogleMemorystoreInstance#managed_backup_source}
        :param mode: Optional. cluster or cluster-disabled. Possible values: CLUSTER CLUSTER_DISABLED Possible values: ["CLUSTER", "CLUSTER_DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#mode GoogleMemorystoreInstance#mode}
        :param node_type: Optional. Machine type for individual nodes of the instance. Possible values: SHARED_CORE_NANO HIGHMEM_MEDIUM HIGHMEM_XLARGE STANDARD_SMALL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#node_type GoogleMemorystoreInstance#node_type}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#persistence_config GoogleMemorystoreInstance#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#project GoogleMemorystoreInstance#project}.
        :param replica_count: Optional. Number of replica nodes per shard. If omitted the default is 0 replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#replica_count GoogleMemorystoreInstance#replica_count}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#timeouts GoogleMemorystoreInstance#timeouts}
        :param transit_encryption_mode: Optional. Immutable. In-transit encryption mode of the instance. Possible values: TRANSIT_ENCRYPTION_DISABLED SERVER_AUTHENTICATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#transit_encryption_mode GoogleMemorystoreInstance#transit_encryption_mode}
        :param zone_distribution_config: zone_distribution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#zone_distribution_config GoogleMemorystoreInstance#zone_distribution_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4688ebec174e4e2bce73fba43bf23f773ce551120e85cff9bb081f5e88b3686d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleMemorystoreInstanceConfig(
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
        '''Generates CDKTF code for importing a GoogleMemorystoreInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleMemorystoreInstance to import.
        :param import_from_id: The id of the existing GoogleMemorystoreInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleMemorystoreInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512ee504f9ad42f1170b0ba76292931a000eff65bed59e483ec08e2e36f22cfa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutomatedBackupConfig")
    def put_automated_backup_config(
        self,
        *,
        fixed_frequency_schedule: typing.Union["GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule", typing.Dict[builtins.str, typing.Any]],
        retention: builtins.str,
    ) -> None:
        '''
        :param fixed_frequency_schedule: fixed_frequency_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#fixed_frequency_schedule GoogleMemorystoreInstance#fixed_frequency_schedule}
        :param retention: How long to keep automated backups before the backups are deleted. The value should be between 1 day and 365 days. If not specified, the default value is 35 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". The default_value is "3024000s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#retention GoogleMemorystoreInstance#retention}
        '''
        value = GoogleMemorystoreInstanceAutomatedBackupConfig(
            fixed_frequency_schedule=fixed_frequency_schedule, retention=retention
        )

        return typing.cast(None, jsii.invoke(self, "putAutomatedBackupConfig", [value]))

    @jsii.member(jsii_name="putCrossInstanceReplicationConfig")
    def put_cross_instance_replication_config(
        self,
        *,
        instance_role: typing.Optional[builtins.str] = None,
        primary_instance: typing.Optional[typing.Union["GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param instance_role: The instance role supports the following values: 1. 'INSTANCE_ROLE_UNSPECIFIED': This is an independent instance that has never participated in cross instance replication. It allows both reads and writes. 2. 'NONE': This is an independent instance that previously participated in cross instance replication(either as a 'PRIMARY' or 'SECONDARY' cluster). It allows both reads and writes. 3. 'PRIMARY': This instance serves as the replication source for secondary instance that are replicating from it. Any data written to it is automatically replicated to its secondary clusters. It allows both reads and writes. 4. 'SECONDARY': This instance replicates data from the primary instance. It allows only reads. Possible values: ["INSTANCE_ROLE_UNSPECIFIED", "NONE", "PRIMARY", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#instance_role GoogleMemorystoreInstance#instance_role}
        :param primary_instance: primary_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#primary_instance GoogleMemorystoreInstance#primary_instance}
        :param secondary_instances: secondary_instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#secondary_instances GoogleMemorystoreInstance#secondary_instances}
        '''
        value = GoogleMemorystoreInstanceCrossInstanceReplicationConfig(
            instance_role=instance_role,
            primary_instance=primary_instance,
            secondary_instances=secondary_instances,
        )

        return typing.cast(None, jsii.invoke(self, "putCrossInstanceReplicationConfig", [value]))

    @jsii.member(jsii_name="putDesiredAutoCreatedEndpoints")
    def put_desired_auto_created_endpoints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0cbfd392c8bbd5be54df993775116068ead47e596b745ae4985f9a229bdfe69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDesiredAutoCreatedEndpoints", [value]))

    @jsii.member(jsii_name="putDesiredPscAutoConnections")
    def put_desired_psc_auto_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceDesiredPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ce83b6def3374756126fb6bd1d1c6465f013bc5f47e51045cdb79b352c6f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDesiredPscAutoConnections", [value]))

    @jsii.member(jsii_name="putGcsSource")
    def put_gcs_source(self, *, uris: typing.Sequence[builtins.str]) -> None:
        '''
        :param uris: URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#uris GoogleMemorystoreInstance#uris}
        '''
        value = GoogleMemorystoreInstanceGcsSource(uris=uris)

        return typing.cast(None, jsii.invoke(self, "putGcsSource", [value]))

    @jsii.member(jsii_name="putMaintenancePolicy")
    def put_maintenance_policy(
        self,
        *,
        weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#weekly_maintenance_window GoogleMemorystoreInstance#weekly_maintenance_window}
        '''
        value = GoogleMemorystoreInstanceMaintenancePolicy(
            weekly_maintenance_window=weekly_maintenance_window
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenancePolicy", [value]))

    @jsii.member(jsii_name="putManagedBackupSource")
    def put_managed_backup_source(self, *, backup: builtins.str) -> None:
        '''
        :param backup: Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#backup GoogleMemorystoreInstance#backup}
        '''
        value = GoogleMemorystoreInstanceManagedBackupSource(backup=backup)

        return typing.cast(None, jsii.invoke(self, "putManagedBackupSource", [value]))

    @jsii.member(jsii_name="putPersistenceConfig")
    def put_persistence_config(
        self,
        *,
        aof_config: typing.Optional[typing.Union["GoogleMemorystoreInstancePersistenceConfigAofConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        rdb_config: typing.Optional[typing.Union["GoogleMemorystoreInstancePersistenceConfigRdbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aof_config: aof_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#aof_config GoogleMemorystoreInstance#aof_config}
        :param mode: Optional. Current persistence mode. Possible values: DISABLED RDB AOF Possible values: ["DISABLED", "RDB", "AOF"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#mode GoogleMemorystoreInstance#mode}
        :param rdb_config: rdb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#rdb_config GoogleMemorystoreInstance#rdb_config}
        '''
        value = GoogleMemorystoreInstancePersistenceConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#create GoogleMemorystoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#delete GoogleMemorystoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#update GoogleMemorystoreInstance#update}.
        '''
        value = GoogleMemorystoreInstanceTimeouts(
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
        :param mode: Optional. Current zone distribution mode. Defaults to MULTI_ZONE. Possible values: MULTI_ZONE SINGLE_ZONE Possible values: ["MULTI_ZONE", "SINGLE_ZONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#mode GoogleMemorystoreInstance#mode}
        :param zone: Optional. Defines zone where all resources will be allocated with SINGLE_ZONE mode. Ignored for MULTI_ZONE mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#zone GoogleMemorystoreInstance#zone}
        '''
        value = GoogleMemorystoreInstanceZoneDistributionConfig(mode=mode, zone=zone)

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
    ) -> "GoogleMemorystoreInstanceAutomatedBackupConfigOutputReference":
        return typing.cast("GoogleMemorystoreInstanceAutomatedBackupConfigOutputReference", jsii.get(self, "automatedBackupConfig"))

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
    ) -> "GoogleMemorystoreInstanceCrossInstanceReplicationConfigOutputReference":
        return typing.cast("GoogleMemorystoreInstanceCrossInstanceReplicationConfigOutputReference", jsii.get(self, "crossInstanceReplicationConfig"))

    @builtins.property
    @jsii.member(jsii_name="desiredAutoCreatedEndpoints")
    def desired_auto_created_endpoints(
        self,
    ) -> "GoogleMemorystoreInstanceDesiredAutoCreatedEndpointsList":
        return typing.cast("GoogleMemorystoreInstanceDesiredAutoCreatedEndpointsList", jsii.get(self, "desiredAutoCreatedEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="desiredPscAutoConnections")
    def desired_psc_auto_connections(
        self,
    ) -> "GoogleMemorystoreInstanceDesiredPscAutoConnectionsList":
        return typing.cast("GoogleMemorystoreInstanceDesiredPscAutoConnectionsList", jsii.get(self, "desiredPscAutoConnections"))

    @builtins.property
    @jsii.member(jsii_name="discoveryEndpoints")
    def discovery_endpoints(self) -> "GoogleMemorystoreInstanceDiscoveryEndpointsList":
        return typing.cast("GoogleMemorystoreInstanceDiscoveryEndpointsList", jsii.get(self, "discoveryEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> "GoogleMemorystoreInstanceEndpointsList":
        return typing.cast("GoogleMemorystoreInstanceEndpointsList", jsii.get(self, "endpoints"))

    @builtins.property
    @jsii.member(jsii_name="gcsSource")
    def gcs_source(self) -> "GoogleMemorystoreInstanceGcsSourceOutputReference":
        return typing.cast("GoogleMemorystoreInstanceGcsSourceOutputReference", jsii.get(self, "gcsSource"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicy")
    def maintenance_policy(
        self,
    ) -> "GoogleMemorystoreInstanceMaintenancePolicyOutputReference":
        return typing.cast("GoogleMemorystoreInstanceMaintenancePolicyOutputReference", jsii.get(self, "maintenancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceSchedule")
    def maintenance_schedule(
        self,
    ) -> "GoogleMemorystoreInstanceMaintenanceScheduleList":
        return typing.cast("GoogleMemorystoreInstanceMaintenanceScheduleList", jsii.get(self, "maintenanceSchedule"))

    @builtins.property
    @jsii.member(jsii_name="managedBackupSource")
    def managed_backup_source(
        self,
    ) -> "GoogleMemorystoreInstanceManagedBackupSourceOutputReference":
        return typing.cast("GoogleMemorystoreInstanceManagedBackupSourceOutputReference", jsii.get(self, "managedBackupSource"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "GoogleMemorystoreInstanceNodeConfigList":
        return typing.cast("GoogleMemorystoreInstanceNodeConfigList", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="persistenceConfig")
    def persistence_config(
        self,
    ) -> "GoogleMemorystoreInstancePersistenceConfigOutputReference":
        return typing.cast("GoogleMemorystoreInstancePersistenceConfigOutputReference", jsii.get(self, "persistenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="pscAttachmentDetails")
    def psc_attachment_details(
        self,
    ) -> "GoogleMemorystoreInstancePscAttachmentDetailsList":
        return typing.cast("GoogleMemorystoreInstancePscAttachmentDetailsList", jsii.get(self, "pscAttachmentDetails"))

    @builtins.property
    @jsii.member(jsii_name="pscAutoConnections")
    def psc_auto_connections(self) -> "GoogleMemorystoreInstancePscAutoConnectionsList":
        return typing.cast("GoogleMemorystoreInstancePscAutoConnectionsList", jsii.get(self, "pscAutoConnections"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateInfo")
    def state_info(self) -> "GoogleMemorystoreInstanceStateInfoList":
        return typing.cast("GoogleMemorystoreInstanceStateInfoList", jsii.get(self, "stateInfo"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleMemorystoreInstanceTimeoutsOutputReference":
        return typing.cast("GoogleMemorystoreInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> "GoogleMemorystoreInstanceZoneDistributionConfigOutputReference":
        return typing.cast("GoogleMemorystoreInstanceZoneDistributionConfigOutputReference", jsii.get(self, "zoneDistributionConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizationModeInput")
    def authorization_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="automatedBackupConfigInput")
    def automated_backup_config_input(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstanceAutomatedBackupConfig"]:
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceAutomatedBackupConfig"], jsii.get(self, "automatedBackupConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="crossInstanceReplicationConfigInput")
    def cross_instance_replication_config_input(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstanceCrossInstanceReplicationConfig"]:
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceCrossInstanceReplicationConfig"], jsii.get(self, "crossInstanceReplicationConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints"]]], jsii.get(self, "desiredAutoCreatedEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredPscAutoConnectionsInput")
    def desired_psc_auto_connections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceDesiredPscAutoConnections"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceDesiredPscAutoConnections"]]], jsii.get(self, "desiredPscAutoConnectionsInput"))

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
    def gcs_source_input(self) -> typing.Optional["GoogleMemorystoreInstanceGcsSource"]:
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceGcsSource"], jsii.get(self, "gcsSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

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
    ) -> typing.Optional["GoogleMemorystoreInstanceMaintenancePolicy"]:
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceMaintenancePolicy"], jsii.get(self, "maintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="managedBackupSourceInput")
    def managed_backup_source_input(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstanceManagedBackupSource"]:
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceManagedBackupSource"], jsii.get(self, "managedBackupSourceInput"))

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
    ) -> typing.Optional["GoogleMemorystoreInstancePersistenceConfig"]:
        return typing.cast(typing.Optional["GoogleMemorystoreInstancePersistenceConfig"], jsii.get(self, "persistenceConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleMemorystoreInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleMemorystoreInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionModeInput")
    def transit_encryption_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitEncryptionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneDistributionConfigInput")
    def zone_distribution_config_input(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstanceZoneDistributionConfig"]:
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceZoneDistributionConfig"], jsii.get(self, "zoneDistributionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationMode")
    def authorization_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationMode"))

    @authorization_mode.setter
    def authorization_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47b564ea1c0f118cf2ebaae23af2b487e7a47b8d595cdb4096234a7a8de1846)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf7e4aaa414209995f02d0d4c9f020f47c4647b91329c7bde1c2bd201753722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineConfigs")
    def engine_configs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "engineConfigs"))

    @engine_configs.setter
    def engine_configs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abeedc3b9748c4b2971697b40d01185a280dab1af9fc87b0a95d63afa71d8972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineConfigs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec0000681c267c9e70bce386446d277cc0b4db572c446febd959e1659f5a3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f1c1f57dc53d04c264791334ce9c454eab3079b786ea423c41bbc1da0b3bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57710777d9973b7754255209086aa55ce28e4ad9e5513ad2fbe85f784f8d10f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee498b6eee9e4e736018e09333b58c57cbe9bf0b6631f584878e09760256dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3597fc1668d948bcef9b555605e30ea17aa62b15a856a477019ea6fa1292ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05cd83134a1760952db3b8f3a198fb28d72240933fff1422b32bc14530dd5d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1506d2f336f29c701c2aeb8c55fdf1b4a1564d483d82237af36e3b6a463831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621bbcb46a21790b7907d40ad1877f0a603ffeeee8309b0db2d451a2825f1520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCount"))

    @replica_count.setter
    def replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4030c1772fac511e051565c596dbb87a7a8e70a54677f4b80be6df0c8a6263fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shardCount")
    def shard_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shardCount"))

    @shard_count.setter
    def shard_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6066a54e144e6c2caf1816e83b9ba9c819644b2e0f41e328927505b2d0ac82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shardCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionMode")
    def transit_encryption_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitEncryptionMode"))

    @transit_encryption_mode.setter
    def transit_encryption_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56bec9155a3dc4b5d99e180ecf766b1d60c6d5ee8cddcd8fcb0515c1b1b09b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitEncryptionMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceAutomatedBackupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "fixed_frequency_schedule": "fixedFrequencySchedule",
        "retention": "retention",
    },
)
class GoogleMemorystoreInstanceAutomatedBackupConfig:
    def __init__(
        self,
        *,
        fixed_frequency_schedule: typing.Union["GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule", typing.Dict[builtins.str, typing.Any]],
        retention: builtins.str,
    ) -> None:
        '''
        :param fixed_frequency_schedule: fixed_frequency_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#fixed_frequency_schedule GoogleMemorystoreInstance#fixed_frequency_schedule}
        :param retention: How long to keep automated backups before the backups are deleted. The value should be between 1 day and 365 days. If not specified, the default value is 35 days. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". The default_value is "3024000s" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#retention GoogleMemorystoreInstance#retention}
        '''
        if isinstance(fixed_frequency_schedule, dict):
            fixed_frequency_schedule = GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule(**fixed_frequency_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed12923319fe96538174196c41ad3c7a9443cae14be84791f648bd5433ea2a67)
            check_type(argname="argument fixed_frequency_schedule", value=fixed_frequency_schedule, expected_type=type_hints["fixed_frequency_schedule"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fixed_frequency_schedule": fixed_frequency_schedule,
            "retention": retention,
        }

    @builtins.property
    def fixed_frequency_schedule(
        self,
    ) -> "GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule":
        '''fixed_frequency_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#fixed_frequency_schedule GoogleMemorystoreInstance#fixed_frequency_schedule}
        '''
        result = self._values.get("fixed_frequency_schedule")
        assert result is not None, "Required property 'fixed_frequency_schedule' is missing"
        return typing.cast("GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule", result)

    @builtins.property
    def retention(self) -> builtins.str:
        '''How long to keep automated backups before the backups are deleted.

        The value should be between 1 day and 365 days. If not specified, the default value is 35 days.
        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". The default_value is "3024000s"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#retention GoogleMemorystoreInstance#retention}
        '''
        result = self._values.get("retention")
        assert result is not None, "Required property 'retention' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceAutomatedBackupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule",
    jsii_struct_bases=[],
    name_mapping={"start_time": "startTime"},
)
class GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule:
    def __init__(
        self,
        *,
        start_time: typing.Union["GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#start_time GoogleMemorystoreInstance#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0d8afd809bf272d698ab8254254ce7856f819c992551bf96b46951b50706dff)
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_time": start_time,
        }

    @builtins.property
    def start_time(
        self,
    ) -> "GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#start_time GoogleMemorystoreInstance#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70daed0ac8f542aedcc2b9864379a1bdbb520b774fa2477b4baac157e49bf0d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(self, *, hours: jsii.Number) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#hours GoogleMemorystoreInstance#hours}
        '''
        value = GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime(
            hours=hours
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference":
        return typing.cast("GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime"]:
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec4cc2478ac335ab8fbb563d5ee0439fb88b81cb5929119f2b3296d6e5fffe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime",
    jsii_struct_bases=[],
    name_mapping={"hours": "hours"},
)
class GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime:
    def __init__(self, *, hours: jsii.Number) -> None:
        '''
        :param hours: Hours of a day in 24 hour format. Must be greater than or equal to 0 and typically must be less than or equal to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#hours GoogleMemorystoreInstance#hours}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a6f5ae110e43282753443a324a69a1a4e233a04e68910cc2fec7a3633a2307)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hours": hours,
        }

    @builtins.property
    def hours(self) -> jsii.Number:
        '''Hours of a day in 24 hour format.

        Must be greater than or equal to 0 and typically must be less than or equal to 23.
        An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#hours GoogleMemorystoreInstance#hours}
        '''
        result = self._values.get("hours")
        assert result is not None, "Required property 'hours' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1df081763c42804f096eadc89ccaaa3d91b3eeedc7a98e6690db6485f406a38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf20c01bbe4fa8fa47a36b704f3e9d3246d5a368550c7cb4d6788e48c9ea9ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c55c82c92d8b6f806fda422cd4526be1f1b05b36b43e0783a9e4b7ed8fb093a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceAutomatedBackupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceAutomatedBackupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f74e5e019ec6bf27de607e237b6a32ef5487a5780caca1a48cecf2c270d12e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFixedFrequencySchedule")
    def put_fixed_frequency_schedule(
        self,
        *,
        start_time: typing.Union[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#start_time GoogleMemorystoreInstance#start_time}
        '''
        value = GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule(
            start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putFixedFrequencySchedule", [value]))

    @builtins.property
    @jsii.member(jsii_name="fixedFrequencySchedule")
    def fixed_frequency_schedule(
        self,
    ) -> GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleOutputReference:
        return typing.cast(GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleOutputReference, jsii.get(self, "fixedFrequencySchedule"))

    @builtins.property
    @jsii.member(jsii_name="fixedFrequencyScheduleInput")
    def fixed_frequency_schedule_input(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule], jsii.get(self, "fixedFrequencyScheduleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__41aa3be59fa7c81fdd4a8a259dfe8912b8a412c197df056836665854b0dd1f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfig]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a4ed458d98e762d36f3158d615b919b5602d2fb111e7a27254f42a6c8b2211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceConfig",
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
class GoogleMemorystoreInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        automated_backup_config: typing.Optional[typing.Union[GoogleMemorystoreInstanceAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        cross_instance_replication_config: typing.Optional[typing.Union["GoogleMemorystoreInstanceCrossInstanceReplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        desired_auto_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        desired_psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceDesiredPscAutoConnections", typing.Dict[builtins.str, typing.Any]]]]] = None,
        engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        gcs_source: typing.Optional[typing.Union["GoogleMemorystoreInstanceGcsSource", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_policy: typing.Optional[typing.Union["GoogleMemorystoreInstanceMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_backup_source: typing.Optional[typing.Union["GoogleMemorystoreInstanceManagedBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["GoogleMemorystoreInstancePersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleMemorystoreInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        zone_distribution_config: typing.Optional[typing.Union["GoogleMemorystoreInstanceZoneDistributionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_id: Required. The ID to use for the instance, which will become the final component of the instance's resource name. This value is subject to the following restrictions: - Must be 4-63 characters in length - Must begin with a letter or digit - Must contain only lowercase letters, digits, and hyphens - Must not end with a hyphen - Must be unique within a location Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#instance_id GoogleMemorystoreInstance#instance_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. See documentation for resource type 'memorystore.googleapis.com/CertificateAuthority'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#location GoogleMemorystoreInstance#location}
        :param shard_count: Required. Number of shards for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#shard_count GoogleMemorystoreInstance#shard_count}
        :param authorization_mode: Optional. Immutable. Authorization mode of the instance. Possible values: AUTH_DISABLED IAM_AUTH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#authorization_mode GoogleMemorystoreInstance#authorization_mode}
        :param automated_backup_config: automated_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#automated_backup_config GoogleMemorystoreInstance#automated_backup_config}
        :param cross_instance_replication_config: cross_instance_replication_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#cross_instance_replication_config GoogleMemorystoreInstance#cross_instance_replication_config}
        :param deletion_protection_enabled: Optional. If set to true deletion of the instance will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#deletion_protection_enabled GoogleMemorystoreInstance#deletion_protection_enabled}
        :param desired_auto_created_endpoints: desired_auto_created_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#desired_auto_created_endpoints GoogleMemorystoreInstance#desired_auto_created_endpoints}
        :param desired_psc_auto_connections: desired_psc_auto_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#desired_psc_auto_connections GoogleMemorystoreInstance#desired_psc_auto_connections}
        :param engine_configs: Optional. User-provided engine configurations for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#engine_configs GoogleMemorystoreInstance#engine_configs}
        :param engine_version: Optional. Engine version of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#engine_version GoogleMemorystoreInstance#engine_version}
        :param gcs_source: gcs_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#gcs_source GoogleMemorystoreInstance#gcs_source}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#id GoogleMemorystoreInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#labels GoogleMemorystoreInstance#labels}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#maintenance_policy GoogleMemorystoreInstance#maintenance_policy}
        :param managed_backup_source: managed_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#managed_backup_source GoogleMemorystoreInstance#managed_backup_source}
        :param mode: Optional. cluster or cluster-disabled. Possible values: CLUSTER CLUSTER_DISABLED Possible values: ["CLUSTER", "CLUSTER_DISABLED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#mode GoogleMemorystoreInstance#mode}
        :param node_type: Optional. Machine type for individual nodes of the instance. Possible values: SHARED_CORE_NANO HIGHMEM_MEDIUM HIGHMEM_XLARGE STANDARD_SMALL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#node_type GoogleMemorystoreInstance#node_type}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#persistence_config GoogleMemorystoreInstance#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#project GoogleMemorystoreInstance#project}.
        :param replica_count: Optional. Number of replica nodes per shard. If omitted the default is 0 replicas. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#replica_count GoogleMemorystoreInstance#replica_count}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#timeouts GoogleMemorystoreInstance#timeouts}
        :param transit_encryption_mode: Optional. Immutable. In-transit encryption mode of the instance. Possible values: TRANSIT_ENCRYPTION_DISABLED SERVER_AUTHENTICATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#transit_encryption_mode GoogleMemorystoreInstance#transit_encryption_mode}
        :param zone_distribution_config: zone_distribution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#zone_distribution_config GoogleMemorystoreInstance#zone_distribution_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(automated_backup_config, dict):
            automated_backup_config = GoogleMemorystoreInstanceAutomatedBackupConfig(**automated_backup_config)
        if isinstance(cross_instance_replication_config, dict):
            cross_instance_replication_config = GoogleMemorystoreInstanceCrossInstanceReplicationConfig(**cross_instance_replication_config)
        if isinstance(gcs_source, dict):
            gcs_source = GoogleMemorystoreInstanceGcsSource(**gcs_source)
        if isinstance(maintenance_policy, dict):
            maintenance_policy = GoogleMemorystoreInstanceMaintenancePolicy(**maintenance_policy)
        if isinstance(managed_backup_source, dict):
            managed_backup_source = GoogleMemorystoreInstanceManagedBackupSource(**managed_backup_source)
        if isinstance(persistence_config, dict):
            persistence_config = GoogleMemorystoreInstancePersistenceConfig(**persistence_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleMemorystoreInstanceTimeouts(**timeouts)
        if isinstance(zone_distribution_config, dict):
            zone_distribution_config = GoogleMemorystoreInstanceZoneDistributionConfig(**zone_distribution_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce2acffab769689ca75cf807d1172d26a3eba0f7c678343bc130011ca87a83c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#instance_id GoogleMemorystoreInstance#instance_id}
        '''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'.

        It identifies the resource within its parent collection as described in https://google.aip.dev/122. See documentation for resource type 'memorystore.googleapis.com/CertificateAuthority'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#location GoogleMemorystoreInstance#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shard_count(self) -> jsii.Number:
        '''Required. Number of shards for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#shard_count GoogleMemorystoreInstance#shard_count}
        '''
        result = self._values.get("shard_count")
        assert result is not None, "Required property 'shard_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def authorization_mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Immutable. Authorization mode of the instance. Possible values:  AUTH_DISABLED IAM_AUTH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#authorization_mode GoogleMemorystoreInstance#authorization_mode}
        '''
        result = self._values.get("authorization_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automated_backup_config(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfig]:
        '''automated_backup_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#automated_backup_config GoogleMemorystoreInstance#automated_backup_config}
        '''
        result = self._values.get("automated_backup_config")
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfig], result)

    @builtins.property
    def cross_instance_replication_config(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstanceCrossInstanceReplicationConfig"]:
        '''cross_instance_replication_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#cross_instance_replication_config GoogleMemorystoreInstance#cross_instance_replication_config}
        '''
        result = self._values.get("cross_instance_replication_config")
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceCrossInstanceReplicationConfig"], result)

    @builtins.property
    def deletion_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. If set to true deletion of the instance will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#deletion_protection_enabled GoogleMemorystoreInstance#deletion_protection_enabled}
        '''
        result = self._values.get("deletion_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def desired_auto_created_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints"]]]:
        '''desired_auto_created_endpoints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#desired_auto_created_endpoints GoogleMemorystoreInstance#desired_auto_created_endpoints}
        '''
        result = self._values.get("desired_auto_created_endpoints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints"]]], result)

    @builtins.property
    def desired_psc_auto_connections(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceDesiredPscAutoConnections"]]]:
        '''desired_psc_auto_connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#desired_psc_auto_connections GoogleMemorystoreInstance#desired_psc_auto_connections}
        '''
        result = self._values.get("desired_psc_auto_connections")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceDesiredPscAutoConnections"]]], result)

    @builtins.property
    def engine_configs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. User-provided engine configurations for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#engine_configs GoogleMemorystoreInstance#engine_configs}
        '''
        result = self._values.get("engine_configs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''Optional. Engine version of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#engine_version GoogleMemorystoreInstance#engine_version}
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcs_source(self) -> typing.Optional["GoogleMemorystoreInstanceGcsSource"]:
        '''gcs_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#gcs_source GoogleMemorystoreInstance#gcs_source}
        '''
        result = self._values.get("gcs_source")
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceGcsSource"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#id GoogleMemorystoreInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Labels to represent user-provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#labels GoogleMemorystoreInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def maintenance_policy(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstanceMaintenancePolicy"]:
        '''maintenance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#maintenance_policy GoogleMemorystoreInstance#maintenance_policy}
        '''
        result = self._values.get("maintenance_policy")
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceMaintenancePolicy"], result)

    @builtins.property
    def managed_backup_source(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstanceManagedBackupSource"]:
        '''managed_backup_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#managed_backup_source GoogleMemorystoreInstance#managed_backup_source}
        '''
        result = self._values.get("managed_backup_source")
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceManagedBackupSource"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Optional. cluster or cluster-disabled.   Possible values:  CLUSTER  CLUSTER_DISABLED Possible values: ["CLUSTER", "CLUSTER_DISABLED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#mode GoogleMemorystoreInstance#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Machine type for individual nodes of the instance.   Possible values:  SHARED_CORE_NANO HIGHMEM_MEDIUM HIGHMEM_XLARGE STANDARD_SMALL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#node_type GoogleMemorystoreInstance#node_type}
        '''
        result = self._values.get("node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def persistence_config(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstancePersistenceConfig"]:
        '''persistence_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#persistence_config GoogleMemorystoreInstance#persistence_config}
        '''
        result = self._values.get("persistence_config")
        return typing.cast(typing.Optional["GoogleMemorystoreInstancePersistenceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#project GoogleMemorystoreInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Optional. Number of replica nodes per shard. If omitted the default is 0 replicas.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#replica_count GoogleMemorystoreInstance#replica_count}
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleMemorystoreInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#timeouts GoogleMemorystoreInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceTimeouts"], result)

    @builtins.property
    def transit_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Immutable. In-transit encryption mode of the instance.   Possible values:  TRANSIT_ENCRYPTION_DISABLED SERVER_AUTHENTICATION.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#transit_encryption_mode GoogleMemorystoreInstance#transit_encryption_mode}
        '''
        result = self._values.get("transit_encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_distribution_config(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstanceZoneDistributionConfig"]:
        '''zone_distribution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#zone_distribution_config GoogleMemorystoreInstance#zone_distribution_config}
        '''
        result = self._values.get("zone_distribution_config")
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceZoneDistributionConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "instance_role": "instanceRole",
        "primary_instance": "primaryInstance",
        "secondary_instances": "secondaryInstances",
    },
)
class GoogleMemorystoreInstanceCrossInstanceReplicationConfig:
    def __init__(
        self,
        *,
        instance_role: typing.Optional[builtins.str] = None,
        primary_instance: typing.Optional[typing.Union["GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param instance_role: The instance role supports the following values: 1. 'INSTANCE_ROLE_UNSPECIFIED': This is an independent instance that has never participated in cross instance replication. It allows both reads and writes. 2. 'NONE': This is an independent instance that previously participated in cross instance replication(either as a 'PRIMARY' or 'SECONDARY' cluster). It allows both reads and writes. 3. 'PRIMARY': This instance serves as the replication source for secondary instance that are replicating from it. Any data written to it is automatically replicated to its secondary clusters. It allows both reads and writes. 4. 'SECONDARY': This instance replicates data from the primary instance. It allows only reads. Possible values: ["INSTANCE_ROLE_UNSPECIFIED", "NONE", "PRIMARY", "SECONDARY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#instance_role GoogleMemorystoreInstance#instance_role}
        :param primary_instance: primary_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#primary_instance GoogleMemorystoreInstance#primary_instance}
        :param secondary_instances: secondary_instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#secondary_instances GoogleMemorystoreInstance#secondary_instances}
        '''
        if isinstance(primary_instance, dict):
            primary_instance = GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance(**primary_instance)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c34ba5741eebbc05a98dc02a7d562e652232468bde9d58858bdccb6d2dac07a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#instance_role GoogleMemorystoreInstance#instance_role}
        '''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_instance(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance"]:
        '''primary_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#primary_instance GoogleMemorystoreInstance#primary_instance}
        '''
        result = self._values.get("primary_instance")
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance"], result)

    @builtins.property
    def secondary_instances(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances"]]]:
        '''secondary_instances block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#secondary_instances GoogleMemorystoreInstance#secondary_instances}
        '''
        result = self._values.get("secondary_instances")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceCrossInstanceReplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembership",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembership:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembership(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97811c011cffd462bd1af5002ec34e8fb664519ba4f088593e21df4bee42d543)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3be0758356f24831fe77dc0b661cea15d7a531f7a3be38c76d34f3031d62ee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87714a5ba47b74b395ac15490cd916482469c9c2f1d615654ca1a69809d45b58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fe7a7aa90c8d137c91b70f220fcd5b8705906c742182ec4f67e656c09985c38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bac313c5c7e0ff105fd60d827943e57a6c1f019fb5b8a085d79f3b10fede7aad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8831171f594bcfb458f13ae8a8ebca2cf6598b7f1089aa8e5a17963805e35a40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="primaryInstance")
    def primary_instance(
        self,
    ) -> "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceList":
        return typing.cast("GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceList", jsii.get(self, "primaryInstance"))

    @builtins.property
    @jsii.member(jsii_name="secondaryInstance")
    def secondary_instance(
        self,
    ) -> "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceList":
        return typing.cast("GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceList", jsii.get(self, "secondaryInstance"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembership]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembership], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembership],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f3cc57a13de012237ee0a1c6ef5427636efaebd30a6da1e5b04db584e403bdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96e752065fb0e7e7e9472ca4e2605cbe71ef39a451d4485637fb9956cbe51baa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da61dcc2178288705fe84eedc779f99f56f83bfb8a6243dfc3dc373e2d7099b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5204fb7f5bed75b7e14e0159caa0a4b8633e36dfb7c6316833378f1ce41cc783)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e71cc9f94e78d6827eb1b3bfd2adf9df8a100d3afdff23f2ab96a4469846971d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f7730968d8f258daec2dca8dbb8524fa0f14e6f50b836c6c260dde1b384bc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8b33f0ac687677c3430bcf6e12e63b6ed4b234573c169c83747e6da3e270bf6)
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
    ) -> typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837d5df143f327fa35f102dcf5c86cbcd779aa1f18957083a361bb51f0519f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06f7aa1c6a2c9df7ed52260559c65e02c754317b74e3884ecb1726f8fcdd6e57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6539f4255d605cedbc7153acf9c4eb57bd124d74cc5625b1c0acfddc7efc49b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02ffc152535c27e119e736191193d02be157e9acd8839ac5f84ab6a5ea4158b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b834cbcaeb011084d66782ec9e87caa713ecb5fafa56d0ded36ff96f944f079c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4df857977a4d7ed3a7dce1bad4e82a532b0c1869db007a49a7c863e49c8670e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__644f0b0922370f5c1c005eddb735606d5a5e296d6e3d0bdb5981e84e86cc1613)
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
    ) -> typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2387f244cf1f7e010be237cf208675026b1d68e7f9e67eb8acc8c27ab7572d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceCrossInstanceReplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da70f0c318aa6e5d4d96ba31cb14d62512db7ac7e426de7a928995e2ac394d56)
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
        :param instance: The full resource path of the primary instance in the format: projects/{project}/locations/{region}/instances/{instance-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#instance GoogleMemorystoreInstance#instance}
        '''
        value = GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance(
            instance=instance
        )

        return typing.cast(None, jsii.invoke(self, "putPrimaryInstance", [value]))

    @jsii.member(jsii_name="putSecondaryInstances")
    def put_secondary_instances(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4f466351aeeef812f8f0ab75b17dda39668027e22536025944b39300d256b0)
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
    ) -> GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipList:
        return typing.cast(GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipList, jsii.get(self, "membership"))

    @builtins.property
    @jsii.member(jsii_name="primaryInstance")
    def primary_instance(
        self,
    ) -> "GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstanceOutputReference":
        return typing.cast("GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstanceOutputReference", jsii.get(self, "primaryInstance"))

    @builtins.property
    @jsii.member(jsii_name="secondaryInstances")
    def secondary_instances(
        self,
    ) -> "GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesList":
        return typing.cast("GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesList", jsii.get(self, "secondaryInstances"))

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
    ) -> typing.Optional["GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance"]:
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance"], jsii.get(self, "primaryInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryInstancesInput")
    def secondary_instances_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances"]]], jsii.get(self, "secondaryInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceRole")
    def instance_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceRole"))

    @instance_role.setter
    def instance_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d5c9afc2f3f068610ead4d6066e10f642450db7606b241b49490051554f653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfig]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ab9e7556992c40e62de9729f94408bf7c7aa40fb057163236cb5d698f20085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance",
    jsii_struct_bases=[],
    name_mapping={"instance": "instance"},
)
class GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance:
    def __init__(self, *, instance: typing.Optional[builtins.str] = None) -> None:
        '''
        :param instance: The full resource path of the primary instance in the format: projects/{project}/locations/{region}/instances/{instance-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#instance GoogleMemorystoreInstance#instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ab7a2439132e81dfbf69f1606ce9a698721006d5ec6e162199f37965eb3f66)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance is not None:
            self._values["instance"] = instance

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''The full resource path of the primary instance in the format: projects/{project}/locations/{region}/instances/{instance-id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#instance GoogleMemorystoreInstance#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dae2238e362b55f860df9db62bfedce7f0bc2d5f8a441dddbc11b3dc5edc474)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28d92a65e71e7174efc65247339138ae32e10c37ece4c8a2f686b86ccf9599ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ebc98f1771ae7cc3407f4da8d088acaa8ae4d0b27dd368630d1e0ddbb1c2f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances",
    jsii_struct_bases=[],
    name_mapping={"instance": "instance"},
)
class GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances:
    def __init__(self, *, instance: typing.Optional[builtins.str] = None) -> None:
        '''
        :param instance: The full resource path of the Nth instance in the format: projects/{project}/locations/{region}/instance/{instance-id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#instance GoogleMemorystoreInstance#instance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2f67eb82db0e253302dc1150bb98e230a58fcbae52b19f4239609840c08eb2)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance is not None:
            self._values["instance"] = instance

    @builtins.property
    def instance(self) -> typing.Optional[builtins.str]:
        '''The full resource path of the Nth instance in the format: projects/{project}/locations/{region}/instance/{instance-id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#instance GoogleMemorystoreInstance#instance}
        '''
        result = self._values.get("instance")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94133763169d846902ce189efdaa802b78167aabdc299ae223aaeadcc4676076)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53147cd08e77d29d1df3b46a72479f01243a9283c11e51f3aeb87dbbd969df6f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5119cf0314b481f12fc522a5a2b905fff633ec29e81c92321f8fd8a3cb3f451d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05f0ed16f91a3ea9abf4ce28fab079b755eb77d6cc2eea614e01c55ab3bab819)
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
            type_hints = typing.get_type_hints(_typecheckingstub__061d17da07b6fa73615c1a38e65cc85a810fa81dae52b41006c1818251ef42ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ba7ee447941aad4f0110968f376768c2164772a9956d73fb7aff8536abd810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd449bdec4fac12564c66a314723f095f79c9a540e799ed8b7b826fb95401d56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b95162305a06f0d67250816dd88329991c7e29062c65e535d485c3d51225f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65da1a605fac5fa0f443e6850b07f1a3cf090147117d0ca8fb2028bcb2e39c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "project_id": "projectId"},
)
class GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints:
    def __init__(self, *, network: builtins.str, project_id: builtins.str) -> None:
        '''
        :param network: Required. The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#network GoogleMemorystoreInstance#network}
        :param project_id: Required. The consumer project_id where the forwarding rule is created from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#project_id GoogleMemorystoreInstance#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dfee3bc4f92f7060edde946e019672b2d3e603fc544c36d0d01b9bbc1e7e6dd)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network": network,
            "project_id": project_id,
        }

    @builtins.property
    def network(self) -> builtins.str:
        '''Required. The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#network GoogleMemorystoreInstance#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Required. The consumer project_id where the forwarding rule is created from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#project_id GoogleMemorystoreInstance#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceDesiredAutoCreatedEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceDesiredAutoCreatedEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b727fd0714ac14fc68c06af2e672c319024a702584fe53bd5d5b5289ed34397)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceDesiredAutoCreatedEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1db69cd3a88b7fb212c1b5723d0e2c4225b3556cbc071822f01fb82b6a4886)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceDesiredAutoCreatedEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291bc8b83cbaed6873a6327608cd7638099b7189312f97f80e37151125d0b955)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d6fa9f9c7b746a241a04dcf1cb821849492d8e35562e6a4c7391bbfbd3367d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__399c98fba7ccd70041b2a5ffb8f4200d3e3ce1d66ebed887009ed178aaf7c86a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1393e3bc33daf5b20660b2ca52c5f97597b31ca9952e638cebf18c7c52a6c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceDesiredAutoCreatedEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceDesiredAutoCreatedEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae9d733ae60ebec296fa485ed61fcbf7d62b94b4f9aa14fd54b398066cef61e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c6dd5968fbf6d6dceabc5a693efdc97a2010ddfbf26c26d887b755a9ed310b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65998c768ea5a014f89a577bd7e520ea754fc740c7929ae50d5b0c0aa31a6cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889ea2da1f15f254dc1c9e0c018dbb1fb4cb25ea1b18b23530bb202520166c9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceDesiredPscAutoConnections",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "project_id": "projectId"},
)
class GoogleMemorystoreInstanceDesiredPscAutoConnections:
    def __init__(self, *, network: builtins.str, project_id: builtins.str) -> None:
        '''
        :param network: Required. The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#network GoogleMemorystoreInstance#network}
        :param project_id: Required. The consumer project_id where the forwarding rule is created from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#project_id GoogleMemorystoreInstance#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96fe009dcaaae2395d2f3eb79a43c50d9d919dd3a746012335dea9402642e1ab)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network": network,
            "project_id": project_id,
        }

    @builtins.property
    def network(self) -> builtins.str:
        '''Required. The consumer network where the IP address resides, in the form of projects/{project_id}/global/networks/{network_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#network GoogleMemorystoreInstance#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Required. The consumer project_id where the forwarding rule is created from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#project_id GoogleMemorystoreInstance#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceDesiredPscAutoConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceDesiredPscAutoConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceDesiredPscAutoConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2258319408fa649e917c100772b06133c6a3d082c876c37b890af104f24a157c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceDesiredPscAutoConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35367ebde1fd66cd0d539285e70e6437630c49dc6d797aad012b817724c78ced)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceDesiredPscAutoConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5607ff1a928929f0e10c8325567acc6d6ee7bb929a13d793c1ae87bf3ad6c1b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f79797e730667040b333edf37c63afa7cf1684e7d7ed7833659e07de4be34ca8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d2c71468d7a2c8d50511e5ac89c31a9601578f46730ddfd9be3eb571987bbbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceDesiredPscAutoConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceDesiredPscAutoConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceDesiredPscAutoConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83de38f13022974d825d900f2f4a75c8133904051d53c82847a569f81a5cc852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceDesiredPscAutoConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceDesiredPscAutoConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45e10cd1e27d4c9bf748e7ef04db47e53e2222f928edfe27cc01924ff9cb9dc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc57a6a3fe691ffac8533e814656542204af0c3da9b6fb69106f63d18d3509e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1daac4ea91668480d18c09d236abf64b70458244a0be2305195c361d5d4f5de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceDesiredPscAutoConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceDesiredPscAutoConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceDesiredPscAutoConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0472c179fe7e3c05779e7e66735fd87717c2a737dc5be603fb66a61eb3c02a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceDiscoveryEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstanceDiscoveryEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceDiscoveryEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceDiscoveryEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceDiscoveryEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff16deec2d9fbcb5547fc2334f1218a3cb7cf5f2862bbf2a8b22ffd2bcb194e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceDiscoveryEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca121f92865130c2f4c0ab6eb313a4c6320a42ac8e952ddee4439dd8b46268a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceDiscoveryEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c0d99ed4782e30302017b932ef4f26b127b5dedab16aa47b7111e937939a97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e53fc8a84352e92cff06943ba8c8e7a1314b7fe65a02dff4bd49a0186a4e7250)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a19f1eda252454f7f433142d856d85a7be6575b7d43a236f48bc2aa3edb45fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceDiscoveryEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceDiscoveryEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a256f190a628b98a87d2cad17aa7ed9e025436b37a6b972d5d9bdc7c7fdf550c)
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
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceDiscoveryEndpoints]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceDiscoveryEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceDiscoveryEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ac040c0ce609cf4c4f746d49a4c4e57eef861cdbd5d97363996b9678b18715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstanceEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceEndpointsConnections",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstanceEndpointsConnections:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceEndpointsConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceEndpointsConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceEndpointsConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9568a29dd38d4b950e7c7810f132fec337c63fca7cc733f7f8d545c3714a2001)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceEndpointsConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0740b7875d6e2984c2be1144af204cb9b3b2342181e95a2ba884826de163c365)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceEndpointsConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea1e65d057a3cbd765a23c11db1ac2cfe49985305f69fe423f446c459789b17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bb9544f5e54f8cdc5573ce68a4f2a2dba6379c1f17c0508616b47cbc536a275)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53b75ce8eda45651aef755668367e7a97c433e5c9338606437b4e5609a0ddb04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceEndpointsConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceEndpointsConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__863883210cdcc83adaf039999b85dd8f6c1a95a18c4ad588f507284def193390)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pscAutoConnection")
    def psc_auto_connection(
        self,
    ) -> "GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnectionList":
        return typing.cast("GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnectionList", jsii.get(self, "pscAutoConnection"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceEndpointsConnections]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceEndpointsConnections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceEndpointsConnections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2921b2651c16a3c15230a7a8a27a1acccdf034ae4048253374f33c3b5d10bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnection",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnection:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnectionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnectionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c29466c3fb2bdb74ca4343c124479a3f354688a0cdbdc56915b3a82cc163d95c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnectionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__833342c6befa4c88460b2e2189a45f5628f12a5bc26e7d9c3f4ceaeca88c78bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnectionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f470b4d9444acac6033c7bb23d151a86d3933c78e093452ce1010c7d940e0321)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d049d698e126b558f64009582e73f5e3113725266fd08f9665a2504600ebbca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3026279fdb80abde1266dfd61b05b6d52419f70d8fd576e0b2c7dfc37786ff3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9a8ba00c31865ad4f50c8bcdf21ee67d751b77b15f35ecb621114e20614537c)
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
    ) -> typing.Optional[GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnection]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0541a1c79a3eac3f439639c9c0dee60e50b1fd962ec0e7c6e6d0cd8b2b1e41fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a41017858c1457ad14da9bfb8b6b07bf21ea0d8707b93b1c1717a7f6dce827f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375a82195dd0aeb0c3645129e1d64d8d5cffc8e243ae3a014d7cffd2a9ad589e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c70d4e101f3b29543cda0c7049eb9b07ebd9148cf319701e49dd5d961351662)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dbe06db4641248caa617ea90afcbadcc5d2ed23021a87cb82aff56970d816fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47c8c645901a31fe640e65594299928cd736f82afac1ee9429bc577e7d1c8e82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88289e12829f73cc6a62a8dc5394f385726cac82e3fcb825d405c04404bc94dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> GoogleMemorystoreInstanceEndpointsConnectionsList:
        return typing.cast(GoogleMemorystoreInstanceEndpointsConnectionsList, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleMemorystoreInstanceEndpoints]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499291a072579853474b6742bab09f92a8886313078386d0a9c9e12987685eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceGcsSource",
    jsii_struct_bases=[],
    name_mapping={"uris": "uris"},
)
class GoogleMemorystoreInstanceGcsSource:
    def __init__(self, *, uris: typing.Sequence[builtins.str]) -> None:
        '''
        :param uris: URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#uris GoogleMemorystoreInstance#uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811d4aa1e64d09152f4085c17b79a5f721a668b06167aa1ec93dc44fed81c894)
            check_type(argname="argument uris", value=uris, expected_type=type_hints["uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uris": uris,
        }

    @builtins.property
    def uris(self) -> typing.List[builtins.str]:
        '''URIs of the GCS objects to import. Example: gs://bucket1/object1, gs://bucket2/folder2/object2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#uris GoogleMemorystoreInstance#uris}
        '''
        result = self._values.get("uris")
        assert result is not None, "Required property 'uris' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceGcsSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceGcsSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceGcsSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0eba63426da041f89cd25974f203006ca642ec6007bb60381c5b3c92f68b4d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2463eabad05d285a1e7c4ee31224ef239d7ad6c245492011ec391f755a4d1a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleMemorystoreInstanceGcsSource]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceGcsSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceGcsSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be5190d27d06d6ee7ddc9e0441da053cf3dbf0a5de0a4d07e302edd9842cb491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceMaintenancePolicy",
    jsii_struct_bases=[],
    name_mapping={"weekly_maintenance_window": "weeklyMaintenanceWindow"},
)
class GoogleMemorystoreInstanceMaintenancePolicy:
    def __init__(
        self,
        *,
        weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#weekly_maintenance_window GoogleMemorystoreInstance#weekly_maintenance_window}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65055eb2b52d57c6d3eda89f29f90eab18a63188103065273953f433b789705)
            check_type(argname="argument weekly_maintenance_window", value=weekly_maintenance_window, expected_type=type_hints["weekly_maintenance_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if weekly_maintenance_window is not None:
            self._values["weekly_maintenance_window"] = weekly_maintenance_window

    @builtins.property
    def weekly_maintenance_window(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]]:
        '''weekly_maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#weekly_maintenance_window GoogleMemorystoreInstance#weekly_maintenance_window}
        '''
        result = self._values.get("weekly_maintenance_window")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceMaintenancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceMaintenancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceMaintenancePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e2408721f4d76afcd9eb873531df1ccc724901c107add69ce49f4fa7f9d6b3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWeeklyMaintenanceWindow")
    def put_weekly_maintenance_window(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859a629e68e32c634468c441247344402a2b75443029c15c94f9cba31cb702cf)
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
    ) -> "GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowList":
        return typing.cast("GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowList", jsii.get(self, "weeklyMaintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="weeklyMaintenanceWindowInput")
    def weekly_maintenance_window_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]], jsii.get(self, "weeklyMaintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceMaintenancePolicy]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceMaintenancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceMaintenancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1be72a667e991e16e0c55c5c81009b8ee31981a2ae07753099fe9da3b5b3e6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "start_time": "startTime"},
)
class GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow:
    def __init__(
        self,
        *,
        day: builtins.str,
        start_time: typing.Union["GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day: The day of week that maintenance updates occur. - DAY_OF_WEEK_UNSPECIFIED: The day of the week is unspecified. - MONDAY: Monday - TUESDAY: Tuesday - WEDNESDAY: Wednesday - THURSDAY: Thursday - FRIDAY: Friday - SATURDAY: Saturday - SUNDAY: Sunday Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#day GoogleMemorystoreInstance#day}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#start_time GoogleMemorystoreInstance#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba2703bcf84e71b0c9ebdd254a6717b81aaf9b4d6ee1b43aa6b7d186a4e0472)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#day GoogleMemorystoreInstance#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(
        self,
    ) -> "GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#start_time GoogleMemorystoreInstance#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06459100b69f521ae959cd90993f2dcf05f2df1427772922104dac6ccd2871bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9805bf52e5c543137418de1423044123a18e1516c87b653d9daff0b56b12480)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284cab7386e8c5fd827951e2f573fb73baa6da54fbd5c63632e2af65f425ca72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0032999627d26c4ce5ad8334e5d6a4026d2f60d80f4c53a3c84a25345eb9ef0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__faf47653d8646e856a813d07385c7e97101026f1ef1b45c71def49ba9f93b2a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a1479c9e420d091c66ccfd24d3456f2ef1b9f9f305e4183291192ed6a3138b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47eb7cc11afeefc2a0e6a98e0d90601e08e8602d05103f9f262c6170b3c6e38e)
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
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#hours GoogleMemorystoreInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#minutes GoogleMemorystoreInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#nanos GoogleMemorystoreInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#seconds GoogleMemorystoreInstance#seconds}
        '''
        value = GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(
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
    ) -> "GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference":
        return typing.cast("GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime"]:
        return typing.cast(typing.Optional["GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37084fcbb2769561552a0df1ba8a6500a79975ca4d58c9a21aace5faff002a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4baf9e49073031ef425097e3a07c7dec59b623bfcd1e21cdcd4915c804b84645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#hours GoogleMemorystoreInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#minutes GoogleMemorystoreInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#nanos GoogleMemorystoreInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#seconds GoogleMemorystoreInstance#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d840b20250651eeacb9e3df99fe043bb395669a2103362c1b103003a6b9ffb2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#hours GoogleMemorystoreInstance#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#minutes GoogleMemorystoreInstance#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#nanos GoogleMemorystoreInstance#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time.

        Must normally be from 0 to 59.
        An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#seconds GoogleMemorystoreInstance#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ef836ca9994a1575de8bf5c92deb635bba1c12e819df387cfffa29e59ac205f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1557b98d773de75c0f63c64f25c4401cf16f187b3722850bd6b81caaea9a04d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c6473c39e49e2886cb52e5b02f0e21f211e580b64c24a175c3d8c6ea88b9f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76a32dee6fbd75c5b5b167134b144e31899c495ccfe6c04c2e9891bea3234bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f7f9cf2f429038455501a2c34daf9e0ec644c9c878aa42653fcd63b6c8a699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ec3e61dea9714c3fb59f14bd492ce083de1aca3c41b374f3c4cd9b63bd9a2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceMaintenanceSchedule",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstanceMaintenanceSchedule:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceMaintenanceSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceMaintenanceScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceMaintenanceScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2493de11762e91f124bf763b787110ea3183287a3f69c08796332ee949639c95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceMaintenanceScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f67ba81ea2a06cb7dd7308d20aa619cd2cb4b985c765577deb9585a703dcfb6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceMaintenanceScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f730f1faa216387bcc1f3ea1916d8e37781903dc1fed22665f7093a7a0a6e540)
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
            type_hints = typing.get_type_hints(_typecheckingstub__016ae70fd29e43bb3632140ed9639cc2454d4ef8f08899d83be311bd976e99ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60e87efb9cdffb3c2fe70def00987812871aa2dba877bcd00452051924a3548a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceMaintenanceScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceMaintenanceScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f6502e607858422476bf59b70cc19725b224cf9e4e80ed71c18f8daf46c762f)
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
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceMaintenanceSchedule]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceMaintenanceSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceMaintenanceSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2fa043247346a3e17b0196815a3436a0eb75279efd709601ee0f98edad4a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceManagedBackupSource",
    jsii_struct_bases=[],
    name_mapping={"backup": "backup"},
)
class GoogleMemorystoreInstanceManagedBackupSource:
    def __init__(self, *, backup: builtins.str) -> None:
        '''
        :param backup: Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#backup GoogleMemorystoreInstance#backup}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc04766ee94e39bef5029a4af630fd93add78641c7f9491f2a5ff086ef6a950)
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup": backup,
        }

    @builtins.property
    def backup(self) -> builtins.str:
        '''Example: 'projects/{project}/locations/{location}/backupCollections/{collection}/backups/{backup}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#backup GoogleMemorystoreInstance#backup}
        '''
        result = self._values.get("backup")
        assert result is not None, "Required property 'backup' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceManagedBackupSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceManagedBackupSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceManagedBackupSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1185fe5aa0ebff2329b8ba1ac61e37e0d6f07d451b6fa9f7fdcf28a93598bf62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe00ccd5cea9b90dac1d5cfbf33ad0c4ef5121acd73a8d6f57dd477333f5b327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceManagedBackupSource]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceManagedBackupSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceManagedBackupSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdbf34cddd9b52b814b009c505ecda29162daefdc135ca383d55f3bdd662c678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceNodeConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstanceNodeConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceNodeConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceNodeConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff042f6405223091ddcc3e4e18108f1284059312c2a97da2c5814d5cc333904a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceNodeConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac452a2f9f66993a83ee31ff14dedeb8b66ba5aec51cecdc7aadb03407aaad4b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceNodeConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383da695e3c86790e8fddfaf9ce687aede2d11fd88bff57ca850e106b096527f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8efeef52a570450114d6f3e84f2c6cea9b7dc5e48b6e5aa2937bc7e5f1b4e8df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__421485cb59fc888bb732ddcf609eedce2295ed556b1b294108b8888ecee7c209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceNodeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a89c5d018c7d3a99e79778f2a93347c035b6b7d977192755fe5b99079660d844)
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
    def internal_value(self) -> typing.Optional[GoogleMemorystoreInstanceNodeConfig]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90aa3495699f5307671e4697df4a7661a852bffbb58b6bb345b9a5546309b7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePersistenceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aof_config": "aofConfig",
        "mode": "mode",
        "rdb_config": "rdbConfig",
    },
)
class GoogleMemorystoreInstancePersistenceConfig:
    def __init__(
        self,
        *,
        aof_config: typing.Optional[typing.Union["GoogleMemorystoreInstancePersistenceConfigAofConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        rdb_config: typing.Optional[typing.Union["GoogleMemorystoreInstancePersistenceConfigRdbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aof_config: aof_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#aof_config GoogleMemorystoreInstance#aof_config}
        :param mode: Optional. Current persistence mode. Possible values: DISABLED RDB AOF Possible values: ["DISABLED", "RDB", "AOF"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#mode GoogleMemorystoreInstance#mode}
        :param rdb_config: rdb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#rdb_config GoogleMemorystoreInstance#rdb_config}
        '''
        if isinstance(aof_config, dict):
            aof_config = GoogleMemorystoreInstancePersistenceConfigAofConfig(**aof_config)
        if isinstance(rdb_config, dict):
            rdb_config = GoogleMemorystoreInstancePersistenceConfigRdbConfig(**rdb_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14edb3c061778a59bf5ee457423a6e96abfa8c80a6e9ccf96e864d35416825bf)
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
    ) -> typing.Optional["GoogleMemorystoreInstancePersistenceConfigAofConfig"]:
        '''aof_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#aof_config GoogleMemorystoreInstance#aof_config}
        '''
        result = self._values.get("aof_config")
        return typing.cast(typing.Optional["GoogleMemorystoreInstancePersistenceConfigAofConfig"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Current persistence mode.   Possible values: DISABLED RDB AOF Possible values: ["DISABLED", "RDB", "AOF"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#mode GoogleMemorystoreInstance#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_config(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstancePersistenceConfigRdbConfig"]:
        '''rdb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#rdb_config GoogleMemorystoreInstance#rdb_config}
        '''
        result = self._values.get("rdb_config")
        return typing.cast(typing.Optional["GoogleMemorystoreInstancePersistenceConfigRdbConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstancePersistenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePersistenceConfigAofConfig",
    jsii_struct_bases=[],
    name_mapping={"append_fsync": "appendFsync"},
)
class GoogleMemorystoreInstancePersistenceConfigAofConfig:
    def __init__(self, *, append_fsync: typing.Optional[builtins.str] = None) -> None:
        '''
        :param append_fsync: Optional. The fsync mode. Possible values: NEVER EVERY_SEC ALWAYS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#append_fsync GoogleMemorystoreInstance#append_fsync}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__677fa95b1dbedcab77135eb7cc86faf12adf4d0ab9efc84dd20a0cace0881a99)
            check_type(argname="argument append_fsync", value=append_fsync, expected_type=type_hints["append_fsync"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if append_fsync is not None:
            self._values["append_fsync"] = append_fsync

    @builtins.property
    def append_fsync(self) -> typing.Optional[builtins.str]:
        '''Optional. The fsync mode.   Possible values:  NEVER EVERY_SEC ALWAYS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#append_fsync GoogleMemorystoreInstance#append_fsync}
        '''
        result = self._values.get("append_fsync")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstancePersistenceConfigAofConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstancePersistenceConfigAofConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePersistenceConfigAofConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4ef669426cb2aa661c651b027e201c471c2c2ea6c57f7737c0d9e5b130930a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e15a1601ad5f7ae990fdcc3b0429632ea4ccf2dc2397c07e1d8e8490770abec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appendFsync", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstancePersistenceConfigAofConfig]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstancePersistenceConfigAofConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstancePersistenceConfigAofConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45aa49ee3d9d5b628199376e70bf6ad53f0cadc5dd2f6e00f97dd331628c70b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstancePersistenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePersistenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58947915106a304d88883a8989a5282ca7534e4710a28d363ee54d21255d7de3)
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
        :param append_fsync: Optional. The fsync mode. Possible values: NEVER EVERY_SEC ALWAYS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#append_fsync GoogleMemorystoreInstance#append_fsync}
        '''
        value = GoogleMemorystoreInstancePersistenceConfigAofConfig(
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
        :param rdb_snapshot_period: Optional. Period between RDB snapshots. Possible values: ONE_HOUR SIX_HOURS TWELVE_HOURS TWENTY_FOUR_HOURS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#rdb_snapshot_period GoogleMemorystoreInstance#rdb_snapshot_period}
        :param rdb_snapshot_start_time: Optional. Time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#rdb_snapshot_start_time GoogleMemorystoreInstance#rdb_snapshot_start_time}
        '''
        value = GoogleMemorystoreInstancePersistenceConfigRdbConfig(
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
    ) -> GoogleMemorystoreInstancePersistenceConfigAofConfigOutputReference:
        return typing.cast(GoogleMemorystoreInstancePersistenceConfigAofConfigOutputReference, jsii.get(self, "aofConfig"))

    @builtins.property
    @jsii.member(jsii_name="rdbConfig")
    def rdb_config(
        self,
    ) -> "GoogleMemorystoreInstancePersistenceConfigRdbConfigOutputReference":
        return typing.cast("GoogleMemorystoreInstancePersistenceConfigRdbConfigOutputReference", jsii.get(self, "rdbConfig"))

    @builtins.property
    @jsii.member(jsii_name="aofConfigInput")
    def aof_config_input(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstancePersistenceConfigAofConfig]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstancePersistenceConfigAofConfig], jsii.get(self, "aofConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbConfigInput")
    def rdb_config_input(
        self,
    ) -> typing.Optional["GoogleMemorystoreInstancePersistenceConfigRdbConfig"]:
        return typing.cast(typing.Optional["GoogleMemorystoreInstancePersistenceConfigRdbConfig"], jsii.get(self, "rdbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178f67a7427a3dec45c99deeb6cb61fad3371acfbd22ecfd90782a4c5e066539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstancePersistenceConfig]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstancePersistenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstancePersistenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e0b640885cd612d55a4883669ce4a128a3a1206682b2a4d8620870da6b4bfa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePersistenceConfigRdbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "rdb_snapshot_period": "rdbSnapshotPeriod",
        "rdb_snapshot_start_time": "rdbSnapshotStartTime",
    },
)
class GoogleMemorystoreInstancePersistenceConfigRdbConfig:
    def __init__(
        self,
        *,
        rdb_snapshot_period: typing.Optional[builtins.str] = None,
        rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rdb_snapshot_period: Optional. Period between RDB snapshots. Possible values: ONE_HOUR SIX_HOURS TWELVE_HOURS TWENTY_FOUR_HOURS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#rdb_snapshot_period GoogleMemorystoreInstance#rdb_snapshot_period}
        :param rdb_snapshot_start_time: Optional. Time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#rdb_snapshot_start_time GoogleMemorystoreInstance#rdb_snapshot_start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2c7d61a5a0f397875e49dea11e2b0fa3ebe09e2e7e6ef792ee58559aed6a48)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#rdb_snapshot_period GoogleMemorystoreInstance#rdb_snapshot_period}
        '''
        result = self._values.get("rdb_snapshot_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_snapshot_start_time(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Time that the first snapshot was/will be attempted, and to which future
        snapshots will be aligned. If not provided, the current time will be
        used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#rdb_snapshot_start_time GoogleMemorystoreInstance#rdb_snapshot_start_time}
        '''
        result = self._values.get("rdb_snapshot_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstancePersistenceConfigRdbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstancePersistenceConfigRdbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePersistenceConfigRdbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed578c00951e7aa332ff482981b8294d12313bb1ae618f4ebf82b6310610ef25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39fef34c4fd70d45caee0e6675f34ebed5215da45f560acb07461f1349d3d5ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotStartTime")
    def rdb_snapshot_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdbSnapshotStartTime"))

    @rdb_snapshot_start_time.setter
    def rdb_snapshot_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e81a005381ab5047efd471a5a530dfb32acbef1991004b9dfacd47f09dd160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstancePersistenceConfigRdbConfig]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstancePersistenceConfigRdbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstancePersistenceConfigRdbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad2674bed6bcfd0f91be76dc0cbe24d4d4b707c0af774bb7f9189f9db3cb6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePscAttachmentDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstancePscAttachmentDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstancePscAttachmentDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstancePscAttachmentDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePscAttachmentDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99238f2a90ca24307d3a19f1a0bec06aa8208477bd4ab01f10c97f3635f6fe69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstancePscAttachmentDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d975a524082a70b51f97bd6d7cc982281771a213e03350ed0e9ac2268cd834d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstancePscAttachmentDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccdea6a6c457a695d50ddbb72ddb8f7cdd4dc501219ce8c8d74988079835eb47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ab0aca6b3270183b88cf5bfbf867ae935d639c43072c7d2c5b49669a4c067c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8a11ea56115bf78181a0e8489c8a96a655a980f294db367469464a59f0780cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstancePscAttachmentDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePscAttachmentDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24902ce32d0d7dba2f8d18e46a36f7f7d9de7751dae4c0ce279706c1a1b8c91c)
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
    ) -> typing.Optional[GoogleMemorystoreInstancePscAttachmentDetails]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstancePscAttachmentDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstancePscAttachmentDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b2960c5cd04f34ec5eb34f750f512b9ce5e7656c7e234b17836f939a644666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePscAutoConnections",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstancePscAutoConnections:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstancePscAutoConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstancePscAutoConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePscAutoConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2820bb35714e1fde4f07ba7cb6a267aa4fdc651b91be415301b7953127c7e3f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstancePscAutoConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a468077a31186a1a463409bf145247f7a1814f84b4a0eb3c20a272aac7343a4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstancePscAutoConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762d8ba519a4bb1b7014a12c4e33dd4c5b0f1209ca5fb8c802d5db64ffd349db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12e72b7137d0a35341259e22ae10f97b17e5a8d58c07c6ba63dbc5e9e615cb23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__351a482b277b99852fd5ec1156466d3ac7e50dd280278f59da84b5ddd7d29287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstancePscAutoConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstancePscAutoConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__956f1d1de32b6c632fa3be04f97823047b79a3a20331ebb12972bd7f7dc69d68)
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
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstancePscAutoConnections]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstancePscAutoConnections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstancePscAutoConnections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0097b8605cf24d9144f8ff4a9c2603f03b0a819ea4abeaf7aeddba40afacde3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceStateInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstanceStateInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceStateInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceStateInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceStateInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3f6b9da1e92c9f1d3013452a9fa6d919e64aca99f3ca258677e0864898af542)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceStateInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12cb6738612c743f8e891d5df005180ae7c5541529c2df5ccbb23fd64fa9cb95)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceStateInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27d824cac024c98f5f9b1e454cde3a6d131b34f458b7002e2fae90b9a649b48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83a617a3752c8e30444f7d37302fc3d9fa7ee1a03d269668f2202aa92f6a30e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ad7ca64fa9a8f7075d8a10279284e56b457d19fafc41595b604b9d7438b77a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceStateInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceStateInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__061a3a3801f9b9e72f2105f80cf3545b23ce2c201fd2b618d053b1c9ddadf02e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="updateInfo")
    def update_info(self) -> "GoogleMemorystoreInstanceStateInfoUpdateInfoList":
        return typing.cast("GoogleMemorystoreInstanceStateInfoUpdateInfoList", jsii.get(self, "updateInfo"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleMemorystoreInstanceStateInfo]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceStateInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceStateInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f87b253e7c0a6e94c579c960d33742762662d9e7634966d55c841c841ffc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceStateInfoUpdateInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleMemorystoreInstanceStateInfoUpdateInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceStateInfoUpdateInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceStateInfoUpdateInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceStateInfoUpdateInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dfc1bdea7d126c4220d1bd5b680b3ff16515558cc4ef274ab0bf6b31716c3d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleMemorystoreInstanceStateInfoUpdateInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9259fd56c17299447bc088575af9bd3cb9ae5ed8d5dac089eb9034742edcdf2d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleMemorystoreInstanceStateInfoUpdateInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424d0da265e85d8bc9fb547f0b03475a6bb87f025ec03adfd909d0846f996d69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b49dec1a7800a8d8eee940a70c136a2bc4ac0025e92bcd56b7b7ab692566e78b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__678afc6a2e0df2b197e4123a7cba235edec45273bf2a5462f88db2083485794c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleMemorystoreInstanceStateInfoUpdateInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceStateInfoUpdateInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5ebf0436c4c3659a4edecfdb3aeeaefbdb67a364cfe35d2cd3de491c3c70b39)
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
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceStateInfoUpdateInfo]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceStateInfoUpdateInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceStateInfoUpdateInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327529be33725d0d96c6fa32ffa61aacd495d29d2d6c30a4172f3ac82172b72c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleMemorystoreInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#create GoogleMemorystoreInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#delete GoogleMemorystoreInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#update GoogleMemorystoreInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d51a5032c45297d624c220c5dabb700471db120dc31bdf17a81397eec41568f7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#create GoogleMemorystoreInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#delete GoogleMemorystoreInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#update GoogleMemorystoreInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4c85ded7591889831f5ae344b49e57d2f30dcd520c8a1f4d6d61e8747a375f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7a0e27366184c3e83ff575c0a52c7c2617531e5acc3d902d5ab6f23deabfede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4bd5527e75166a4399ff66d241e781daebd4f9769797467da5632d3f77249b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63df70880c47fea48040663b27ce990fb3c8a5991a96472c1282bdb8347f8a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1e53a46cfbe72f3ca1924cc173f7ffbb37f3dc789174dbcfb91ed2c257b2ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceZoneDistributionConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "zone": "zone"},
)
class GoogleMemorystoreInstanceZoneDistributionConfig:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Optional. Current zone distribution mode. Defaults to MULTI_ZONE. Possible values: MULTI_ZONE SINGLE_ZONE Possible values: ["MULTI_ZONE", "SINGLE_ZONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#mode GoogleMemorystoreInstance#mode}
        :param zone: Optional. Defines zone where all resources will be allocated with SINGLE_ZONE mode. Ignored for MULTI_ZONE mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#zone GoogleMemorystoreInstance#zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e90a7942959d61cd460de33c753a32d77772ce82776a75d1543bbb3d1de774e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#mode GoogleMemorystoreInstance#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Optional. Defines zone where all resources will be allocated with SINGLE_ZONE mode. Ignored for MULTI_ZONE mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_memorystore_instance#zone GoogleMemorystoreInstance#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleMemorystoreInstanceZoneDistributionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleMemorystoreInstanceZoneDistributionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleMemorystoreInstance.GoogleMemorystoreInstanceZoneDistributionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a244f6543a835da1a169bf613b9e5a0eb3df2b3e4e65728caa7df5d0e5542aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d83293e3acf7680062c58a5c97f32de595fed8c46008c073189e4da59ead26a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4999deb34286ee38a2c4cb516393e40d925a5fd98b43e9a837cb5a5ad19d3211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleMemorystoreInstanceZoneDistributionConfig]:
        return typing.cast(typing.Optional[GoogleMemorystoreInstanceZoneDistributionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleMemorystoreInstanceZoneDistributionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b483f5a55515812c467127977047882fc658d212678b25193619bbdfaf0bef68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleMemorystoreInstance",
    "GoogleMemorystoreInstanceAutomatedBackupConfig",
    "GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule",
    "GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleOutputReference",
    "GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime",
    "GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTimeOutputReference",
    "GoogleMemorystoreInstanceAutomatedBackupConfigOutputReference",
    "GoogleMemorystoreInstanceConfig",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfig",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembership",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipList",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipOutputReference",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceList",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstanceOutputReference",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceList",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstanceOutputReference",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigOutputReference",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstanceOutputReference",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesList",
    "GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstancesOutputReference",
    "GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints",
    "GoogleMemorystoreInstanceDesiredAutoCreatedEndpointsList",
    "GoogleMemorystoreInstanceDesiredAutoCreatedEndpointsOutputReference",
    "GoogleMemorystoreInstanceDesiredPscAutoConnections",
    "GoogleMemorystoreInstanceDesiredPscAutoConnectionsList",
    "GoogleMemorystoreInstanceDesiredPscAutoConnectionsOutputReference",
    "GoogleMemorystoreInstanceDiscoveryEndpoints",
    "GoogleMemorystoreInstanceDiscoveryEndpointsList",
    "GoogleMemorystoreInstanceDiscoveryEndpointsOutputReference",
    "GoogleMemorystoreInstanceEndpoints",
    "GoogleMemorystoreInstanceEndpointsConnections",
    "GoogleMemorystoreInstanceEndpointsConnectionsList",
    "GoogleMemorystoreInstanceEndpointsConnectionsOutputReference",
    "GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnection",
    "GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnectionList",
    "GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnectionOutputReference",
    "GoogleMemorystoreInstanceEndpointsList",
    "GoogleMemorystoreInstanceEndpointsOutputReference",
    "GoogleMemorystoreInstanceGcsSource",
    "GoogleMemorystoreInstanceGcsSourceOutputReference",
    "GoogleMemorystoreInstanceMaintenancePolicy",
    "GoogleMemorystoreInstanceMaintenancePolicyOutputReference",
    "GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow",
    "GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowList",
    "GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
    "GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    "GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
    "GoogleMemorystoreInstanceMaintenanceSchedule",
    "GoogleMemorystoreInstanceMaintenanceScheduleList",
    "GoogleMemorystoreInstanceMaintenanceScheduleOutputReference",
    "GoogleMemorystoreInstanceManagedBackupSource",
    "GoogleMemorystoreInstanceManagedBackupSourceOutputReference",
    "GoogleMemorystoreInstanceNodeConfig",
    "GoogleMemorystoreInstanceNodeConfigList",
    "GoogleMemorystoreInstanceNodeConfigOutputReference",
    "GoogleMemorystoreInstancePersistenceConfig",
    "GoogleMemorystoreInstancePersistenceConfigAofConfig",
    "GoogleMemorystoreInstancePersistenceConfigAofConfigOutputReference",
    "GoogleMemorystoreInstancePersistenceConfigOutputReference",
    "GoogleMemorystoreInstancePersistenceConfigRdbConfig",
    "GoogleMemorystoreInstancePersistenceConfigRdbConfigOutputReference",
    "GoogleMemorystoreInstancePscAttachmentDetails",
    "GoogleMemorystoreInstancePscAttachmentDetailsList",
    "GoogleMemorystoreInstancePscAttachmentDetailsOutputReference",
    "GoogleMemorystoreInstancePscAutoConnections",
    "GoogleMemorystoreInstancePscAutoConnectionsList",
    "GoogleMemorystoreInstancePscAutoConnectionsOutputReference",
    "GoogleMemorystoreInstanceStateInfo",
    "GoogleMemorystoreInstanceStateInfoList",
    "GoogleMemorystoreInstanceStateInfoOutputReference",
    "GoogleMemorystoreInstanceStateInfoUpdateInfo",
    "GoogleMemorystoreInstanceStateInfoUpdateInfoList",
    "GoogleMemorystoreInstanceStateInfoUpdateInfoOutputReference",
    "GoogleMemorystoreInstanceTimeouts",
    "GoogleMemorystoreInstanceTimeoutsOutputReference",
    "GoogleMemorystoreInstanceZoneDistributionConfig",
    "GoogleMemorystoreInstanceZoneDistributionConfigOutputReference",
]

publication.publish()

def _typecheckingstub__4688ebec174e4e2bce73fba43bf23f773ce551120e85cff9bb081f5e88b3686d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_id: builtins.str,
    location: builtins.str,
    shard_count: jsii.Number,
    authorization_mode: typing.Optional[builtins.str] = None,
    automated_backup_config: typing.Optional[typing.Union[GoogleMemorystoreInstanceAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_instance_replication_config: typing.Optional[typing.Union[GoogleMemorystoreInstanceCrossInstanceReplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    desired_auto_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    desired_psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMemorystoreInstanceDesiredPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]]] = None,
    engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    gcs_source: typing.Optional[typing.Union[GoogleMemorystoreInstanceGcsSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_policy: typing.Optional[typing.Union[GoogleMemorystoreInstanceMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_backup_source: typing.Optional[typing.Union[GoogleMemorystoreInstanceManagedBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[GoogleMemorystoreInstancePersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleMemorystoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
    zone_distribution_config: typing.Optional[typing.Union[GoogleMemorystoreInstanceZoneDistributionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__512ee504f9ad42f1170b0ba76292931a000eff65bed59e483ec08e2e36f22cfa(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0cbfd392c8bbd5be54df993775116068ead47e596b745ae4985f9a229bdfe69(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ce83b6def3374756126fb6bd1d1c6465f013bc5f47e51045cdb79b352c6f77(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMemorystoreInstanceDesiredPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47b564ea1c0f118cf2ebaae23af2b487e7a47b8d595cdb4096234a7a8de1846(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf7e4aaa414209995f02d0d4c9f020f47c4647b91329c7bde1c2bd201753722(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abeedc3b9748c4b2971697b40d01185a280dab1af9fc87b0a95d63afa71d8972(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec0000681c267c9e70bce386446d277cc0b4db572c446febd959e1659f5a3ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f1c1f57dc53d04c264791334ce9c454eab3079b786ea423c41bbc1da0b3bf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57710777d9973b7754255209086aa55ce28e4ad9e5513ad2fbe85f784f8d10f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee498b6eee9e4e736018e09333b58c57cbe9bf0b6631f584878e09760256dc4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3597fc1668d948bcef9b555605e30ea17aa62b15a856a477019ea6fa1292ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05cd83134a1760952db3b8f3a198fb28d72240933fff1422b32bc14530dd5d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1506d2f336f29c701c2aeb8c55fdf1b4a1564d483d82237af36e3b6a463831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621bbcb46a21790b7907d40ad1877f0a603ffeeee8309b0db2d451a2825f1520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4030c1772fac511e051565c596dbb87a7a8e70a54677f4b80be6df0c8a6263fb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6066a54e144e6c2caf1816e83b9ba9c819644b2e0f41e328927505b2d0ac82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56bec9155a3dc4b5d99e180ecf766b1d60c6d5ee8cddcd8fcb0515c1b1b09b5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed12923319fe96538174196c41ad3c7a9443cae14be84791f648bd5433ea2a67(
    *,
    fixed_frequency_schedule: typing.Union[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule, typing.Dict[builtins.str, typing.Any]],
    retention: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d8afd809bf272d698ab8254254ce7856f819c992551bf96b46951b50706dff(
    *,
    start_time: typing.Union[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70daed0ac8f542aedcc2b9864379a1bdbb520b774fa2477b4baac157e49bf0d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec4cc2478ac335ab8fbb563d5ee0439fb88b81cb5929119f2b3296d6e5fffe6(
    value: typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a6f5ae110e43282753443a324a69a1a4e233a04e68910cc2fec7a3633a2307(
    *,
    hours: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1df081763c42804f096eadc89ccaaa3d91b3eeedc7a98e6690db6485f406a38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf20c01bbe4fa8fa47a36b704f3e9d3246d5a368550c7cb4d6788e48c9ea9ca0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c55c82c92d8b6f806fda422cd4526be1f1b05b36b43e0783a9e4b7ed8fb093a(
    value: typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfigFixedFrequencyScheduleStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f74e5e019ec6bf27de607e237b6a32ef5487a5780caca1a48cecf2c270d12e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41aa3be59fa7c81fdd4a8a259dfe8912b8a412c197df056836665854b0dd1f17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a4ed458d98e762d36f3158d615b919b5602d2fb111e7a27254f42a6c8b2211(
    value: typing.Optional[GoogleMemorystoreInstanceAutomatedBackupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce2acffab769689ca75cf807d1172d26a3eba0f7c678343bc130011ca87a83c(
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
    automated_backup_config: typing.Optional[typing.Union[GoogleMemorystoreInstanceAutomatedBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_instance_replication_config: typing.Optional[typing.Union[GoogleMemorystoreInstanceCrossInstanceReplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    desired_auto_created_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    desired_psc_auto_connections: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMemorystoreInstanceDesiredPscAutoConnections, typing.Dict[builtins.str, typing.Any]]]]] = None,
    engine_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    gcs_source: typing.Optional[typing.Union[GoogleMemorystoreInstanceGcsSource, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_policy: typing.Optional[typing.Union[GoogleMemorystoreInstanceMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_backup_source: typing.Optional[typing.Union[GoogleMemorystoreInstanceManagedBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    node_type: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[GoogleMemorystoreInstancePersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleMemorystoreInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
    zone_distribution_config: typing.Optional[typing.Union[GoogleMemorystoreInstanceZoneDistributionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c34ba5741eebbc05a98dc02a7d562e652232468bde9d58858bdccb6d2dac07a(
    *,
    instance_role: typing.Optional[builtins.str] = None,
    primary_instance: typing.Optional[typing.Union[GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    secondary_instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97811c011cffd462bd1af5002ec34e8fb664519ba4f088593e21df4bee42d543(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3be0758356f24831fe77dc0b661cea15d7a531f7a3be38c76d34f3031d62ee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87714a5ba47b74b395ac15490cd916482469c9c2f1d615654ca1a69809d45b58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe7a7aa90c8d137c91b70f220fcd5b8705906c742182ec4f67e656c09985c38(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac313c5c7e0ff105fd60d827943e57a6c1f019fb5b8a085d79f3b10fede7aad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8831171f594bcfb458f13ae8a8ebca2cf6598b7f1089aa8e5a17963805e35a40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3cc57a13de012237ee0a1c6ef5427636efaebd30a6da1e5b04db584e403bdb(
    value: typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembership],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e752065fb0e7e7e9472ca4e2605cbe71ef39a451d4485637fb9956cbe51baa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da61dcc2178288705fe84eedc779f99f56f83bfb8a6243dfc3dc373e2d7099b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5204fb7f5bed75b7e14e0159caa0a4b8633e36dfb7c6316833378f1ce41cc783(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71cc9f94e78d6827eb1b3bfd2adf9df8a100d3afdff23f2ab96a4469846971d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7730968d8f258daec2dca8dbb8524fa0f14e6f50b836c6c260dde1b384bc86(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b33f0ac687677c3430bcf6e12e63b6ed4b234573c169c83747e6da3e270bf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837d5df143f327fa35f102dcf5c86cbcd779aa1f18957083a361bb51f0519f0a(
    value: typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipPrimaryInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f7aa1c6a2c9df7ed52260559c65e02c754317b74e3884ecb1726f8fcdd6e57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6539f4255d605cedbc7153acf9c4eb57bd124d74cc5625b1c0acfddc7efc49b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02ffc152535c27e119e736191193d02be157e9acd8839ac5f84ab6a5ea4158b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b834cbcaeb011084d66782ec9e87caa713ecb5fafa56d0ded36ff96f944f079c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df857977a4d7ed3a7dce1bad4e82a532b0c1869db007a49a7c863e49c8670e2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644f0b0922370f5c1c005eddb735606d5a5e296d6e3d0bdb5981e84e86cc1613(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2387f244cf1f7e010be237cf208675026b1d68e7f9e67eb8acc8c27ab7572d5f(
    value: typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigMembershipSecondaryInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da70f0c318aa6e5d4d96ba31cb14d62512db7ac7e426de7a928995e2ac394d56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4f466351aeeef812f8f0ab75b17dda39668027e22536025944b39300d256b0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d5c9afc2f3f068610ead4d6066e10f642450db7606b241b49490051554f653(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ab9e7556992c40e62de9729f94408bf7c7aa40fb057163236cb5d698f20085(
    value: typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ab7a2439132e81dfbf69f1606ce9a698721006d5ec6e162199f37965eb3f66(
    *,
    instance: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dae2238e362b55f860df9db62bfedce7f0bc2d5f8a441dddbc11b3dc5edc474(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d92a65e71e7174efc65247339138ae32e10c37ece4c8a2f686b86ccf9599ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebc98f1771ae7cc3407f4da8d088acaa8ae4d0b27dd368630d1e0ddbb1c2f42(
    value: typing.Optional[GoogleMemorystoreInstanceCrossInstanceReplicationConfigPrimaryInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2f67eb82db0e253302dc1150bb98e230a58fcbae52b19f4239609840c08eb2(
    *,
    instance: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94133763169d846902ce189efdaa802b78167aabdc299ae223aaeadcc4676076(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53147cd08e77d29d1df3b46a72479f01243a9283c11e51f3aeb87dbbd969df6f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5119cf0314b481f12fc522a5a2b905fff633ec29e81c92321f8fd8a3cb3f451d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f0ed16f91a3ea9abf4ce28fab079b755eb77d6cc2eea614e01c55ab3bab819(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061d17da07b6fa73615c1a38e65cc85a810fa81dae52b41006c1818251ef42ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ba7ee447941aad4f0110968f376768c2164772a9956d73fb7aff8536abd810(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd449bdec4fac12564c66a314723f095f79c9a540e799ed8b7b826fb95401d56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b95162305a06f0d67250816dd88329991c7e29062c65e535d485c3d51225f6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65da1a605fac5fa0f443e6850b07f1a3cf090147117d0ca8fb2028bcb2e39c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceCrossInstanceReplicationConfigSecondaryInstances]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfee3bc4f92f7060edde946e019672b2d3e603fc544c36d0d01b9bbc1e7e6dd(
    *,
    network: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b727fd0714ac14fc68c06af2e672c319024a702584fe53bd5d5b5289ed34397(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1db69cd3a88b7fb212c1b5723d0e2c4225b3556cbc071822f01fb82b6a4886(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291bc8b83cbaed6873a6327608cd7638099b7189312f97f80e37151125d0b955(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6fa9f9c7b746a241a04dcf1cb821849492d8e35562e6a4c7391bbfbd3367d6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399c98fba7ccd70041b2a5ffb8f4200d3e3ce1d66ebed887009ed178aaf7c86a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1393e3bc33daf5b20660b2ca52c5f97597b31ca9952e638cebf18c7c52a6c3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9d733ae60ebec296fa485ed61fcbf7d62b94b4f9aa14fd54b398066cef61e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6dd5968fbf6d6dceabc5a693efdc97a2010ddfbf26c26d887b755a9ed310b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65998c768ea5a014f89a577bd7e520ea754fc740c7929ae50d5b0c0aa31a6cf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889ea2da1f15f254dc1c9e0c018dbb1fb4cb25ea1b18b23530bb202520166c9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceDesiredAutoCreatedEndpoints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96fe009dcaaae2395d2f3eb79a43c50d9d919dd3a746012335dea9402642e1ab(
    *,
    network: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2258319408fa649e917c100772b06133c6a3d082c876c37b890af104f24a157c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35367ebde1fd66cd0d539285e70e6437630c49dc6d797aad012b817724c78ced(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5607ff1a928929f0e10c8325567acc6d6ee7bb929a13d793c1ae87bf3ad6c1b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79797e730667040b333edf37c63afa7cf1684e7d7ed7833659e07de4be34ca8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2c71468d7a2c8d50511e5ac89c31a9601578f46730ddfd9be3eb571987bbbc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83de38f13022974d825d900f2f4a75c8133904051d53c82847a569f81a5cc852(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceDesiredPscAutoConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e10cd1e27d4c9bf748e7ef04db47e53e2222f928edfe27cc01924ff9cb9dc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc57a6a3fe691ffac8533e814656542204af0c3da9b6fb69106f63d18d3509e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1daac4ea91668480d18c09d236abf64b70458244a0be2305195c361d5d4f5de0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0472c179fe7e3c05779e7e66735fd87717c2a737dc5be603fb66a61eb3c02a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceDesiredPscAutoConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff16deec2d9fbcb5547fc2334f1218a3cb7cf5f2862bbf2a8b22ffd2bcb194e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca121f92865130c2f4c0ab6eb313a4c6320a42ac8e952ddee4439dd8b46268a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c0d99ed4782e30302017b932ef4f26b127b5dedab16aa47b7111e937939a97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53fc8a84352e92cff06943ba8c8e7a1314b7fe65a02dff4bd49a0186a4e7250(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19f1eda252454f7f433142d856d85a7be6575b7d43a236f48bc2aa3edb45fcf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a256f190a628b98a87d2cad17aa7ed9e025436b37a6b972d5d9bdc7c7fdf550c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ac040c0ce609cf4c4f746d49a4c4e57eef861cdbd5d97363996b9678b18715(
    value: typing.Optional[GoogleMemorystoreInstanceDiscoveryEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9568a29dd38d4b950e7c7810f132fec337c63fca7cc733f7f8d545c3714a2001(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0740b7875d6e2984c2be1144af204cb9b3b2342181e95a2ba884826de163c365(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea1e65d057a3cbd765a23c11db1ac2cfe49985305f69fe423f446c459789b17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb9544f5e54f8cdc5573ce68a4f2a2dba6379c1f17c0508616b47cbc536a275(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b75ce8eda45651aef755668367e7a97c433e5c9338606437b4e5609a0ddb04(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863883210cdcc83adaf039999b85dd8f6c1a95a18c4ad588f507284def193390(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2921b2651c16a3c15230a7a8a27a1acccdf034ae4048253374f33c3b5d10bd(
    value: typing.Optional[GoogleMemorystoreInstanceEndpointsConnections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29466c3fb2bdb74ca4343c124479a3f354688a0cdbdc56915b3a82cc163d95c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833342c6befa4c88460b2e2189a45f5628f12a5bc26e7d9c3f4ceaeca88c78bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f470b4d9444acac6033c7bb23d151a86d3933c78e093452ce1010c7d940e0321(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d049d698e126b558f64009582e73f5e3113725266fd08f9665a2504600ebbca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3026279fdb80abde1266dfd61b05b6d52419f70d8fd576e0b2c7dfc37786ff3d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a8ba00c31865ad4f50c8bcdf21ee67d751b77b15f35ecb621114e20614537c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0541a1c79a3eac3f439639c9c0dee60e50b1fd962ec0e7c6e6d0cd8b2b1e41fc(
    value: typing.Optional[GoogleMemorystoreInstanceEndpointsConnectionsPscAutoConnection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41017858c1457ad14da9bfb8b6b07bf21ea0d8707b93b1c1717a7f6dce827f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375a82195dd0aeb0c3645129e1d64d8d5cffc8e243ae3a014d7cffd2a9ad589e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c70d4e101f3b29543cda0c7049eb9b07ebd9148cf319701e49dd5d961351662(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbe06db4641248caa617ea90afcbadcc5d2ed23021a87cb82aff56970d816fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c8c645901a31fe640e65594299928cd736f82afac1ee9429bc577e7d1c8e82(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88289e12829f73cc6a62a8dc5394f385726cac82e3fcb825d405c04404bc94dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499291a072579853474b6742bab09f92a8886313078386d0a9c9e12987685eff(
    value: typing.Optional[GoogleMemorystoreInstanceEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811d4aa1e64d09152f4085c17b79a5f721a668b06167aa1ec93dc44fed81c894(
    *,
    uris: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0eba63426da041f89cd25974f203006ca642ec6007bb60381c5b3c92f68b4d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2463eabad05d285a1e7c4ee31224ef239d7ad6c245492011ec391f755a4d1a6d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5190d27d06d6ee7ddc9e0441da053cf3dbf0a5de0a4d07e302edd9842cb491(
    value: typing.Optional[GoogleMemorystoreInstanceGcsSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65055eb2b52d57c6d3eda89f29f90eab18a63188103065273953f433b789705(
    *,
    weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2408721f4d76afcd9eb873531df1ccc724901c107add69ce49f4fa7f9d6b3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859a629e68e32c634468c441247344402a2b75443029c15c94f9cba31cb702cf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1be72a667e991e16e0c55c5c81009b8ee31981a2ae07753099fe9da3b5b3e6d(
    value: typing.Optional[GoogleMemorystoreInstanceMaintenancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba2703bcf84e71b0c9ebdd254a6717b81aaf9b4d6ee1b43aa6b7d186a4e0472(
    *,
    day: builtins.str,
    start_time: typing.Union[GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06459100b69f521ae959cd90993f2dcf05f2df1427772922104dac6ccd2871bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9805bf52e5c543137418de1423044123a18e1516c87b653d9daff0b56b12480(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284cab7386e8c5fd827951e2f573fb73baa6da54fbd5c63632e2af65f425ca72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0032999627d26c4ce5ad8334e5d6a4026d2f60d80f4c53a3c84a25345eb9ef0d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf47653d8646e856a813d07385c7e97101026f1ef1b45c71def49ba9f93b2a0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1479c9e420d091c66ccfd24d3456f2ef1b9f9f305e4183291192ed6a3138b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47eb7cc11afeefc2a0e6a98e0d90601e08e8602d05103f9f262c6170b3c6e38e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37084fcbb2769561552a0df1ba8a6500a79975ca4d58c9a21aace5faff002a6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4baf9e49073031ef425097e3a07c7dec59b623bfcd1e21cdcd4915c804b84645(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindow]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d840b20250651eeacb9e3df99fe043bb395669a2103362c1b103003a6b9ffb2(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef836ca9994a1575de8bf5c92deb635bba1c12e819df387cfffa29e59ac205f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1557b98d773de75c0f63c64f25c4401cf16f187b3722850bd6b81caaea9a04d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c6473c39e49e2886cb52e5b02f0e21f211e580b64c24a175c3d8c6ea88b9f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76a32dee6fbd75c5b5b167134b144e31899c495ccfe6c04c2e9891bea3234bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f7f9cf2f429038455501a2c34daf9e0ec644c9c878aa42653fcd63b6c8a699(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ec3e61dea9714c3fb59f14bd492ce083de1aca3c41b374f3c4cd9b63bd9a2e(
    value: typing.Optional[GoogleMemorystoreInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2493de11762e91f124bf763b787110ea3183287a3f69c08796332ee949639c95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f67ba81ea2a06cb7dd7308d20aa619cd2cb4b985c765577deb9585a703dcfb6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f730f1faa216387bcc1f3ea1916d8e37781903dc1fed22665f7093a7a0a6e540(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016ae70fd29e43bb3632140ed9639cc2454d4ef8f08899d83be311bd976e99ec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e87efb9cdffb3c2fe70def00987812871aa2dba877bcd00452051924a3548a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6502e607858422476bf59b70cc19725b224cf9e4e80ed71c18f8daf46c762f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2fa043247346a3e17b0196815a3436a0eb75279efd709601ee0f98edad4a9e(
    value: typing.Optional[GoogleMemorystoreInstanceMaintenanceSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc04766ee94e39bef5029a4af630fd93add78641c7f9491f2a5ff086ef6a950(
    *,
    backup: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1185fe5aa0ebff2329b8ba1ac61e37e0d6f07d451b6fa9f7fdcf28a93598bf62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe00ccd5cea9b90dac1d5cfbf33ad0c4ef5121acd73a8d6f57dd477333f5b327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbf34cddd9b52b814b009c505ecda29162daefdc135ca383d55f3bdd662c678(
    value: typing.Optional[GoogleMemorystoreInstanceManagedBackupSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff042f6405223091ddcc3e4e18108f1284059312c2a97da2c5814d5cc333904a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac452a2f9f66993a83ee31ff14dedeb8b66ba5aec51cecdc7aadb03407aaad4b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383da695e3c86790e8fddfaf9ce687aede2d11fd88bff57ca850e106b096527f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efeef52a570450114d6f3e84f2c6cea9b7dc5e48b6e5aa2937bc7e5f1b4e8df(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421485cb59fc888bb732ddcf609eedce2295ed556b1b294108b8888ecee7c209(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89c5d018c7d3a99e79778f2a93347c035b6b7d977192755fe5b99079660d844(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90aa3495699f5307671e4697df4a7661a852bffbb58b6bb345b9a5546309b7b(
    value: typing.Optional[GoogleMemorystoreInstanceNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14edb3c061778a59bf5ee457423a6e96abfa8c80a6e9ccf96e864d35416825bf(
    *,
    aof_config: typing.Optional[typing.Union[GoogleMemorystoreInstancePersistenceConfigAofConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    rdb_config: typing.Optional[typing.Union[GoogleMemorystoreInstancePersistenceConfigRdbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__677fa95b1dbedcab77135eb7cc86faf12adf4d0ab9efc84dd20a0cace0881a99(
    *,
    append_fsync: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ef669426cb2aa661c651b027e201c471c2c2ea6c57f7737c0d9e5b130930a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15a1601ad5f7ae990fdcc3b0429632ea4ccf2dc2397c07e1d8e8490770abec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45aa49ee3d9d5b628199376e70bf6ad53f0cadc5dd2f6e00f97dd331628c70b(
    value: typing.Optional[GoogleMemorystoreInstancePersistenceConfigAofConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58947915106a304d88883a8989a5282ca7534e4710a28d363ee54d21255d7de3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178f67a7427a3dec45c99deeb6cb61fad3371acfbd22ecfd90782a4c5e066539(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0b640885cd612d55a4883669ce4a128a3a1206682b2a4d8620870da6b4bfa4(
    value: typing.Optional[GoogleMemorystoreInstancePersistenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2c7d61a5a0f397875e49dea11e2b0fa3ebe09e2e7e6ef792ee58559aed6a48(
    *,
    rdb_snapshot_period: typing.Optional[builtins.str] = None,
    rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed578c00951e7aa332ff482981b8294d12313bb1ae618f4ebf82b6310610ef25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39fef34c4fd70d45caee0e6675f34ebed5215da45f560acb07461f1349d3d5ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e81a005381ab5047efd471a5a530dfb32acbef1991004b9dfacd47f09dd160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad2674bed6bcfd0f91be76dc0cbe24d4d4b707c0af774bb7f9189f9db3cb6b8(
    value: typing.Optional[GoogleMemorystoreInstancePersistenceConfigRdbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99238f2a90ca24307d3a19f1a0bec06aa8208477bd4ab01f10c97f3635f6fe69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d975a524082a70b51f97bd6d7cc982281771a213e03350ed0e9ac2268cd834d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccdea6a6c457a695d50ddbb72ddb8f7cdd4dc501219ce8c8d74988079835eb47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab0aca6b3270183b88cf5bfbf867ae935d639c43072c7d2c5b49669a4c067c3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a11ea56115bf78181a0e8489c8a96a655a980f294db367469464a59f0780cc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24902ce32d0d7dba2f8d18e46a36f7f7d9de7751dae4c0ce279706c1a1b8c91c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b2960c5cd04f34ec5eb34f750f512b9ce5e7656c7e234b17836f939a644666(
    value: typing.Optional[GoogleMemorystoreInstancePscAttachmentDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2820bb35714e1fde4f07ba7cb6a267aa4fdc651b91be415301b7953127c7e3f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a468077a31186a1a463409bf145247f7a1814f84b4a0eb3c20a272aac7343a4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762d8ba519a4bb1b7014a12c4e33dd4c5b0f1209ca5fb8c802d5db64ffd349db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e72b7137d0a35341259e22ae10f97b17e5a8d58c07c6ba63dbc5e9e615cb23(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351a482b277b99852fd5ec1156466d3ac7e50dd280278f59da84b5ddd7d29287(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956f1d1de32b6c632fa3be04f97823047b79a3a20331ebb12972bd7f7dc69d68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0097b8605cf24d9144f8ff4a9c2603f03b0a819ea4abeaf7aeddba40afacde3c(
    value: typing.Optional[GoogleMemorystoreInstancePscAutoConnections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f6b9da1e92c9f1d3013452a9fa6d919e64aca99f3ca258677e0864898af542(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12cb6738612c743f8e891d5df005180ae7c5541529c2df5ccbb23fd64fa9cb95(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27d824cac024c98f5f9b1e454cde3a6d131b34f458b7002e2fae90b9a649b48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a617a3752c8e30444f7d37302fc3d9fa7ee1a03d269668f2202aa92f6a30e6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad7ca64fa9a8f7075d8a10279284e56b457d19fafc41595b604b9d7438b77a3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061a3a3801f9b9e72f2105f80cf3545b23ce2c201fd2b618d053b1c9ddadf02e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f87b253e7c0a6e94c579c960d33742762662d9e7634966d55c841c841ffc12(
    value: typing.Optional[GoogleMemorystoreInstanceStateInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dfc1bdea7d126c4220d1bd5b680b3ff16515558cc4ef274ab0bf6b31716c3d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9259fd56c17299447bc088575af9bd3cb9ae5ed8d5dac089eb9034742edcdf2d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424d0da265e85d8bc9fb547f0b03475a6bb87f025ec03adfd909d0846f996d69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49dec1a7800a8d8eee940a70c136a2bc4ac0025e92bcd56b7b7ab692566e78b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678afc6a2e0df2b197e4123a7cba235edec45273bf2a5462f88db2083485794c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ebf0436c4c3659a4edecfdb3aeeaefbdb67a364cfe35d2cd3de491c3c70b39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327529be33725d0d96c6fa32ffa61aacd495d29d2d6c30a4172f3ac82172b72c(
    value: typing.Optional[GoogleMemorystoreInstanceStateInfoUpdateInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51a5032c45297d624c220c5dabb700471db120dc31bdf17a81397eec41568f7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c85ded7591889831f5ae344b49e57d2f30dcd520c8a1f4d6d61e8747a375f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a0e27366184c3e83ff575c0a52c7c2617531e5acc3d902d5ab6f23deabfede(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4bd5527e75166a4399ff66d241e781daebd4f9769797467da5632d3f77249b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63df70880c47fea48040663b27ce990fb3c8a5991a96472c1282bdb8347f8a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1e53a46cfbe72f3ca1924cc173f7ffbb37f3dc789174dbcfb91ed2c257b2ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleMemorystoreInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e90a7942959d61cd460de33c753a32d77772ce82776a75d1543bbb3d1de774e(
    *,
    mode: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a244f6543a835da1a169bf613b9e5a0eb3df2b3e4e65728caa7df5d0e5542aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83293e3acf7680062c58a5c97f32de595fed8c46008c073189e4da59ead26a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4999deb34286ee38a2c4cb516393e40d925a5fd98b43e9a837cb5a5ad19d3211(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b483f5a55515812c467127977047882fc658d212678b25193619bbdfaf0bef68(
    value: typing.Optional[GoogleMemorystoreInstanceZoneDistributionConfig],
) -> None:
    """Type checking stubs"""
    pass
