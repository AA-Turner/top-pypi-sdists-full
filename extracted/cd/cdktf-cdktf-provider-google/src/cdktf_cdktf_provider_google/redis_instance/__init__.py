r'''
# `google_redis_instance`

Refer to the Terraform Registry for docs: [`google_redis_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance).
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


class RedisInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance google_redis_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        memory_size_gb: jsii.Number,
        name: builtins.str,
        alternative_location_id: typing.Optional[builtins.str] = None,
        auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        authorized_network: typing.Optional[builtins.str] = None,
        connect_mode: typing.Optional[builtins.str] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location_id: typing.Optional[builtins.str] = None,
        maintenance_policy: typing.Optional[typing.Union["RedisInstanceMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_version: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["RedisInstancePersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        read_replicas_mode: typing.Optional[builtins.str] = None,
        redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        redis_version: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        reserved_ip_range: typing.Optional[builtins.str] = None,
        secondary_ip_range: typing.Optional[builtins.str] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["RedisInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance google_redis_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param memory_size_gb: Redis memory size in GiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#memory_size_gb RedisInstance#memory_size_gb}
        :param name: The ID of the instance or a fully qualified identifier for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#name RedisInstance#name}
        :param alternative_location_id: Only applicable to STANDARD_HA tier which protects the instance against zonal failures by provisioning it across two zones. If provided, it must be a different zone from the one provided in [locationId]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#alternative_location_id RedisInstance#alternative_location_id}
        :param auth_enabled: Optional. Indicates whether OSS Redis AUTH is enabled for the instance. If set to "true" AUTH is enabled on the instance. Default value is "false" meaning AUTH is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#auth_enabled RedisInstance#auth_enabled}
        :param authorized_network: The full name of the Google Compute Engine network to which the instance is connected. If left unspecified, the default network will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#authorized_network RedisInstance#authorized_network}
        :param connect_mode: The connection mode of the Redis instance. Default value: "DIRECT_PEERING" Possible values: ["DIRECT_PEERING", "PRIVATE_SERVICE_ACCESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#connect_mode RedisInstance#connect_mode}
        :param customer_managed_key: Optional. The KMS key reference that you want to use to encrypt the data at rest for this Redis instance. If this is provided, CMEK is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#customer_managed_key RedisInstance#customer_managed_key}
        :param display_name: An arbitrary and optional user-provided name for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#display_name RedisInstance#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#id RedisInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#labels RedisInstance#labels}
        :param location_id: The zone where the instance will be provisioned. If not provided, the service will choose a zone for the instance. For STANDARD_HA tier, instances will be created across two zones for protection against zonal failures. If [alternativeLocationId] is also provided, it must be different from [locationId]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#location_id RedisInstance#location_id}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#maintenance_policy RedisInstance#maintenance_policy}
        :param maintenance_version: The self service update maintenance version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#maintenance_version RedisInstance#maintenance_version}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#persistence_config RedisInstance#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#project RedisInstance#project}.
        :param read_replicas_mode: Optional. Read replica mode. Can only be specified when trying to create the instance. If not set, Memorystore Redis backend will default to READ_REPLICAS_DISABLED. - READ_REPLICAS_DISABLED: If disabled, read endpoint will not be provided and the instance cannot scale up or down the number of replicas. - READ_REPLICAS_ENABLED: If enabled, read endpoint will be provided and the instance can scale up and down the number of replicas. Possible values: ["READ_REPLICAS_DISABLED", "READ_REPLICAS_ENABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#read_replicas_mode RedisInstance#read_replicas_mode}
        :param redis_configs: Redis configuration parameters, according to http://redis.io/topics/config. Please check Memorystore documentation for the list of supported parameters: https://cloud.google.com/memorystore/docs/redis/reference/rest/v1/projects.locations.instances#Instance.FIELDS.redis_configs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#redis_configs RedisInstance#redis_configs}
        :param redis_version: The version of Redis software. If not provided, latest supported version will be used. Please check the API documentation linked at the top for the latest valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#redis_version RedisInstance#redis_version}
        :param region: The name of the Redis region of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#region RedisInstance#region}
        :param replica_count: Optional. The number of replica nodes. The valid range for the Standard Tier with read replicas enabled is [1-5] and defaults to 2. If read replicas are not enabled for a Standard Tier instance, the only valid value is 1 and the default is 1. The valid value for basic tier is 0 and the default is also 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#replica_count RedisInstance#replica_count}
        :param reserved_ip_range: The CIDR range of internal addresses that are reserved for this instance. If not provided, the service will choose an unused /29 block, for example, 10.0.0.0/29 or 192.168.0.0/29. Ranges must be unique and non-overlapping with existing subnets in an authorized network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#reserved_ip_range RedisInstance#reserved_ip_range}
        :param secondary_ip_range: Optional. Additional IP range for node placement. Required when enabling read replicas on an existing instance. For DIRECT_PEERING mode value must be a CIDR range of size /28, or "auto". For PRIVATE_SERVICE_ACCESS mode value must be the name of an allocated address range associated with the private service access connection, or "auto". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#secondary_ip_range RedisInstance#secondary_ip_range}
        :param tier: The service tier of the instance. Must be one of these values:. - BASIC: standalone instance - STANDARD_HA: highly available primary/replica instances Default value: "BASIC" Possible values: ["BASIC", "STANDARD_HA"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#tier RedisInstance#tier}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#timeouts RedisInstance#timeouts}
        :param transit_encryption_mode: The TLS mode of the Redis instance, If not provided, TLS is disabled for the instance. - SERVER_AUTHENTICATION: Client to Server traffic encryption enabled with server authentication Default value: "DISABLED" Possible values: ["SERVER_AUTHENTICATION", "DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#transit_encryption_mode RedisInstance#transit_encryption_mode}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__790a3ba378b670f4b5143988d7c4a895ae18767aec4dac9258e386585989c4f5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RedisInstanceConfig(
            memory_size_gb=memory_size_gb,
            name=name,
            alternative_location_id=alternative_location_id,
            auth_enabled=auth_enabled,
            authorized_network=authorized_network,
            connect_mode=connect_mode,
            customer_managed_key=customer_managed_key,
            display_name=display_name,
            id=id,
            labels=labels,
            location_id=location_id,
            maintenance_policy=maintenance_policy,
            maintenance_version=maintenance_version,
            persistence_config=persistence_config,
            project=project,
            read_replicas_mode=read_replicas_mode,
            redis_configs=redis_configs,
            redis_version=redis_version,
            region=region,
            replica_count=replica_count,
            reserved_ip_range=reserved_ip_range,
            secondary_ip_range=secondary_ip_range,
            tier=tier,
            timeouts=timeouts,
            transit_encryption_mode=transit_encryption_mode,
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
        '''Generates CDKTF code for importing a RedisInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RedisInstance to import.
        :param import_from_id: The id of the existing RedisInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RedisInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80744e16c2ea1ab265bed52208eb15e3fdd5ec6210c18cb7e5dc4312fdfc041a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMaintenancePolicy")
    def put_maintenance_policy(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param description: Optional. Description of what this policy is for. Create/Update methods return INVALID_ARGUMENT if the length is greater than 512. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#description RedisInstance#description}
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#weekly_maintenance_window RedisInstance#weekly_maintenance_window}
        '''
        value = RedisInstanceMaintenancePolicy(
            description=description,
            weekly_maintenance_window=weekly_maintenance_window,
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenancePolicy", [value]))

    @jsii.member(jsii_name="putPersistenceConfig")
    def put_persistence_config(
        self,
        *,
        persistence_mode: typing.Optional[builtins.str] = None,
        rdb_snapshot_period: typing.Optional[builtins.str] = None,
        rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param persistence_mode: Optional. Controls whether Persistence features are enabled. If not provided, the existing value will be used. - DISABLED: Persistence is disabled for the instance, and any existing snapshots are deleted. - RDB: RDB based Persistence is enabled. Possible values: ["DISABLED", "RDB"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#persistence_mode RedisInstance#persistence_mode}
        :param rdb_snapshot_period: Optional. Available snapshot periods for scheduling. - ONE_HOUR: Snapshot every 1 hour. - SIX_HOURS: Snapshot every 6 hours. - TWELVE_HOURS: Snapshot every 12 hours. - TWENTY_FOUR_HOURS: Snapshot every 24 hours. Possible values: ["ONE_HOUR", "SIX_HOURS", "TWELVE_HOURS", "TWENTY_FOUR_HOURS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#rdb_snapshot_period RedisInstance#rdb_snapshot_period}
        :param rdb_snapshot_start_time: Optional. Date and time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#rdb_snapshot_start_time RedisInstance#rdb_snapshot_start_time}
        '''
        value = RedisInstancePersistenceConfig(
            persistence_mode=persistence_mode,
            rdb_snapshot_period=rdb_snapshot_period,
            rdb_snapshot_start_time=rdb_snapshot_start_time,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#create RedisInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#delete RedisInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#update RedisInstance#update}.
        '''
        value = RedisInstanceTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAlternativeLocationId")
    def reset_alternative_location_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlternativeLocationId", []))

    @jsii.member(jsii_name="resetAuthEnabled")
    def reset_auth_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthEnabled", []))

    @jsii.member(jsii_name="resetAuthorizedNetwork")
    def reset_authorized_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizedNetwork", []))

    @jsii.member(jsii_name="resetConnectMode")
    def reset_connect_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectMode", []))

    @jsii.member(jsii_name="resetCustomerManagedKey")
    def reset_customer_managed_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedKey", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocationId")
    def reset_location_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationId", []))

    @jsii.member(jsii_name="resetMaintenancePolicy")
    def reset_maintenance_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenancePolicy", []))

    @jsii.member(jsii_name="resetMaintenanceVersion")
    def reset_maintenance_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceVersion", []))

    @jsii.member(jsii_name="resetPersistenceConfig")
    def reset_persistence_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersistenceConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReadReplicasMode")
    def reset_read_replicas_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadReplicasMode", []))

    @jsii.member(jsii_name="resetRedisConfigs")
    def reset_redis_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisConfigs", []))

    @jsii.member(jsii_name="resetRedisVersion")
    def reset_redis_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisVersion", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReplicaCount")
    def reset_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaCount", []))

    @jsii.member(jsii_name="resetReservedIpRange")
    def reset_reserved_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedIpRange", []))

    @jsii.member(jsii_name="resetSecondaryIpRange")
    def reset_secondary_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryIpRange", []))

    @jsii.member(jsii_name="resetTier")
    def reset_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTier", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTransitEncryptionMode")
    def reset_transit_encryption_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransitEncryptionMode", []))

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
    @jsii.member(jsii_name="authString")
    def auth_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authString"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="currentLocationId")
    def current_location_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "currentLocationId"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="effectiveReservedIpRange")
    def effective_reserved_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveReservedIpRange"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicy")
    def maintenance_policy(self) -> "RedisInstanceMaintenancePolicyOutputReference":
        return typing.cast("RedisInstanceMaintenancePolicyOutputReference", jsii.get(self, "maintenancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceSchedule")
    def maintenance_schedule(self) -> "RedisInstanceMaintenanceScheduleList":
        return typing.cast("RedisInstanceMaintenanceScheduleList", jsii.get(self, "maintenanceSchedule"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> "RedisInstanceNodesList":
        return typing.cast("RedisInstanceNodesList", jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="persistenceConfig")
    def persistence_config(self) -> "RedisInstancePersistenceConfigOutputReference":
        return typing.cast("RedisInstancePersistenceConfigOutputReference", jsii.get(self, "persistenceConfig"))

    @builtins.property
    @jsii.member(jsii_name="persistenceIamIdentity")
    def persistence_iam_identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "persistenceIamIdentity"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="readEndpoint")
    def read_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="readEndpointPort")
    def read_endpoint_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "readEndpointPort"))

    @builtins.property
    @jsii.member(jsii_name="serverCaCerts")
    def server_ca_certs(self) -> "RedisInstanceServerCaCertsList":
        return typing.cast("RedisInstanceServerCaCertsList", jsii.get(self, "serverCaCerts"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RedisInstanceTimeoutsOutputReference":
        return typing.cast("RedisInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="alternativeLocationIdInput")
    def alternative_location_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alternativeLocationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="authEnabledInput")
    def auth_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "authEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedNetworkInput")
    def authorized_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizedNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="connectModeInput")
    def connect_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectModeInput"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKeyInput")
    def customer_managed_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerManagedKeyInput"))

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
    @jsii.member(jsii_name="locationIdInput")
    def location_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicyInput")
    def maintenance_policy_input(
        self,
    ) -> typing.Optional["RedisInstanceMaintenancePolicy"]:
        return typing.cast(typing.Optional["RedisInstanceMaintenancePolicy"], jsii.get(self, "maintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceVersionInput")
    def maintenance_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeGbInput")
    def memory_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="persistenceConfigInput")
    def persistence_config_input(
        self,
    ) -> typing.Optional["RedisInstancePersistenceConfig"]:
        return typing.cast(typing.Optional["RedisInstancePersistenceConfig"], jsii.get(self, "persistenceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="readReplicasModeInput")
    def read_replicas_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readReplicasModeInput"))

    @builtins.property
    @jsii.member(jsii_name="redisConfigsInput")
    def redis_configs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "redisConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="redisVersionInput")
    def redis_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redisVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaCountInput")
    def replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedIpRangeInput")
    def reserved_ip_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservedIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryIpRangeInput")
    def secondary_ip_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RedisInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RedisInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionModeInput")
    def transit_encryption_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transitEncryptionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="alternativeLocationId")
    def alternative_location_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alternativeLocationId"))

    @alternative_location_id.setter
    def alternative_location_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c4a2fc546c2318d82872f52d69db7bc03dd4d180069e71b500bb6323284e5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alternativeLocationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authEnabled")
    def auth_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "authEnabled"))

    @auth_enabled.setter
    def auth_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78593bdce37284268735ac126ab742ab23bccd57e6b75c1c6ece5bdb1bb07761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizedNetwork")
    def authorized_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizedNetwork"))

    @authorized_network.setter
    def authorized_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d1888bda8db053c4c7a0ae2cc49ba165d17cb5630b5bc4ece165795d09fd28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectMode")
    def connect_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectMode"))

    @connect_mode.setter
    def connect_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__196a1ea213013b1c2061597d6c9a14ea6ded312584277ef178aeb3af56ef3c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customerManagedKey")
    def customer_managed_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerManagedKey"))

    @customer_managed_key.setter
    def customer_managed_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2016fd66ae5bb2a561b518c7b72b6156813edabd02683bedadb2133b0d196d0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerManagedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0beca8081c2967819518aa600718ce367b36dcfe9a20d4429ee671b496328e2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8bf8189b6edb2e2634ca86e2a3f3882f258bb8ec29fb6ef4622fda305539c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b971da92a20493932c35ce578125bde7f37a9844cc170ba051cf572c1cd0dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locationId")
    def location_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locationId"))

    @location_id.setter
    def location_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01336da298b9791089d79fbf14e9983e64044f0bf0aa88d55de27fd9b4e629a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceVersion")
    def maintenance_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceVersion"))

    @maintenance_version.setter
    def maintenance_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb5bbe5daa6610894606e8eac0316139e51246af14888729ff751016b5fec23a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySizeGb")
    def memory_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeGb"))

    @memory_size_gb.setter
    def memory_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b5f64ad603d236c295d7ee0d955f0b391182511ad868d5d3ec3ef0d837a1e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78843c387fe6ec2f92a4a0a239d7918509392dbb9aa55614839d5a3b58d235c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68900387b051971953999fe12e74f9c9ad878c744e0f5ab4e10f2f6439b7eb5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readReplicasMode")
    def read_replicas_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readReplicasMode"))

    @read_replicas_mode.setter
    def read_replicas_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7795cd0f08e392297914ffd9d3bb818d2a49a7dfe7f3f86f849403ba97090695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readReplicasMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redisConfigs")
    def redis_configs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "redisConfigs"))

    @redis_configs.setter
    def redis_configs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051286ca428c2b3b15ae3a7b0c49adf5aa175e0ea544b7823f3d28aca8c5efef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisConfigs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redisVersion")
    def redis_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redisVersion"))

    @redis_version.setter
    def redis_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6738ed447c78e06d3cd07630292e295eda31c4bd93a014e229ec5d5d0cc5f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ea6430575809345611276915bcd65e5453ffc905d029ca75b8fa607891a5e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaCount")
    def replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCount"))

    @replica_count.setter
    def replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645d2bd774c6c4a8e0e1945b957d21ea9435bf967bfee905fdd300b37341e71f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedIpRange")
    def reserved_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedIpRange"))

    @reserved_ip_range.setter
    def reserved_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138eee7fe1bdf516ecf366dcb4a95ef3d1c7d9ac8282864e03894132197dae2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryIpRange")
    def secondary_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryIpRange"))

    @secondary_ip_range.setter
    def secondary_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeefaafd687ab7bc34cb5b105d8bf31193033d431faf8b53a19efac421de040e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b0c0d57d6400980224c118c8862aefbc0259f19efae85d74cc20cb79e8db8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionMode")
    def transit_encryption_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitEncryptionMode"))

    @transit_encryption_mode.setter
    def transit_encryption_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9077e812e6e6c03f8762cc805bfeea174abc77514d032a1c5c9b9fcb949eeeb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitEncryptionMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "memory_size_gb": "memorySizeGb",
        "name": "name",
        "alternative_location_id": "alternativeLocationId",
        "auth_enabled": "authEnabled",
        "authorized_network": "authorizedNetwork",
        "connect_mode": "connectMode",
        "customer_managed_key": "customerManagedKey",
        "display_name": "displayName",
        "id": "id",
        "labels": "labels",
        "location_id": "locationId",
        "maintenance_policy": "maintenancePolicy",
        "maintenance_version": "maintenanceVersion",
        "persistence_config": "persistenceConfig",
        "project": "project",
        "read_replicas_mode": "readReplicasMode",
        "redis_configs": "redisConfigs",
        "redis_version": "redisVersion",
        "region": "region",
        "replica_count": "replicaCount",
        "reserved_ip_range": "reservedIpRange",
        "secondary_ip_range": "secondaryIpRange",
        "tier": "tier",
        "timeouts": "timeouts",
        "transit_encryption_mode": "transitEncryptionMode",
    },
)
class RedisInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        memory_size_gb: jsii.Number,
        name: builtins.str,
        alternative_location_id: typing.Optional[builtins.str] = None,
        auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        authorized_network: typing.Optional[builtins.str] = None,
        connect_mode: typing.Optional[builtins.str] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location_id: typing.Optional[builtins.str] = None,
        maintenance_policy: typing.Optional[typing.Union["RedisInstanceMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_version: typing.Optional[builtins.str] = None,
        persistence_config: typing.Optional[typing.Union["RedisInstancePersistenceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        read_replicas_mode: typing.Optional[builtins.str] = None,
        redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        redis_version: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        replica_count: typing.Optional[jsii.Number] = None,
        reserved_ip_range: typing.Optional[builtins.str] = None,
        secondary_ip_range: typing.Optional[builtins.str] = None,
        tier: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["RedisInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transit_encryption_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param memory_size_gb: Redis memory size in GiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#memory_size_gb RedisInstance#memory_size_gb}
        :param name: The ID of the instance or a fully qualified identifier for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#name RedisInstance#name}
        :param alternative_location_id: Only applicable to STANDARD_HA tier which protects the instance against zonal failures by provisioning it across two zones. If provided, it must be a different zone from the one provided in [locationId]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#alternative_location_id RedisInstance#alternative_location_id}
        :param auth_enabled: Optional. Indicates whether OSS Redis AUTH is enabled for the instance. If set to "true" AUTH is enabled on the instance. Default value is "false" meaning AUTH is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#auth_enabled RedisInstance#auth_enabled}
        :param authorized_network: The full name of the Google Compute Engine network to which the instance is connected. If left unspecified, the default network will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#authorized_network RedisInstance#authorized_network}
        :param connect_mode: The connection mode of the Redis instance. Default value: "DIRECT_PEERING" Possible values: ["DIRECT_PEERING", "PRIVATE_SERVICE_ACCESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#connect_mode RedisInstance#connect_mode}
        :param customer_managed_key: Optional. The KMS key reference that you want to use to encrypt the data at rest for this Redis instance. If this is provided, CMEK is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#customer_managed_key RedisInstance#customer_managed_key}
        :param display_name: An arbitrary and optional user-provided name for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#display_name RedisInstance#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#id RedisInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#labels RedisInstance#labels}
        :param location_id: The zone where the instance will be provisioned. If not provided, the service will choose a zone for the instance. For STANDARD_HA tier, instances will be created across two zones for protection against zonal failures. If [alternativeLocationId] is also provided, it must be different from [locationId]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#location_id RedisInstance#location_id}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#maintenance_policy RedisInstance#maintenance_policy}
        :param maintenance_version: The self service update maintenance version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#maintenance_version RedisInstance#maintenance_version}
        :param persistence_config: persistence_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#persistence_config RedisInstance#persistence_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#project RedisInstance#project}.
        :param read_replicas_mode: Optional. Read replica mode. Can only be specified when trying to create the instance. If not set, Memorystore Redis backend will default to READ_REPLICAS_DISABLED. - READ_REPLICAS_DISABLED: If disabled, read endpoint will not be provided and the instance cannot scale up or down the number of replicas. - READ_REPLICAS_ENABLED: If enabled, read endpoint will be provided and the instance can scale up and down the number of replicas. Possible values: ["READ_REPLICAS_DISABLED", "READ_REPLICAS_ENABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#read_replicas_mode RedisInstance#read_replicas_mode}
        :param redis_configs: Redis configuration parameters, according to http://redis.io/topics/config. Please check Memorystore documentation for the list of supported parameters: https://cloud.google.com/memorystore/docs/redis/reference/rest/v1/projects.locations.instances#Instance.FIELDS.redis_configs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#redis_configs RedisInstance#redis_configs}
        :param redis_version: The version of Redis software. If not provided, latest supported version will be used. Please check the API documentation linked at the top for the latest valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#redis_version RedisInstance#redis_version}
        :param region: The name of the Redis region of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#region RedisInstance#region}
        :param replica_count: Optional. The number of replica nodes. The valid range for the Standard Tier with read replicas enabled is [1-5] and defaults to 2. If read replicas are not enabled for a Standard Tier instance, the only valid value is 1 and the default is 1. The valid value for basic tier is 0 and the default is also 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#replica_count RedisInstance#replica_count}
        :param reserved_ip_range: The CIDR range of internal addresses that are reserved for this instance. If not provided, the service will choose an unused /29 block, for example, 10.0.0.0/29 or 192.168.0.0/29. Ranges must be unique and non-overlapping with existing subnets in an authorized network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#reserved_ip_range RedisInstance#reserved_ip_range}
        :param secondary_ip_range: Optional. Additional IP range for node placement. Required when enabling read replicas on an existing instance. For DIRECT_PEERING mode value must be a CIDR range of size /28, or "auto". For PRIVATE_SERVICE_ACCESS mode value must be the name of an allocated address range associated with the private service access connection, or "auto". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#secondary_ip_range RedisInstance#secondary_ip_range}
        :param tier: The service tier of the instance. Must be one of these values:. - BASIC: standalone instance - STANDARD_HA: highly available primary/replica instances Default value: "BASIC" Possible values: ["BASIC", "STANDARD_HA"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#tier RedisInstance#tier}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#timeouts RedisInstance#timeouts}
        :param transit_encryption_mode: The TLS mode of the Redis instance, If not provided, TLS is disabled for the instance. - SERVER_AUTHENTICATION: Client to Server traffic encryption enabled with server authentication Default value: "DISABLED" Possible values: ["SERVER_AUTHENTICATION", "DISABLED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#transit_encryption_mode RedisInstance#transit_encryption_mode}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(maintenance_policy, dict):
            maintenance_policy = RedisInstanceMaintenancePolicy(**maintenance_policy)
        if isinstance(persistence_config, dict):
            persistence_config = RedisInstancePersistenceConfig(**persistence_config)
        if isinstance(timeouts, dict):
            timeouts = RedisInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af74190e5e9f1cf069f67044ad12e63822955148a7fb12c58a281dedd7ebd4b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument memory_size_gb", value=memory_size_gb, expected_type=type_hints["memory_size_gb"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument alternative_location_id", value=alternative_location_id, expected_type=type_hints["alternative_location_id"])
            check_type(argname="argument auth_enabled", value=auth_enabled, expected_type=type_hints["auth_enabled"])
            check_type(argname="argument authorized_network", value=authorized_network, expected_type=type_hints["authorized_network"])
            check_type(argname="argument connect_mode", value=connect_mode, expected_type=type_hints["connect_mode"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location_id", value=location_id, expected_type=type_hints["location_id"])
            check_type(argname="argument maintenance_policy", value=maintenance_policy, expected_type=type_hints["maintenance_policy"])
            check_type(argname="argument maintenance_version", value=maintenance_version, expected_type=type_hints["maintenance_version"])
            check_type(argname="argument persistence_config", value=persistence_config, expected_type=type_hints["persistence_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument read_replicas_mode", value=read_replicas_mode, expected_type=type_hints["read_replicas_mode"])
            check_type(argname="argument redis_configs", value=redis_configs, expected_type=type_hints["redis_configs"])
            check_type(argname="argument redis_version", value=redis_version, expected_type=type_hints["redis_version"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument replica_count", value=replica_count, expected_type=type_hints["replica_count"])
            check_type(argname="argument reserved_ip_range", value=reserved_ip_range, expected_type=type_hints["reserved_ip_range"])
            check_type(argname="argument secondary_ip_range", value=secondary_ip_range, expected_type=type_hints["secondary_ip_range"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument transit_encryption_mode", value=transit_encryption_mode, expected_type=type_hints["transit_encryption_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "memory_size_gb": memory_size_gb,
            "name": name,
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
        if alternative_location_id is not None:
            self._values["alternative_location_id"] = alternative_location_id
        if auth_enabled is not None:
            self._values["auth_enabled"] = auth_enabled
        if authorized_network is not None:
            self._values["authorized_network"] = authorized_network
        if connect_mode is not None:
            self._values["connect_mode"] = connect_mode
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location_id is not None:
            self._values["location_id"] = location_id
        if maintenance_policy is not None:
            self._values["maintenance_policy"] = maintenance_policy
        if maintenance_version is not None:
            self._values["maintenance_version"] = maintenance_version
        if persistence_config is not None:
            self._values["persistence_config"] = persistence_config
        if project is not None:
            self._values["project"] = project
        if read_replicas_mode is not None:
            self._values["read_replicas_mode"] = read_replicas_mode
        if redis_configs is not None:
            self._values["redis_configs"] = redis_configs
        if redis_version is not None:
            self._values["redis_version"] = redis_version
        if region is not None:
            self._values["region"] = region
        if replica_count is not None:
            self._values["replica_count"] = replica_count
        if reserved_ip_range is not None:
            self._values["reserved_ip_range"] = reserved_ip_range
        if secondary_ip_range is not None:
            self._values["secondary_ip_range"] = secondary_ip_range
        if tier is not None:
            self._values["tier"] = tier
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if transit_encryption_mode is not None:
            self._values["transit_encryption_mode"] = transit_encryption_mode

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
    def memory_size_gb(self) -> jsii.Number:
        '''Redis memory size in GiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#memory_size_gb RedisInstance#memory_size_gb}
        '''
        result = self._values.get("memory_size_gb")
        assert result is not None, "Required property 'memory_size_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The ID of the instance or a fully qualified identifier for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#name RedisInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alternative_location_id(self) -> typing.Optional[builtins.str]:
        '''Only applicable to STANDARD_HA tier which protects the instance against zonal failures by provisioning it across two zones.

        If provided, it must be a different zone from the one provided in
        [locationId].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#alternative_location_id RedisInstance#alternative_location_id}
        '''
        result = self._values.get("alternative_location_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Indicates whether OSS Redis AUTH is enabled for the
        instance. If set to "true" AUTH is enabled on the instance.
        Default value is "false" meaning AUTH is disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#auth_enabled RedisInstance#auth_enabled}
        '''
        result = self._values.get("auth_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def authorized_network(self) -> typing.Optional[builtins.str]:
        '''The full name of the Google Compute Engine network to which the instance is connected.

        If left unspecified, the default network
        will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#authorized_network RedisInstance#authorized_network}
        '''
        result = self._values.get("authorized_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect_mode(self) -> typing.Optional[builtins.str]:
        '''The connection mode of the Redis instance. Default value: "DIRECT_PEERING" Possible values: ["DIRECT_PEERING", "PRIVATE_SERVICE_ACCESS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#connect_mode RedisInstance#connect_mode}
        '''
        result = self._values.get("connect_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_managed_key(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The KMS key reference that you want to use to encrypt the data at rest for this Redis
        instance. If this is provided, CMEK is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#customer_managed_key RedisInstance#customer_managed_key}
        '''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''An arbitrary and optional user-provided name for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#display_name RedisInstance#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#id RedisInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource labels to represent user provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#labels RedisInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location_id(self) -> typing.Optional[builtins.str]:
        '''The zone where the instance will be provisioned.

        If not provided,
        the service will choose a zone for the instance. For STANDARD_HA tier,
        instances will be created across two zones for protection against
        zonal failures. If [alternativeLocationId] is also provided, it must
        be different from [locationId].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#location_id RedisInstance#location_id}
        '''
        result = self._values.get("location_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_policy(self) -> typing.Optional["RedisInstanceMaintenancePolicy"]:
        '''maintenance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#maintenance_policy RedisInstance#maintenance_policy}
        '''
        result = self._values.get("maintenance_policy")
        return typing.cast(typing.Optional["RedisInstanceMaintenancePolicy"], result)

    @builtins.property
    def maintenance_version(self) -> typing.Optional[builtins.str]:
        '''The self service update maintenance version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#maintenance_version RedisInstance#maintenance_version}
        '''
        result = self._values.get("maintenance_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def persistence_config(self) -> typing.Optional["RedisInstancePersistenceConfig"]:
        '''persistence_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#persistence_config RedisInstance#persistence_config}
        '''
        result = self._values.get("persistence_config")
        return typing.cast(typing.Optional["RedisInstancePersistenceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#project RedisInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_replicas_mode(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Read replica mode. Can only be specified when trying to create the instance.
        If not set, Memorystore Redis backend will default to READ_REPLICAS_DISABLED.

        - READ_REPLICAS_DISABLED: If disabled, read endpoint will not be provided and the
          instance cannot scale up or down the number of replicas.
        - READ_REPLICAS_ENABLED: If enabled, read endpoint will be provided and the instance
          can scale up and down the number of replicas. Possible values: ["READ_REPLICAS_DISABLED", "READ_REPLICAS_ENABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#read_replicas_mode RedisInstance#read_replicas_mode}
        '''
        result = self._values.get("read_replicas_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redis_configs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Redis configuration parameters, according to http://redis.io/topics/config. Please check Memorystore documentation for the list of supported parameters: https://cloud.google.com/memorystore/docs/redis/reference/rest/v1/projects.locations.instances#Instance.FIELDS.redis_configs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#redis_configs RedisInstance#redis_configs}
        '''
        result = self._values.get("redis_configs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def redis_version(self) -> typing.Optional[builtins.str]:
        '''The version of Redis software.

        If not provided, latest supported
        version will be used. Please check the API documentation linked
        at the top for the latest valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#redis_version RedisInstance#redis_version}
        '''
        result = self._values.get("redis_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The name of the Redis region of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#region RedisInstance#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_count(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The number of replica nodes. The valid range for the Standard Tier with
        read replicas enabled is [1-5] and defaults to 2. If read replicas are not enabled
        for a Standard Tier instance, the only valid value is 1 and the default is 1.
        The valid value for basic tier is 0 and the default is also 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#replica_count RedisInstance#replica_count}
        '''
        result = self._values.get("replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def reserved_ip_range(self) -> typing.Optional[builtins.str]:
        '''The CIDR range of internal addresses that are reserved for this instance.

        If not provided, the service will choose an unused /29
        block, for example, 10.0.0.0/29 or 192.168.0.0/29. Ranges must be
        unique and non-overlapping with existing subnets in an authorized
        network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#reserved_ip_range RedisInstance#reserved_ip_range}
        '''
        result = self._values.get("reserved_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_ip_range(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Additional IP range for node placement. Required when enabling read replicas on
        an existing instance. For DIRECT_PEERING mode value must be a CIDR range of size /28, or
        "auto". For PRIVATE_SERVICE_ACCESS mode value must be the name of an allocated address
        range associated with the private service access connection, or "auto".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#secondary_ip_range RedisInstance#secondary_ip_range}
        '''
        result = self._values.get("secondary_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''The service tier of the instance. Must be one of these values:.

        - BASIC: standalone instance
        - STANDARD_HA: highly available primary/replica instances Default value: "BASIC" Possible values: ["BASIC", "STANDARD_HA"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#tier RedisInstance#tier}
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RedisInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#timeouts RedisInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RedisInstanceTimeouts"], result)

    @builtins.property
    def transit_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''The TLS mode of the Redis instance, If not provided, TLS is disabled for the instance.

        - SERVER_AUTHENTICATION: Client to Server traffic encryption enabled with server authentication Default value: "DISABLED" Possible values: ["SERVER_AUTHENTICATION", "DISABLED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#transit_encryption_mode RedisInstance#transit_encryption_mode}
        '''
        result = self._values.get("transit_encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceMaintenancePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "weekly_maintenance_window": "weeklyMaintenanceWindow",
    },
)
class RedisInstanceMaintenancePolicy:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param description: Optional. Description of what this policy is for. Create/Update methods return INVALID_ARGUMENT if the length is greater than 512. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#description RedisInstance#description}
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#weekly_maintenance_window RedisInstance#weekly_maintenance_window}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3585547f07550b54b4c6dbfddb1bd85ab1eb3972e22babe6ee696fa28d4ab2)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument weekly_maintenance_window", value=weekly_maintenance_window, expected_type=type_hints["weekly_maintenance_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if weekly_maintenance_window is not None:
            self._values["weekly_maintenance_window"] = weekly_maintenance_window

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of what this policy is for. Create/Update methods return INVALID_ARGUMENT if the length is greater than 512.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#description RedisInstance#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekly_maintenance_window(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]]:
        '''weekly_maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#weekly_maintenance_window RedisInstance#weekly_maintenance_window}
        '''
        result = self._values.get("weekly_maintenance_window")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisInstanceMaintenancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisInstanceMaintenancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceMaintenancePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7bc59772ce6dd81d0be4dfcb578ce293ce1b6bb71c3383032249707a0ea7dda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWeeklyMaintenanceWindow")
    def put_weekly_maintenance_window(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd7c7b71eab316f15b37b5cf965bf82c57904e81452cad3d0216112091e3975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWeeklyMaintenanceWindow", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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
    ) -> "RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowList":
        return typing.cast("RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowList", jsii.get(self, "weeklyMaintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyMaintenanceWindowInput")
    def weekly_maintenance_window_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]], jsii.get(self, "weeklyMaintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8749046f9e55f04fdc2354a50e110a646f91db8b52695dae6dc6de561f2d093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisInstanceMaintenancePolicy]:
        return typing.cast(typing.Optional[RedisInstanceMaintenancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisInstanceMaintenancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89acb166fe02b62ef43c3cd548162c01a7c06c4034cbeb190d03819f0389a2f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "start_time": "startTime"},
)
class RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow:
    def __init__(
        self,
        *,
        day: builtins.str,
        start_time: typing.Union["RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day: Required. The day of week that maintenance updates occur. - DAY_OF_WEEK_UNSPECIFIED: The day of the week is unspecified. - MONDAY: Monday - TUESDAY: Tuesday - WEDNESDAY: Wednesday - THURSDAY: Thursday - FRIDAY: Friday - SATURDAY: Saturday - SUNDAY: Sunday Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#day RedisInstance#day}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#start_time RedisInstance#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec76c4f9282837e7d88ccdea58c951814402f20b6ab74424fbc3aee5b7b5b0d9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#day RedisInstance#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(
        self,
    ) -> "RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#start_time RedisInstance#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2fe7f9abcb5ecbcc5d09f835eb7c12f254c1bfcd7dca387ff091556f07c982a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9a156a7a23c6863962a632f4dd221fcda69a7aa0422b63f5708517415ef3ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def1c5ae4b2d5852814a7f8abe4cf188e66cf759210e59d84a9dfba19d4b84d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5797f8bc6b0b67ee480ac8b7dbb2179ee36fa7b30aac3de009e84924c8aa34ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a220f840a1a13914318ef4c3f923856d601ff03cb7a7a70a64e9cd1f0f407ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5b73bbf8d4d8206db7427dc7e15c918c339a93ec0dd5911346c373352d65ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcb7334f5e553c5b7757677397c724c55923a0c8b50992356301a337915a9af6)
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
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#hours RedisInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#minutes RedisInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#nanos RedisInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#seconds RedisInstance#seconds}
        '''
        value = RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(
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
    ) -> "RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference":
        return typing.cast("RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime"]:
        return typing.cast(typing.Optional["RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115a854e2bbd8ded834f8e8d77ecc8ba1860bd092698ea42debc3e2cef926a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627f07d0616ef5db206b08df2b6b375984fe7ebc359003f2d89c29bd4c500e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#hours RedisInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#minutes RedisInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#nanos RedisInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#seconds RedisInstance#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a7157f69357616c0b19ba51f81c029b6c0efb98a2cf31405fd95548d97c089)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#hours RedisInstance#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#minutes RedisInstance#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#nanos RedisInstance#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time.

        Must normally be from 0 to 59.
        An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#seconds RedisInstance#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09bd1f0afc1051a0f93bf80d46199e3c2dc6a55c03c60de09b1b2e583eb75003)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9bc90a78c7281ee1c0dbbc3cd415aa45e229554cae400afd0fd5179f93c730e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d92ef3ff5e2e32f435f38e9faebee729501590d17d027861fa49d5bc3e96d65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e0dab48304bbb51d5a1b896d55bae7856fc2f6752c8273c206de9169c8cbcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397838e7165a7cba98970aa45170dec4cd96fa134b4e11329532c7aa660ab8e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime]:
        return typing.cast(typing.Optional[RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d8d314b34ddb4e3a797eb36b02767439eb2008672768d955c2334450ed5697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceMaintenanceSchedule",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisInstanceMaintenanceSchedule:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisInstanceMaintenanceSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisInstanceMaintenanceScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceMaintenanceScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d87095250f221384a990940a7d2df09636c5ead26a116d8411fcd49e9bf6535)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RedisInstanceMaintenanceScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b89fe12ac4d104043edf9851ce58b417d447f079e5fdd0c61ce9d877fa8699)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisInstanceMaintenanceScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c71c54c9643ba9863770ea3fcd44cb163c9c5b3721cf91d308048046d5a7fa1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e1c0cc47209d57d6a8c88bba1c0be46a37b6f9282ee253f51192cbb9023b708)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e586594daf1ffc47810e75ed400cfc2d3dc4a2307e31eaf58366d70ada4118d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisInstanceMaintenanceScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceMaintenanceScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d01a4853fb6be35b239b782031181b80c79990686f1fabcebbf773c0a0b23c4e)
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
    def internal_value(self) -> typing.Optional[RedisInstanceMaintenanceSchedule]:
        return typing.cast(typing.Optional[RedisInstanceMaintenanceSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisInstanceMaintenanceSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4200bb7889e3f6e6fb054b786f221a92646b6a7f33084f31c90aa243855c40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceNodes",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisInstanceNodes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisInstanceNodes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisInstanceNodesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceNodesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__222db0428edcbb9f6a31e34c05e5f22b6fe24c4ebc71d389f7f129481f04f41b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RedisInstanceNodesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2366ff4047930a61db054098e234ab94fb114186bc2c2ce625bd5e5cb814fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisInstanceNodesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ddb3831b2d2ce1ca9f05d2e97ced2c6c2f1edfe9c3b9bebebe34e8a5d541fdd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0b895ef118a6a037015049194e2f24186cd8bfd866e579119480a2dee9ae98d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7a8a86d5deacd972cb09ed3b1c3e1962b0778c0abb4c8e9f97df06883be0f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisInstanceNodesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceNodesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cf6ce780a24830398a2658963877d7514a702c24bd30a84231afa1d7f7ece81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisInstanceNodes]:
        return typing.cast(typing.Optional[RedisInstanceNodes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RedisInstanceNodes]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e469c9b22f80b5c434473739451521f8c97eda689248b5be20d5de31561b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstancePersistenceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "persistence_mode": "persistenceMode",
        "rdb_snapshot_period": "rdbSnapshotPeriod",
        "rdb_snapshot_start_time": "rdbSnapshotStartTime",
    },
)
class RedisInstancePersistenceConfig:
    def __init__(
        self,
        *,
        persistence_mode: typing.Optional[builtins.str] = None,
        rdb_snapshot_period: typing.Optional[builtins.str] = None,
        rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param persistence_mode: Optional. Controls whether Persistence features are enabled. If not provided, the existing value will be used. - DISABLED: Persistence is disabled for the instance, and any existing snapshots are deleted. - RDB: RDB based Persistence is enabled. Possible values: ["DISABLED", "RDB"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#persistence_mode RedisInstance#persistence_mode}
        :param rdb_snapshot_period: Optional. Available snapshot periods for scheduling. - ONE_HOUR: Snapshot every 1 hour. - SIX_HOURS: Snapshot every 6 hours. - TWELVE_HOURS: Snapshot every 12 hours. - TWENTY_FOUR_HOURS: Snapshot every 24 hours. Possible values: ["ONE_HOUR", "SIX_HOURS", "TWELVE_HOURS", "TWENTY_FOUR_HOURS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#rdb_snapshot_period RedisInstance#rdb_snapshot_period}
        :param rdb_snapshot_start_time: Optional. Date and time that the first snapshot was/will be attempted, and to which future snapshots will be aligned. If not provided, the current time will be used. A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#rdb_snapshot_start_time RedisInstance#rdb_snapshot_start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b9d2fb6541e0dee61360b8f9827109eaca858d7302c034d3224447df65a71a)
            check_type(argname="argument persistence_mode", value=persistence_mode, expected_type=type_hints["persistence_mode"])
            check_type(argname="argument rdb_snapshot_period", value=rdb_snapshot_period, expected_type=type_hints["rdb_snapshot_period"])
            check_type(argname="argument rdb_snapshot_start_time", value=rdb_snapshot_start_time, expected_type=type_hints["rdb_snapshot_start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if persistence_mode is not None:
            self._values["persistence_mode"] = persistence_mode
        if rdb_snapshot_period is not None:
            self._values["rdb_snapshot_period"] = rdb_snapshot_period
        if rdb_snapshot_start_time is not None:
            self._values["rdb_snapshot_start_time"] = rdb_snapshot_start_time

    @builtins.property
    def persistence_mode(self) -> typing.Optional[builtins.str]:
        '''Optional. Controls whether Persistence features are enabled. If not provided, the existing value will be used.

        - DISABLED: 	Persistence is disabled for the instance, and any existing snapshots are deleted.
        - RDB: RDB based Persistence is enabled. Possible values: ["DISABLED", "RDB"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#persistence_mode RedisInstance#persistence_mode}
        '''
        result = self._values.get("persistence_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_snapshot_period(self) -> typing.Optional[builtins.str]:
        '''Optional. Available snapshot periods for scheduling.

        - ONE_HOUR:	Snapshot every 1 hour.
        - SIX_HOURS:	Snapshot every 6 hours.
        - TWELVE_HOURS:	Snapshot every 12 hours.
        - TWENTY_FOUR_HOURS:	Snapshot every 24 hours. Possible values: ["ONE_HOUR", "SIX_HOURS", "TWELVE_HOURS", "TWENTY_FOUR_HOURS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#rdb_snapshot_period RedisInstance#rdb_snapshot_period}
        '''
        result = self._values.get("rdb_snapshot_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_snapshot_start_time(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Date and time that the first snapshot was/will be attempted,
        and to which future snapshots will be aligned. If not provided,
        the current time will be used.
        A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution
        and up to nine fractional digits.
        Examples: "2014-10-02T15:01:23Z" and "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#rdb_snapshot_start_time RedisInstance#rdb_snapshot_start_time}
        '''
        result = self._values.get("rdb_snapshot_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisInstancePersistenceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisInstancePersistenceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstancePersistenceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e68b0df4320bb4ed72fc5290b17bcaa7ea1229053fd55fc111aa813fdf524df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPersistenceMode")
    def reset_persistence_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersistenceMode", []))

    @jsii.member(jsii_name="resetRdbSnapshotPeriod")
    def reset_rdb_snapshot_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbSnapshotPeriod", []))

    @jsii.member(jsii_name="resetRdbSnapshotStartTime")
    def reset_rdb_snapshot_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbSnapshotStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="rdbNextSnapshotTime")
    def rdb_next_snapshot_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdbNextSnapshotTime"))

    @builtins.property
    @jsii.member(jsii_name="persistenceModeInput")
    def persistence_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "persistenceModeInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotPeriodInput")
    def rdb_snapshot_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rdbSnapshotPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotStartTimeInput")
    def rdb_snapshot_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rdbSnapshotStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="persistenceMode")
    def persistence_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "persistenceMode"))

    @persistence_mode.setter
    def persistence_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffac0ec2c05608191132ea0e4ac53e4f9c686f71ba5368c6cba29f15c8125f85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "persistenceMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotPeriod")
    def rdb_snapshot_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdbSnapshotPeriod"))

    @rdb_snapshot_period.setter
    def rdb_snapshot_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527e1e35c5cf632832c77ea160e7119276af58e55dd7c955416cd27f0e201a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rdbSnapshotStartTime")
    def rdb_snapshot_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdbSnapshotStartTime"))

    @rdb_snapshot_start_time.setter
    def rdb_snapshot_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aea6119e2a5ac9a224516f63635746558f06d64cebb98bc88db7afe884a2e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbSnapshotStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisInstancePersistenceConfig]:
        return typing.cast(typing.Optional[RedisInstancePersistenceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisInstancePersistenceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e347e7b1f35cc45577cdfc4630948f2093cf06bb6a5398445edb3c35e4659da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceServerCaCerts",
    jsii_struct_bases=[],
    name_mapping={},
)
class RedisInstanceServerCaCerts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisInstanceServerCaCerts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisInstanceServerCaCertsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceServerCaCertsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b053886c62dc4be39c0ef0f12c2b4a88a7d892ed6ad8a8795bed3dc48b838df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RedisInstanceServerCaCertsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7138fcac5031e868daadeb1f08d02c57426d925c006ddc7f8fd00668624eb746)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisInstanceServerCaCertsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e206d7fee84e2cbaba2ab1d1dc2cfa74b2803cc2eefbe8dbcceaa5affced43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96c35abb369926bc68612162c87e46a8a5bb43b4411ccab9d0b3167042618937)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48ebe4c3986ccca851c2bba14607f970106b4382ab140fbac78141ba24b758df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class RedisInstanceServerCaCertsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceServerCaCertsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__953f7ef70a51a0406324642b6e4bb92fa66a71ed1f947184dbdd13db2b9a3e84)
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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @builtins.property
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serialNumber"))

    @builtins.property
    @jsii.member(jsii_name="sha1Fingerprint")
    def sha1_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha1Fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisInstanceServerCaCerts]:
        return typing.cast(typing.Optional[RedisInstanceServerCaCerts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisInstanceServerCaCerts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288f5313c29239ac380e2f7f708801ef775a4c8f74a424459f6b4bc7241ae638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class RedisInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#create RedisInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#delete RedisInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#update RedisInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b40d029e496fe8f35d6ca66ae52c15b744d903597d29ceef677a253213e3387)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#create RedisInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#delete RedisInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/redis_instance#update RedisInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.redisInstance.RedisInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e35959f7db5685a7085640295f525bf6f24873aae41101cafc5079e59721d2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f91449cfc3c0a2eb04673fd7e64425e14a0d48442f8d9919ebb9664376d6bb0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40442c090bd731a02a6a57d1620975a9826e3ecf5d62f801695723d55d5b804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b57504c76474a00ee050d8c1d9a21ecc5c20bc7cf7bc9b0169c145c34d3f5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008fffe5a4063d4402ff7d21dd9e947811a18df3a32601d5808239e4bd4b67f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RedisInstance",
    "RedisInstanceConfig",
    "RedisInstanceMaintenancePolicy",
    "RedisInstanceMaintenancePolicyOutputReference",
    "RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow",
    "RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowList",
    "RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
    "RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    "RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
    "RedisInstanceMaintenanceSchedule",
    "RedisInstanceMaintenanceScheduleList",
    "RedisInstanceMaintenanceScheduleOutputReference",
    "RedisInstanceNodes",
    "RedisInstanceNodesList",
    "RedisInstanceNodesOutputReference",
    "RedisInstancePersistenceConfig",
    "RedisInstancePersistenceConfigOutputReference",
    "RedisInstanceServerCaCerts",
    "RedisInstanceServerCaCertsList",
    "RedisInstanceServerCaCertsOutputReference",
    "RedisInstanceTimeouts",
    "RedisInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__790a3ba378b670f4b5143988d7c4a895ae18767aec4dac9258e386585989c4f5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    memory_size_gb: jsii.Number,
    name: builtins.str,
    alternative_location_id: typing.Optional[builtins.str] = None,
    auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    authorized_network: typing.Optional[builtins.str] = None,
    connect_mode: typing.Optional[builtins.str] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location_id: typing.Optional[builtins.str] = None,
    maintenance_policy: typing.Optional[typing.Union[RedisInstanceMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_version: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[RedisInstancePersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    read_replicas_mode: typing.Optional[builtins.str] = None,
    redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    redis_version: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    reserved_ip_range: typing.Optional[builtins.str] = None,
    secondary_ip_range: typing.Optional[builtins.str] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[RedisInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__80744e16c2ea1ab265bed52208eb15e3fdd5ec6210c18cb7e5dc4312fdfc041a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c4a2fc546c2318d82872f52d69db7bc03dd4d180069e71b500bb6323284e5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78593bdce37284268735ac126ab742ab23bccd57e6b75c1c6ece5bdb1bb07761(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d1888bda8db053c4c7a0ae2cc49ba165d17cb5630b5bc4ece165795d09fd28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196a1ea213013b1c2061597d6c9a14ea6ded312584277ef178aeb3af56ef3c3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2016fd66ae5bb2a561b518c7b72b6156813edabd02683bedadb2133b0d196d0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0beca8081c2967819518aa600718ce367b36dcfe9a20d4429ee671b496328e2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8bf8189b6edb2e2634ca86e2a3f3882f258bb8ec29fb6ef4622fda305539c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b971da92a20493932c35ce578125bde7f37a9844cc170ba051cf572c1cd0dd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01336da298b9791089d79fbf14e9983e64044f0bf0aa88d55de27fd9b4e629a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5bbe5daa6610894606e8eac0316139e51246af14888729ff751016b5fec23a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b5f64ad603d236c295d7ee0d955f0b391182511ad868d5d3ec3ef0d837a1e13(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78843c387fe6ec2f92a4a0a239d7918509392dbb9aa55614839d5a3b58d235c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68900387b051971953999fe12e74f9c9ad878c744e0f5ab4e10f2f6439b7eb5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7795cd0f08e392297914ffd9d3bb818d2a49a7dfe7f3f86f849403ba97090695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051286ca428c2b3b15ae3a7b0c49adf5aa175e0ea544b7823f3d28aca8c5efef(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6738ed447c78e06d3cd07630292e295eda31c4bd93a014e229ec5d5d0cc5f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ea6430575809345611276915bcd65e5453ffc905d029ca75b8fa607891a5e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645d2bd774c6c4a8e0e1945b957d21ea9435bf967bfee905fdd300b37341e71f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138eee7fe1bdf516ecf366dcb4a95ef3d1c7d9ac8282864e03894132197dae2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeefaafd687ab7bc34cb5b105d8bf31193033d431faf8b53a19efac421de040e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b0c0d57d6400980224c118c8862aefbc0259f19efae85d74cc20cb79e8db8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9077e812e6e6c03f8762cc805bfeea174abc77514d032a1c5c9b9fcb949eeeb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af74190e5e9f1cf069f67044ad12e63822955148a7fb12c58a281dedd7ebd4b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    memory_size_gb: jsii.Number,
    name: builtins.str,
    alternative_location_id: typing.Optional[builtins.str] = None,
    auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    authorized_network: typing.Optional[builtins.str] = None,
    connect_mode: typing.Optional[builtins.str] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location_id: typing.Optional[builtins.str] = None,
    maintenance_policy: typing.Optional[typing.Union[RedisInstanceMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_version: typing.Optional[builtins.str] = None,
    persistence_config: typing.Optional[typing.Union[RedisInstancePersistenceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    read_replicas_mode: typing.Optional[builtins.str] = None,
    redis_configs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    redis_version: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    reserved_ip_range: typing.Optional[builtins.str] = None,
    secondary_ip_range: typing.Optional[builtins.str] = None,
    tier: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[RedisInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transit_encryption_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3585547f07550b54b4c6dbfddb1bd85ab1eb3972e22babe6ee696fa28d4ab2(
    *,
    description: typing.Optional[builtins.str] = None,
    weekly_maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bc59772ce6dd81d0be4dfcb578ce293ce1b6bb71c3383032249707a0ea7dda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd7c7b71eab316f15b37b5cf965bf82c57904e81452cad3d0216112091e3975(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8749046f9e55f04fdc2354a50e110a646f91db8b52695dae6dc6de561f2d093(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89acb166fe02b62ef43c3cd548162c01a7c06c4034cbeb190d03819f0389a2f5(
    value: typing.Optional[RedisInstanceMaintenancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec76c4f9282837e7d88ccdea58c951814402f20b6ab74424fbc3aee5b7b5b0d9(
    *,
    day: builtins.str,
    start_time: typing.Union[RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fe7f9abcb5ecbcc5d09f835eb7c12f254c1bfcd7dca387ff091556f07c982a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9a156a7a23c6863962a632f4dd221fcda69a7aa0422b63f5708517415ef3ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def1c5ae4b2d5852814a7f8abe4cf188e66cf759210e59d84a9dfba19d4b84d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5797f8bc6b0b67ee480ac8b7dbb2179ee36fa7b30aac3de009e84924c8aa34ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a220f840a1a13914318ef4c3f923856d601ff03cb7a7a70a64e9cd1f0f407ca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5b73bbf8d4d8206db7427dc7e15c918c339a93ec0dd5911346c373352d65ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb7334f5e553c5b7757677397c724c55923a0c8b50992356301a337915a9af6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115a854e2bbd8ded834f8e8d77ecc8ba1860bd092698ea42debc3e2cef926a37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627f07d0616ef5db206b08df2b6b375984fe7ebc359003f2d89c29bd4c500e63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisInstanceMaintenancePolicyWeeklyMaintenanceWindow]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a7157f69357616c0b19ba51f81c029b6c0efb98a2cf31405fd95548d97c089(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09bd1f0afc1051a0f93bf80d46199e3c2dc6a55c03c60de09b1b2e583eb75003(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bc90a78c7281ee1c0dbbc3cd415aa45e229554cae400afd0fd5179f93c730e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d92ef3ff5e2e32f435f38e9faebee729501590d17d027861fa49d5bc3e96d65(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e0dab48304bbb51d5a1b896d55bae7856fc2f6752c8273c206de9169c8cbcf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397838e7165a7cba98970aa45170dec4cd96fa134b4e11329532c7aa660ab8e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d8d314b34ddb4e3a797eb36b02767439eb2008672768d955c2334450ed5697(
    value: typing.Optional[RedisInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d87095250f221384a990940a7d2df09636c5ead26a116d8411fcd49e9bf6535(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b89fe12ac4d104043edf9851ce58b417d447f079e5fdd0c61ce9d877fa8699(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c71c54c9643ba9863770ea3fcd44cb163c9c5b3721cf91d308048046d5a7fa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1c0cc47209d57d6a8c88bba1c0be46a37b6f9282ee253f51192cbb9023b708(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e586594daf1ffc47810e75ed400cfc2d3dc4a2307e31eaf58366d70ada4118d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01a4853fb6be35b239b782031181b80c79990686f1fabcebbf773c0a0b23c4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4200bb7889e3f6e6fb054b786f221a92646b6a7f33084f31c90aa243855c40(
    value: typing.Optional[RedisInstanceMaintenanceSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222db0428edcbb9f6a31e34c05e5f22b6fe24c4ebc71d389f7f129481f04f41b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2366ff4047930a61db054098e234ab94fb114186bc2c2ce625bd5e5cb814fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ddb3831b2d2ce1ca9f05d2e97ced2c6c2f1edfe9c3b9bebebe34e8a5d541fdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b895ef118a6a037015049194e2f24186cd8bfd866e579119480a2dee9ae98d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a8a86d5deacd972cb09ed3b1c3e1962b0778c0abb4c8e9f97df06883be0f17(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf6ce780a24830398a2658963877d7514a702c24bd30a84231afa1d7f7ece81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e469c9b22f80b5c434473739451521f8c97eda689248b5be20d5de31561b0a(
    value: typing.Optional[RedisInstanceNodes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b9d2fb6541e0dee61360b8f9827109eaca858d7302c034d3224447df65a71a(
    *,
    persistence_mode: typing.Optional[builtins.str] = None,
    rdb_snapshot_period: typing.Optional[builtins.str] = None,
    rdb_snapshot_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e68b0df4320bb4ed72fc5290b17bcaa7ea1229053fd55fc111aa813fdf524df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffac0ec2c05608191132ea0e4ac53e4f9c686f71ba5368c6cba29f15c8125f85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527e1e35c5cf632832c77ea160e7119276af58e55dd7c955416cd27f0e201a7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aea6119e2a5ac9a224516f63635746558f06d64cebb98bc88db7afe884a2e41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e347e7b1f35cc45577cdfc4630948f2093cf06bb6a5398445edb3c35e4659da(
    value: typing.Optional[RedisInstancePersistenceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b053886c62dc4be39c0ef0f12c2b4a88a7d892ed6ad8a8795bed3dc48b838df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7138fcac5031e868daadeb1f08d02c57426d925c006ddc7f8fd00668624eb746(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e206d7fee84e2cbaba2ab1d1dc2cfa74b2803cc2eefbe8dbcceaa5affced43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c35abb369926bc68612162c87e46a8a5bb43b4411ccab9d0b3167042618937(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ebe4c3986ccca851c2bba14607f970106b4382ab140fbac78141ba24b758df(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953f7ef70a51a0406324642b6e4bb92fa66a71ed1f947184dbdd13db2b9a3e84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288f5313c29239ac380e2f7f708801ef775a4c8f74a424459f6b4bc7241ae638(
    value: typing.Optional[RedisInstanceServerCaCerts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b40d029e496fe8f35d6ca66ae52c15b744d903597d29ceef677a253213e3387(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e35959f7db5685a7085640295f525bf6f24873aae41101cafc5079e59721d2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91449cfc3c0a2eb04673fd7e64425e14a0d48442f8d9919ebb9664376d6bb0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40442c090bd731a02a6a57d1620975a9826e3ecf5d62f801695723d55d5b804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b57504c76474a00ee050d8c1d9a21ecc5c20bc7cf7bc9b0169c145c34d3f5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008fffe5a4063d4402ff7d21dd9e947811a18df3a32601d5808239e4bd4b67f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
