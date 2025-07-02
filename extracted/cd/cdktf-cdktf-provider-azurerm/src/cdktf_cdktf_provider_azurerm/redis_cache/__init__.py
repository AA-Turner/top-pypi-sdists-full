r'''
# `azurerm_redis_cache`

Refer to the Terraform Registry for docs: [`azurerm_redis_cache`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache).
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


class RedisCache(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redisCache.RedisCache",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache azurerm_redis_cache}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        capacity: jsii.Number,
        family: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku_name: builtins.str,
        access_keys_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["RedisCacheIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        minimum_tls_version: typing.Optional[builtins.str] = None,
        non_ssl_port_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        patch_schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisCachePatchSchedule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        private_static_ip_address: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        redis_configuration: typing.Optional[typing.Union["RedisCacheRedisConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        redis_version: typing.Optional[builtins.str] = None,
        replicas_per_master: typing.Optional[jsii.Number] = None,
        replicas_per_primary: typing.Optional[jsii.Number] = None,
        shard_count: typing.Optional[jsii.Number] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenant_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RedisCacheTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache azurerm_redis_cache} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#capacity RedisCache#capacity}.
        :param family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#family RedisCache#family}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#location RedisCache#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#name RedisCache#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#resource_group_name RedisCache#resource_group_name}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#sku_name RedisCache#sku_name}.
        :param access_keys_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#access_keys_authentication_enabled RedisCache#access_keys_authentication_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#id RedisCache#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#identity RedisCache#identity}
        :param minimum_tls_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#minimum_tls_version RedisCache#minimum_tls_version}.
        :param non_ssl_port_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#non_ssl_port_enabled RedisCache#non_ssl_port_enabled}.
        :param patch_schedule: patch_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#patch_schedule RedisCache#patch_schedule}
        :param private_static_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#private_static_ip_address RedisCache#private_static_ip_address}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#public_network_access_enabled RedisCache#public_network_access_enabled}.
        :param redis_configuration: redis_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#redis_configuration RedisCache#redis_configuration}
        :param redis_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#redis_version RedisCache#redis_version}.
        :param replicas_per_master: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#replicas_per_master RedisCache#replicas_per_master}.
        :param replicas_per_primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#replicas_per_primary RedisCache#replicas_per_primary}.
        :param shard_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#shard_count RedisCache#shard_count}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#subnet_id RedisCache#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#tags RedisCache#tags}.
        :param tenant_settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#tenant_settings RedisCache#tenant_settings}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#timeouts RedisCache#timeouts}
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#zones RedisCache#zones}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeaaf0a6422abbe43b925106121aa0f645fc74b48706b58fc82ad889d5b9f158)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RedisCacheConfig(
            capacity=capacity,
            family=family,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            sku_name=sku_name,
            access_keys_authentication_enabled=access_keys_authentication_enabled,
            id=id,
            identity=identity,
            minimum_tls_version=minimum_tls_version,
            non_ssl_port_enabled=non_ssl_port_enabled,
            patch_schedule=patch_schedule,
            private_static_ip_address=private_static_ip_address,
            public_network_access_enabled=public_network_access_enabled,
            redis_configuration=redis_configuration,
            redis_version=redis_version,
            replicas_per_master=replicas_per_master,
            replicas_per_primary=replicas_per_primary,
            shard_count=shard_count,
            subnet_id=subnet_id,
            tags=tags,
            tenant_settings=tenant_settings,
            timeouts=timeouts,
            zones=zones,
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
        '''Generates CDKTF code for importing a RedisCache resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RedisCache to import.
        :param import_from_id: The id of the existing RedisCache that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RedisCache to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684ca5039fb00f21659d78a4f73e5f131ba5af6f4029c55792d5f405889ff0b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#type RedisCache#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#identity_ids RedisCache#identity_ids}.
        '''
        value = RedisCacheIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putPatchSchedule")
    def put_patch_schedule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisCachePatchSchedule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__232fb5b1d59835d910902483c34f146479f81cc0e83cddee65f429ae82f3a4db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPatchSchedule", [value]))

    @jsii.member(jsii_name="putRedisConfiguration")
    def put_redis_configuration(
        self,
        *,
        active_directory_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        aof_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        aof_storage_connection_string0: typing.Optional[builtins.str] = None,
        aof_storage_connection_string1: typing.Optional[builtins.str] = None,
        authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_persistence_authentication_method: typing.Optional[builtins.str] = None,
        maxfragmentationmemory_reserved: typing.Optional[jsii.Number] = None,
        maxmemory_delta: typing.Optional[jsii.Number] = None,
        maxmemory_policy: typing.Optional[builtins.str] = None,
        maxmemory_reserved: typing.Optional[jsii.Number] = None,
        notify_keyspace_events: typing.Optional[builtins.str] = None,
        rdb_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rdb_backup_frequency: typing.Optional[jsii.Number] = None,
        rdb_backup_max_snapshot_count: typing.Optional[jsii.Number] = None,
        rdb_storage_connection_string: typing.Optional[builtins.str] = None,
        storage_account_subscription_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param active_directory_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#active_directory_authentication_enabled RedisCache#active_directory_authentication_enabled}.
        :param aof_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#aof_backup_enabled RedisCache#aof_backup_enabled}.
        :param aof_storage_connection_string0: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#aof_storage_connection_string_0 RedisCache#aof_storage_connection_string_0}.
        :param aof_storage_connection_string1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#aof_storage_connection_string_1 RedisCache#aof_storage_connection_string_1}.
        :param authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#authentication_enabled RedisCache#authentication_enabled}.
        :param data_persistence_authentication_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#data_persistence_authentication_method RedisCache#data_persistence_authentication_method}.
        :param maxfragmentationmemory_reserved: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxfragmentationmemory_reserved RedisCache#maxfragmentationmemory_reserved}.
        :param maxmemory_delta: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxmemory_delta RedisCache#maxmemory_delta}.
        :param maxmemory_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxmemory_policy RedisCache#maxmemory_policy}.
        :param maxmemory_reserved: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxmemory_reserved RedisCache#maxmemory_reserved}.
        :param notify_keyspace_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#notify_keyspace_events RedisCache#notify_keyspace_events}.
        :param rdb_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_backup_enabled RedisCache#rdb_backup_enabled}.
        :param rdb_backup_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_backup_frequency RedisCache#rdb_backup_frequency}.
        :param rdb_backup_max_snapshot_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_backup_max_snapshot_count RedisCache#rdb_backup_max_snapshot_count}.
        :param rdb_storage_connection_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_storage_connection_string RedisCache#rdb_storage_connection_string}.
        :param storage_account_subscription_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#storage_account_subscription_id RedisCache#storage_account_subscription_id}.
        '''
        value = RedisCacheRedisConfiguration(
            active_directory_authentication_enabled=active_directory_authentication_enabled,
            aof_backup_enabled=aof_backup_enabled,
            aof_storage_connection_string0=aof_storage_connection_string0,
            aof_storage_connection_string1=aof_storage_connection_string1,
            authentication_enabled=authentication_enabled,
            data_persistence_authentication_method=data_persistence_authentication_method,
            maxfragmentationmemory_reserved=maxfragmentationmemory_reserved,
            maxmemory_delta=maxmemory_delta,
            maxmemory_policy=maxmemory_policy,
            maxmemory_reserved=maxmemory_reserved,
            notify_keyspace_events=notify_keyspace_events,
            rdb_backup_enabled=rdb_backup_enabled,
            rdb_backup_frequency=rdb_backup_frequency,
            rdb_backup_max_snapshot_count=rdb_backup_max_snapshot_count,
            rdb_storage_connection_string=rdb_storage_connection_string,
            storage_account_subscription_id=storage_account_subscription_id,
        )

        return typing.cast(None, jsii.invoke(self, "putRedisConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#create RedisCache#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#delete RedisCache#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#read RedisCache#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#update RedisCache#update}.
        '''
        value = RedisCacheTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessKeysAuthenticationEnabled")
    def reset_access_keys_authentication_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKeysAuthenticationEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetMinimumTlsVersion")
    def reset_minimum_tls_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumTlsVersion", []))

    @jsii.member(jsii_name="resetNonSslPortEnabled")
    def reset_non_ssl_port_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonSslPortEnabled", []))

    @jsii.member(jsii_name="resetPatchSchedule")
    def reset_patch_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPatchSchedule", []))

    @jsii.member(jsii_name="resetPrivateStaticIpAddress")
    def reset_private_static_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateStaticIpAddress", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetRedisConfiguration")
    def reset_redis_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisConfiguration", []))

    @jsii.member(jsii_name="resetRedisVersion")
    def reset_redis_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisVersion", []))

    @jsii.member(jsii_name="resetReplicasPerMaster")
    def reset_replicas_per_master(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicasPerMaster", []))

    @jsii.member(jsii_name="resetReplicasPerPrimary")
    def reset_replicas_per_primary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicasPerPrimary", []))

    @jsii.member(jsii_name="resetShardCount")
    def reset_shard_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShardCount", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTenantSettings")
    def reset_tenant_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantSettings", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

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
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "RedisCacheIdentityOutputReference":
        return typing.cast("RedisCacheIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="patchSchedule")
    def patch_schedule(self) -> "RedisCachePatchScheduleList":
        return typing.cast("RedisCachePatchScheduleList", jsii.get(self, "patchSchedule"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="primaryAccessKey")
    def primary_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryAccessKey"))

    @builtins.property
    @jsii.member(jsii_name="primaryConnectionString")
    def primary_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="redisConfiguration")
    def redis_configuration(self) -> "RedisCacheRedisConfigurationOutputReference":
        return typing.cast("RedisCacheRedisConfigurationOutputReference", jsii.get(self, "redisConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="secondaryAccessKey")
    def secondary_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryAccessKey"))

    @builtins.property
    @jsii.member(jsii_name="secondaryConnectionString")
    def secondary_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="sslPort")
    def ssl_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sslPort"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "RedisCacheTimeoutsOutputReference":
        return typing.cast("RedisCacheTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessKeysAuthenticationEnabledInput")
    def access_keys_authentication_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessKeysAuthenticationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="familyInput")
    def family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "familyInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["RedisCacheIdentity"]:
        return typing.cast(typing.Optional["RedisCacheIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumTlsVersionInput")
    def minimum_tls_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumTlsVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nonSslPortEnabledInput")
    def non_ssl_port_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nonSslPortEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="patchScheduleInput")
    def patch_schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisCachePatchSchedule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisCachePatchSchedule"]]], jsii.get(self, "patchScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="privateStaticIpAddressInput")
    def private_static_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateStaticIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="redisConfigurationInput")
    def redis_configuration_input(
        self,
    ) -> typing.Optional["RedisCacheRedisConfiguration"]:
        return typing.cast(typing.Optional["RedisCacheRedisConfiguration"], jsii.get(self, "redisConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="redisVersionInput")
    def redis_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redisVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="replicasPerMasterInput")
    def replicas_per_master_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicasPerMasterInput"))

    @builtins.property
    @jsii.member(jsii_name="replicasPerPrimaryInput")
    def replicas_per_primary_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicasPerPrimaryInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="shardCountInput")
    def shard_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "shardCountInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantSettingsInput")
    def tenant_settings_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tenantSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RedisCacheTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "RedisCacheTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKeysAuthenticationEnabled")
    def access_keys_authentication_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessKeysAuthenticationEnabled"))

    @access_keys_authentication_enabled.setter
    def access_keys_authentication_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7813cfb4d3da89af531656bf59064eb75f1277bae6eb55a6ee30f41f99501b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeysAuthenticationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b7899296ec33d4477c9e2340dca53c5386c3a374097a28e91b003b5aff5b394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "family"))

    @family.setter
    def family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4583a20171473d835d5234e4283aed10b439d203c3095b10a1d86f01dd91ba2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "family", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d6133b1cad7b1d33498196005d0296093aaa1735b54353590d4880583088f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1a053b6442424ac9ee397d6d5efd32a774672819bdabacbb9932b0c6fcee60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumTlsVersion")
    def minimum_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumTlsVersion"))

    @minimum_tls_version.setter
    def minimum_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed987113b8b4b56149d92f85ec96de9b6cdb2acde4938f8c3c0da0cbc6af8061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumTlsVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c2470d5d063975f89197797c4b3c60c2f66b600c02238716d8774ccdcc37d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonSslPortEnabled")
    def non_ssl_port_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nonSslPortEnabled"))

    @non_ssl_port_enabled.setter
    def non_ssl_port_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26449550c8dd19ab4addc7cb291e413d345a3f718fedf34d87a7ac8ef1cf4115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonSslPortEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateStaticIpAddress")
    def private_static_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateStaticIpAddress"))

    @private_static_ip_address.setter
    def private_static_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b070e98b74e6b9cb7434f20a931b9917a48451923ab86113899e0e525bc7cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateStaticIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabled")
    def public_network_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicNetworkAccessEnabled"))

    @public_network_access_enabled.setter
    def public_network_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__481bf4ccbdc63fa953dc8afc6e6baf019464cab0444097faa73f33898f06c9e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redisVersion")
    def redis_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redisVersion"))

    @redis_version.setter
    def redis_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a4e5d5671ca38a2c61a074c636894763a240db8dd69d966f0222b9933ea757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicasPerMaster")
    def replicas_per_master(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicasPerMaster"))

    @replicas_per_master.setter
    def replicas_per_master(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e584a93ea7c9640426153433f17b0fdbbbc670d85f459434524519fb8deedc47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicasPerMaster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicasPerPrimary")
    def replicas_per_primary(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicasPerPrimary"))

    @replicas_per_primary.setter
    def replicas_per_primary(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324233a6232bfe0de0aaca4d3d0d2d3049355a35c53bddd83575a42606ec39df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicasPerPrimary", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd1fd1f3f7882f017887d4cb5120226ce90870c3098e7c596686f5bf051c0939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shardCount")
    def shard_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shardCount"))

    @shard_count.setter
    def shard_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad17b57ae7224502e6bdda7b68283707547451e9d2ab2cbebcf9e2d320f89ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shardCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e186d7ad22f1a2e22dac569bdab5bb76fbee16aa2c882901c19ce528ffc9cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375a790eb5d6c9de7c78c25500ca774c1a0528a3aa61cea43fcf633eaf1713eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f5f735e763ebeb1da1c247d7c0293c310fcc300e7549e982897037b786682b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantSettings")
    def tenant_settings(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tenantSettings"))

    @tenant_settings.setter
    def tenant_settings(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03dab2a45274f1119766c2a84fe117e55099eb117de906ec078126a9f2dee0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc2a8bd49f685944ac1659d0351b832b180bc9abbf2277d8d43cc064b32b1a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redisCache.RedisCacheConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "capacity": "capacity",
        "family": "family",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "sku_name": "skuName",
        "access_keys_authentication_enabled": "accessKeysAuthenticationEnabled",
        "id": "id",
        "identity": "identity",
        "minimum_tls_version": "minimumTlsVersion",
        "non_ssl_port_enabled": "nonSslPortEnabled",
        "patch_schedule": "patchSchedule",
        "private_static_ip_address": "privateStaticIpAddress",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "redis_configuration": "redisConfiguration",
        "redis_version": "redisVersion",
        "replicas_per_master": "replicasPerMaster",
        "replicas_per_primary": "replicasPerPrimary",
        "shard_count": "shardCount",
        "subnet_id": "subnetId",
        "tags": "tags",
        "tenant_settings": "tenantSettings",
        "timeouts": "timeouts",
        "zones": "zones",
    },
)
class RedisCacheConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        capacity: jsii.Number,
        family: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku_name: builtins.str,
        access_keys_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["RedisCacheIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        minimum_tls_version: typing.Optional[builtins.str] = None,
        non_ssl_port_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        patch_schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RedisCachePatchSchedule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        private_static_ip_address: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        redis_configuration: typing.Optional[typing.Union["RedisCacheRedisConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        redis_version: typing.Optional[builtins.str] = None,
        replicas_per_master: typing.Optional[jsii.Number] = None,
        replicas_per_primary: typing.Optional[jsii.Number] = None,
        shard_count: typing.Optional[jsii.Number] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenant_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["RedisCacheTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#capacity RedisCache#capacity}.
        :param family: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#family RedisCache#family}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#location RedisCache#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#name RedisCache#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#resource_group_name RedisCache#resource_group_name}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#sku_name RedisCache#sku_name}.
        :param access_keys_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#access_keys_authentication_enabled RedisCache#access_keys_authentication_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#id RedisCache#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#identity RedisCache#identity}
        :param minimum_tls_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#minimum_tls_version RedisCache#minimum_tls_version}.
        :param non_ssl_port_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#non_ssl_port_enabled RedisCache#non_ssl_port_enabled}.
        :param patch_schedule: patch_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#patch_schedule RedisCache#patch_schedule}
        :param private_static_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#private_static_ip_address RedisCache#private_static_ip_address}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#public_network_access_enabled RedisCache#public_network_access_enabled}.
        :param redis_configuration: redis_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#redis_configuration RedisCache#redis_configuration}
        :param redis_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#redis_version RedisCache#redis_version}.
        :param replicas_per_master: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#replicas_per_master RedisCache#replicas_per_master}.
        :param replicas_per_primary: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#replicas_per_primary RedisCache#replicas_per_primary}.
        :param shard_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#shard_count RedisCache#shard_count}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#subnet_id RedisCache#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#tags RedisCache#tags}.
        :param tenant_settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#tenant_settings RedisCache#tenant_settings}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#timeouts RedisCache#timeouts}
        :param zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#zones RedisCache#zones}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity, dict):
            identity = RedisCacheIdentity(**identity)
        if isinstance(redis_configuration, dict):
            redis_configuration = RedisCacheRedisConfiguration(**redis_configuration)
        if isinstance(timeouts, dict):
            timeouts = RedisCacheTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2694780dc864929ce36bd43db7a3489c908bb98a87bf629157e697b7c4434ea)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument access_keys_authentication_enabled", value=access_keys_authentication_enabled, expected_type=type_hints["access_keys_authentication_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument minimum_tls_version", value=minimum_tls_version, expected_type=type_hints["minimum_tls_version"])
            check_type(argname="argument non_ssl_port_enabled", value=non_ssl_port_enabled, expected_type=type_hints["non_ssl_port_enabled"])
            check_type(argname="argument patch_schedule", value=patch_schedule, expected_type=type_hints["patch_schedule"])
            check_type(argname="argument private_static_ip_address", value=private_static_ip_address, expected_type=type_hints["private_static_ip_address"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument redis_configuration", value=redis_configuration, expected_type=type_hints["redis_configuration"])
            check_type(argname="argument redis_version", value=redis_version, expected_type=type_hints["redis_version"])
            check_type(argname="argument replicas_per_master", value=replicas_per_master, expected_type=type_hints["replicas_per_master"])
            check_type(argname="argument replicas_per_primary", value=replicas_per_primary, expected_type=type_hints["replicas_per_primary"])
            check_type(argname="argument shard_count", value=shard_count, expected_type=type_hints["shard_count"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tenant_settings", value=tenant_settings, expected_type=type_hints["tenant_settings"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity": capacity,
            "family": family,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "sku_name": sku_name,
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
        if access_keys_authentication_enabled is not None:
            self._values["access_keys_authentication_enabled"] = access_keys_authentication_enabled
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if minimum_tls_version is not None:
            self._values["minimum_tls_version"] = minimum_tls_version
        if non_ssl_port_enabled is not None:
            self._values["non_ssl_port_enabled"] = non_ssl_port_enabled
        if patch_schedule is not None:
            self._values["patch_schedule"] = patch_schedule
        if private_static_ip_address is not None:
            self._values["private_static_ip_address"] = private_static_ip_address
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if redis_configuration is not None:
            self._values["redis_configuration"] = redis_configuration
        if redis_version is not None:
            self._values["redis_version"] = redis_version
        if replicas_per_master is not None:
            self._values["replicas_per_master"] = replicas_per_master
        if replicas_per_primary is not None:
            self._values["replicas_per_primary"] = replicas_per_primary
        if shard_count is not None:
            self._values["shard_count"] = shard_count
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tags is not None:
            self._values["tags"] = tags
        if tenant_settings is not None:
            self._values["tenant_settings"] = tenant_settings
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if zones is not None:
            self._values["zones"] = zones

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
    def capacity(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#capacity RedisCache#capacity}.'''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def family(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#family RedisCache#family}.'''
        result = self._values.get("family")
        assert result is not None, "Required property 'family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#location RedisCache#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#name RedisCache#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#resource_group_name RedisCache#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#sku_name RedisCache#sku_name}.'''
        result = self._values.get("sku_name")
        assert result is not None, "Required property 'sku_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_keys_authentication_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#access_keys_authentication_enabled RedisCache#access_keys_authentication_enabled}.'''
        result = self._values.get("access_keys_authentication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#id RedisCache#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["RedisCacheIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#identity RedisCache#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["RedisCacheIdentity"], result)

    @builtins.property
    def minimum_tls_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#minimum_tls_version RedisCache#minimum_tls_version}.'''
        result = self._values.get("minimum_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def non_ssl_port_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#non_ssl_port_enabled RedisCache#non_ssl_port_enabled}.'''
        result = self._values.get("non_ssl_port_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def patch_schedule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisCachePatchSchedule"]]]:
        '''patch_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#patch_schedule RedisCache#patch_schedule}
        '''
        result = self._values.get("patch_schedule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RedisCachePatchSchedule"]]], result)

    @builtins.property
    def private_static_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#private_static_ip_address RedisCache#private_static_ip_address}.'''
        result = self._values.get("private_static_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#public_network_access_enabled RedisCache#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def redis_configuration(self) -> typing.Optional["RedisCacheRedisConfiguration"]:
        '''redis_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#redis_configuration RedisCache#redis_configuration}
        '''
        result = self._values.get("redis_configuration")
        return typing.cast(typing.Optional["RedisCacheRedisConfiguration"], result)

    @builtins.property
    def redis_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#redis_version RedisCache#redis_version}.'''
        result = self._values.get("redis_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replicas_per_master(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#replicas_per_master RedisCache#replicas_per_master}.'''
        result = self._values.get("replicas_per_master")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replicas_per_primary(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#replicas_per_primary RedisCache#replicas_per_primary}.'''
        result = self._values.get("replicas_per_primary")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def shard_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#shard_count RedisCache#shard_count}.'''
        result = self._values.get("shard_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#subnet_id RedisCache#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#tags RedisCache#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tenant_settings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#tenant_settings RedisCache#tenant_settings}.'''
        result = self._values.get("tenant_settings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["RedisCacheTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#timeouts RedisCache#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["RedisCacheTimeouts"], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#zones RedisCache#zones}.'''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisCacheConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redisCache.RedisCacheIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class RedisCacheIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#type RedisCache#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#identity_ids RedisCache#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225b0d4fa429315c2f655b029ca86065fcbd6a7dfd0a39a4042b08f088de10eb)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#type RedisCache#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#identity_ids RedisCache#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisCacheIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisCacheIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redisCache.RedisCacheIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aebbc3102de335ce86ed3af59db872edf0deed9e41b8ceb05479672ee49a680)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3983be2caf755627b810d8790e3ca70a86682d03a641a52a0e5372cae1d0b970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d849d98632d1d133f9811374043c07ab8616c161dc5472b3a7fed378640867ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisCacheIdentity]:
        return typing.cast(typing.Optional[RedisCacheIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RedisCacheIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123e6791824321b885505751a7034f37771833d1ab18752461f5fa002e48ed7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redisCache.RedisCachePatchSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "day_of_week": "dayOfWeek",
        "maintenance_window": "maintenanceWindow",
        "start_hour_utc": "startHourUtc",
    },
)
class RedisCachePatchSchedule:
    def __init__(
        self,
        *,
        day_of_week: builtins.str,
        maintenance_window: typing.Optional[builtins.str] = None,
        start_hour_utc: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#day_of_week RedisCache#day_of_week}.
        :param maintenance_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maintenance_window RedisCache#maintenance_window}.
        :param start_hour_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#start_hour_utc RedisCache#start_hour_utc}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d26c87a7285aba89aac873c38521f2031edc785cad6d093f4d685bb4f879d9)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument start_hour_utc", value=start_hour_utc, expected_type=type_hints["start_hour_utc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
        }
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if start_hour_utc is not None:
            self._values["start_hour_utc"] = start_hour_utc

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#day_of_week RedisCache#day_of_week}.'''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maintenance_window RedisCache#maintenance_window}.'''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_hour_utc(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#start_hour_utc RedisCache#start_hour_utc}.'''
        result = self._values.get("start_hour_utc")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisCachePatchSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisCachePatchScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redisCache.RedisCachePatchScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10ddbec86df9315a21519538dad56e6279c544c6e1dbbf67658c5f2acc578fe1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RedisCachePatchScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4d84fceb05f81022a22cc2749dc4348201b0468a6707825443dec1ef2729af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RedisCachePatchScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4194cf3fff6ac63145a8d386684a9e55a5ab0ae51bcd6b8dad3a9d1eeae69b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__369ebdeaf3eddd805d5442cb2327005dc76702ebf6bf3a34acc11bab370928b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05290112ad1277ab3c8fb64069eea83d6d9269c74d1954a15d2ad15a2721c159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisCachePatchSchedule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisCachePatchSchedule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisCachePatchSchedule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3585e8d5fe5e318667270eb18b8b299d676fe249cd48e2e03557c59f20f9fbcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RedisCachePatchScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redisCache.RedisCachePatchScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae5391f66d5fca6ff2c41ecbd39b7f1e6a85e7a3be622348e4ba56b13d95124d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetStartHourUtc")
    def reset_start_hour_utc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartHourUtc", []))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="startHourUtcInput")
    def start_hour_utc_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startHourUtcInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3988e022df2449ddcda4ff1fb94591c352d889bd6bc14dd53fbffceaf412c066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceWindow"))

    @maintenance_window.setter
    def maintenance_window(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2452617c8e177e3eb54260e00fec0c087cb294104ca662604b95d59a5e5db7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startHourUtc")
    def start_hour_utc(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startHourUtc"))

    @start_hour_utc.setter
    def start_hour_utc(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad822485de43508c1e0a0765e41db5aec379a23811e20bf5a19b23af2b4710e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startHourUtc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisCachePatchSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisCachePatchSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisCachePatchSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8129a85a59d404c642da0d04497c9276cf1c97a666d4a51a7382854f7ca505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redisCache.RedisCacheRedisConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "active_directory_authentication_enabled": "activeDirectoryAuthenticationEnabled",
        "aof_backup_enabled": "aofBackupEnabled",
        "aof_storage_connection_string0": "aofStorageConnectionString0",
        "aof_storage_connection_string1": "aofStorageConnectionString1",
        "authentication_enabled": "authenticationEnabled",
        "data_persistence_authentication_method": "dataPersistenceAuthenticationMethod",
        "maxfragmentationmemory_reserved": "maxfragmentationmemoryReserved",
        "maxmemory_delta": "maxmemoryDelta",
        "maxmemory_policy": "maxmemoryPolicy",
        "maxmemory_reserved": "maxmemoryReserved",
        "notify_keyspace_events": "notifyKeyspaceEvents",
        "rdb_backup_enabled": "rdbBackupEnabled",
        "rdb_backup_frequency": "rdbBackupFrequency",
        "rdb_backup_max_snapshot_count": "rdbBackupMaxSnapshotCount",
        "rdb_storage_connection_string": "rdbStorageConnectionString",
        "storage_account_subscription_id": "storageAccountSubscriptionId",
    },
)
class RedisCacheRedisConfiguration:
    def __init__(
        self,
        *,
        active_directory_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        aof_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        aof_storage_connection_string0: typing.Optional[builtins.str] = None,
        aof_storage_connection_string1: typing.Optional[builtins.str] = None,
        authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_persistence_authentication_method: typing.Optional[builtins.str] = None,
        maxfragmentationmemory_reserved: typing.Optional[jsii.Number] = None,
        maxmemory_delta: typing.Optional[jsii.Number] = None,
        maxmemory_policy: typing.Optional[builtins.str] = None,
        maxmemory_reserved: typing.Optional[jsii.Number] = None,
        notify_keyspace_events: typing.Optional[builtins.str] = None,
        rdb_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rdb_backup_frequency: typing.Optional[jsii.Number] = None,
        rdb_backup_max_snapshot_count: typing.Optional[jsii.Number] = None,
        rdb_storage_connection_string: typing.Optional[builtins.str] = None,
        storage_account_subscription_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param active_directory_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#active_directory_authentication_enabled RedisCache#active_directory_authentication_enabled}.
        :param aof_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#aof_backup_enabled RedisCache#aof_backup_enabled}.
        :param aof_storage_connection_string0: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#aof_storage_connection_string_0 RedisCache#aof_storage_connection_string_0}.
        :param aof_storage_connection_string1: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#aof_storage_connection_string_1 RedisCache#aof_storage_connection_string_1}.
        :param authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#authentication_enabled RedisCache#authentication_enabled}.
        :param data_persistence_authentication_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#data_persistence_authentication_method RedisCache#data_persistence_authentication_method}.
        :param maxfragmentationmemory_reserved: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxfragmentationmemory_reserved RedisCache#maxfragmentationmemory_reserved}.
        :param maxmemory_delta: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxmemory_delta RedisCache#maxmemory_delta}.
        :param maxmemory_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxmemory_policy RedisCache#maxmemory_policy}.
        :param maxmemory_reserved: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxmemory_reserved RedisCache#maxmemory_reserved}.
        :param notify_keyspace_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#notify_keyspace_events RedisCache#notify_keyspace_events}.
        :param rdb_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_backup_enabled RedisCache#rdb_backup_enabled}.
        :param rdb_backup_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_backup_frequency RedisCache#rdb_backup_frequency}.
        :param rdb_backup_max_snapshot_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_backup_max_snapshot_count RedisCache#rdb_backup_max_snapshot_count}.
        :param rdb_storage_connection_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_storage_connection_string RedisCache#rdb_storage_connection_string}.
        :param storage_account_subscription_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#storage_account_subscription_id RedisCache#storage_account_subscription_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f70c63e765f0bdc7bc585f64cce8371aa515b0b34bd00a79a2324a6dfc9e3c6)
            check_type(argname="argument active_directory_authentication_enabled", value=active_directory_authentication_enabled, expected_type=type_hints["active_directory_authentication_enabled"])
            check_type(argname="argument aof_backup_enabled", value=aof_backup_enabled, expected_type=type_hints["aof_backup_enabled"])
            check_type(argname="argument aof_storage_connection_string0", value=aof_storage_connection_string0, expected_type=type_hints["aof_storage_connection_string0"])
            check_type(argname="argument aof_storage_connection_string1", value=aof_storage_connection_string1, expected_type=type_hints["aof_storage_connection_string1"])
            check_type(argname="argument authentication_enabled", value=authentication_enabled, expected_type=type_hints["authentication_enabled"])
            check_type(argname="argument data_persistence_authentication_method", value=data_persistence_authentication_method, expected_type=type_hints["data_persistence_authentication_method"])
            check_type(argname="argument maxfragmentationmemory_reserved", value=maxfragmentationmemory_reserved, expected_type=type_hints["maxfragmentationmemory_reserved"])
            check_type(argname="argument maxmemory_delta", value=maxmemory_delta, expected_type=type_hints["maxmemory_delta"])
            check_type(argname="argument maxmemory_policy", value=maxmemory_policy, expected_type=type_hints["maxmemory_policy"])
            check_type(argname="argument maxmemory_reserved", value=maxmemory_reserved, expected_type=type_hints["maxmemory_reserved"])
            check_type(argname="argument notify_keyspace_events", value=notify_keyspace_events, expected_type=type_hints["notify_keyspace_events"])
            check_type(argname="argument rdb_backup_enabled", value=rdb_backup_enabled, expected_type=type_hints["rdb_backup_enabled"])
            check_type(argname="argument rdb_backup_frequency", value=rdb_backup_frequency, expected_type=type_hints["rdb_backup_frequency"])
            check_type(argname="argument rdb_backup_max_snapshot_count", value=rdb_backup_max_snapshot_count, expected_type=type_hints["rdb_backup_max_snapshot_count"])
            check_type(argname="argument rdb_storage_connection_string", value=rdb_storage_connection_string, expected_type=type_hints["rdb_storage_connection_string"])
            check_type(argname="argument storage_account_subscription_id", value=storage_account_subscription_id, expected_type=type_hints["storage_account_subscription_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_directory_authentication_enabled is not None:
            self._values["active_directory_authentication_enabled"] = active_directory_authentication_enabled
        if aof_backup_enabled is not None:
            self._values["aof_backup_enabled"] = aof_backup_enabled
        if aof_storage_connection_string0 is not None:
            self._values["aof_storage_connection_string0"] = aof_storage_connection_string0
        if aof_storage_connection_string1 is not None:
            self._values["aof_storage_connection_string1"] = aof_storage_connection_string1
        if authentication_enabled is not None:
            self._values["authentication_enabled"] = authentication_enabled
        if data_persistence_authentication_method is not None:
            self._values["data_persistence_authentication_method"] = data_persistence_authentication_method
        if maxfragmentationmemory_reserved is not None:
            self._values["maxfragmentationmemory_reserved"] = maxfragmentationmemory_reserved
        if maxmemory_delta is not None:
            self._values["maxmemory_delta"] = maxmemory_delta
        if maxmemory_policy is not None:
            self._values["maxmemory_policy"] = maxmemory_policy
        if maxmemory_reserved is not None:
            self._values["maxmemory_reserved"] = maxmemory_reserved
        if notify_keyspace_events is not None:
            self._values["notify_keyspace_events"] = notify_keyspace_events
        if rdb_backup_enabled is not None:
            self._values["rdb_backup_enabled"] = rdb_backup_enabled
        if rdb_backup_frequency is not None:
            self._values["rdb_backup_frequency"] = rdb_backup_frequency
        if rdb_backup_max_snapshot_count is not None:
            self._values["rdb_backup_max_snapshot_count"] = rdb_backup_max_snapshot_count
        if rdb_storage_connection_string is not None:
            self._values["rdb_storage_connection_string"] = rdb_storage_connection_string
        if storage_account_subscription_id is not None:
            self._values["storage_account_subscription_id"] = storage_account_subscription_id

    @builtins.property
    def active_directory_authentication_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#active_directory_authentication_enabled RedisCache#active_directory_authentication_enabled}.'''
        result = self._values.get("active_directory_authentication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def aof_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#aof_backup_enabled RedisCache#aof_backup_enabled}.'''
        result = self._values.get("aof_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def aof_storage_connection_string0(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#aof_storage_connection_string_0 RedisCache#aof_storage_connection_string_0}.'''
        result = self._values.get("aof_storage_connection_string0")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aof_storage_connection_string1(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#aof_storage_connection_string_1 RedisCache#aof_storage_connection_string_1}.'''
        result = self._values.get("aof_storage_connection_string1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#authentication_enabled RedisCache#authentication_enabled}.'''
        result = self._values.get("authentication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def data_persistence_authentication_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#data_persistence_authentication_method RedisCache#data_persistence_authentication_method}.'''
        result = self._values.get("data_persistence_authentication_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maxfragmentationmemory_reserved(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxfragmentationmemory_reserved RedisCache#maxfragmentationmemory_reserved}.'''
        result = self._values.get("maxfragmentationmemory_reserved")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maxmemory_delta(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxmemory_delta RedisCache#maxmemory_delta}.'''
        result = self._values.get("maxmemory_delta")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maxmemory_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxmemory_policy RedisCache#maxmemory_policy}.'''
        result = self._values.get("maxmemory_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maxmemory_reserved(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#maxmemory_reserved RedisCache#maxmemory_reserved}.'''
        result = self._values.get("maxmemory_reserved")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def notify_keyspace_events(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#notify_keyspace_events RedisCache#notify_keyspace_events}.'''
        result = self._values.get("notify_keyspace_events")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rdb_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_backup_enabled RedisCache#rdb_backup_enabled}.'''
        result = self._values.get("rdb_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rdb_backup_frequency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_backup_frequency RedisCache#rdb_backup_frequency}.'''
        result = self._values.get("rdb_backup_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rdb_backup_max_snapshot_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_backup_max_snapshot_count RedisCache#rdb_backup_max_snapshot_count}.'''
        result = self._values.get("rdb_backup_max_snapshot_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rdb_storage_connection_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#rdb_storage_connection_string RedisCache#rdb_storage_connection_string}.'''
        result = self._values.get("rdb_storage_connection_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_subscription_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#storage_account_subscription_id RedisCache#storage_account_subscription_id}.'''
        result = self._values.get("storage_account_subscription_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisCacheRedisConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisCacheRedisConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redisCache.RedisCacheRedisConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ba3a73f7ce31359c15ea011c40505c9398cf52f3f1a6d8dde142cee042860a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActiveDirectoryAuthenticationEnabled")
    def reset_active_directory_authentication_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectoryAuthenticationEnabled", []))

    @jsii.member(jsii_name="resetAofBackupEnabled")
    def reset_aof_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAofBackupEnabled", []))

    @jsii.member(jsii_name="resetAofStorageConnectionString0")
    def reset_aof_storage_connection_string0(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAofStorageConnectionString0", []))

    @jsii.member(jsii_name="resetAofStorageConnectionString1")
    def reset_aof_storage_connection_string1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAofStorageConnectionString1", []))

    @jsii.member(jsii_name="resetAuthenticationEnabled")
    def reset_authentication_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationEnabled", []))

    @jsii.member(jsii_name="resetDataPersistenceAuthenticationMethod")
    def reset_data_persistence_authentication_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataPersistenceAuthenticationMethod", []))

    @jsii.member(jsii_name="resetMaxfragmentationmemoryReserved")
    def reset_maxfragmentationmemory_reserved(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxfragmentationmemoryReserved", []))

    @jsii.member(jsii_name="resetMaxmemoryDelta")
    def reset_maxmemory_delta(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxmemoryDelta", []))

    @jsii.member(jsii_name="resetMaxmemoryPolicy")
    def reset_maxmemory_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxmemoryPolicy", []))

    @jsii.member(jsii_name="resetMaxmemoryReserved")
    def reset_maxmemory_reserved(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxmemoryReserved", []))

    @jsii.member(jsii_name="resetNotifyKeyspaceEvents")
    def reset_notify_keyspace_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyKeyspaceEvents", []))

    @jsii.member(jsii_name="resetRdbBackupEnabled")
    def reset_rdb_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbBackupEnabled", []))

    @jsii.member(jsii_name="resetRdbBackupFrequency")
    def reset_rdb_backup_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbBackupFrequency", []))

    @jsii.member(jsii_name="resetRdbBackupMaxSnapshotCount")
    def reset_rdb_backup_max_snapshot_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbBackupMaxSnapshotCount", []))

    @jsii.member(jsii_name="resetRdbStorageConnectionString")
    def reset_rdb_storage_connection_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRdbStorageConnectionString", []))

    @jsii.member(jsii_name="resetStorageAccountSubscriptionId")
    def reset_storage_account_subscription_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountSubscriptionId", []))

    @builtins.property
    @jsii.member(jsii_name="maxclients")
    def maxclients(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxclients"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryAuthenticationEnabledInput")
    def active_directory_authentication_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activeDirectoryAuthenticationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="aofBackupEnabledInput")
    def aof_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "aofBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="aofStorageConnectionString0Input")
    def aof_storage_connection_string0_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aofStorageConnectionString0Input"))

    @builtins.property
    @jsii.member(jsii_name="aofStorageConnectionString1Input")
    def aof_storage_connection_string1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aofStorageConnectionString1Input"))

    @builtins.property
    @jsii.member(jsii_name="authenticationEnabledInput")
    def authentication_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "authenticationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dataPersistenceAuthenticationMethodInput")
    def data_persistence_authentication_method_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataPersistenceAuthenticationMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="maxfragmentationmemoryReservedInput")
    def maxfragmentationmemory_reserved_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxfragmentationmemoryReservedInput"))

    @builtins.property
    @jsii.member(jsii_name="maxmemoryDeltaInput")
    def maxmemory_delta_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxmemoryDeltaInput"))

    @builtins.property
    @jsii.member(jsii_name="maxmemoryPolicyInput")
    def maxmemory_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxmemoryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxmemoryReservedInput")
    def maxmemory_reserved_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxmemoryReservedInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyKeyspaceEventsInput")
    def notify_keyspace_events_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notifyKeyspaceEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbBackupEnabledInput")
    def rdb_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rdbBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbBackupFrequencyInput")
    def rdb_backup_frequency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rdbBackupFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbBackupMaxSnapshotCountInput")
    def rdb_backup_max_snapshot_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rdbBackupMaxSnapshotCountInput"))

    @builtins.property
    @jsii.member(jsii_name="rdbStorageConnectionStringInput")
    def rdb_storage_connection_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rdbStorageConnectionStringInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountSubscriptionIdInput")
    def storage_account_subscription_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountSubscriptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryAuthenticationEnabled")
    def active_directory_authentication_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "activeDirectoryAuthenticationEnabled"))

    @active_directory_authentication_enabled.setter
    def active_directory_authentication_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa904894faa7e4c891e8e899d7208463b1b905c32a4016dbd88ac43fa6793ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectoryAuthenticationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="aofBackupEnabled")
    def aof_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "aofBackupEnabled"))

    @aof_backup_enabled.setter
    def aof_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ec3223fe55246a4eee1896443d4e9a509fceef518bb03bf0484941364c01f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aofBackupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="aofStorageConnectionString0")
    def aof_storage_connection_string0(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aofStorageConnectionString0"))

    @aof_storage_connection_string0.setter
    def aof_storage_connection_string0(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5c6513beacaf5fb4168c998ec18522155d38ebdd0733b09255e3a04b968ac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aofStorageConnectionString0", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="aofStorageConnectionString1")
    def aof_storage_connection_string1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aofStorageConnectionString1"))

    @aof_storage_connection_string1.setter
    def aof_storage_connection_string1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb40e4271c318718c38e2e9b9e3def29ce178cc2f8524fb8c92f67466b03f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aofStorageConnectionString1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authenticationEnabled")
    def authentication_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "authenticationEnabled"))

    @authentication_enabled.setter
    def authentication_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f25b5fe50899932b8e2d4a7e7b04c35485e2e6cdb538ece2c39556f3194dcf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataPersistenceAuthenticationMethod")
    def data_persistence_authentication_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataPersistenceAuthenticationMethod"))

    @data_persistence_authentication_method.setter
    def data_persistence_authentication_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8695da1dcf102ce1825d61111762462345bc097f83437c2b10715302ec7df0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataPersistenceAuthenticationMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxfragmentationmemoryReserved")
    def maxfragmentationmemory_reserved(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxfragmentationmemoryReserved"))

    @maxfragmentationmemory_reserved.setter
    def maxfragmentationmemory_reserved(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496ffaae3fa9b216e7b36e6bf53f805a3602d76cc0ce16671e51c0f1bb41dd1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxfragmentationmemoryReserved", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxmemoryDelta")
    def maxmemory_delta(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxmemoryDelta"))

    @maxmemory_delta.setter
    def maxmemory_delta(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92f77adbe766e5c76a49cd4bcdde7f019b87358928fe4962f244ca1014227043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxmemoryDelta", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxmemoryPolicy")
    def maxmemory_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxmemoryPolicy"))

    @maxmemory_policy.setter
    def maxmemory_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f15d3ae44338dbf529662451dff41b45c9003019ad6730929bfdba045aaa17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxmemoryPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxmemoryReserved")
    def maxmemory_reserved(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxmemoryReserved"))

    @maxmemory_reserved.setter
    def maxmemory_reserved(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14dac744005627a9790180b3de53e42118de02974c5afb4df94d636e5d8f9371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxmemoryReserved", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyKeyspaceEvents")
    def notify_keyspace_events(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notifyKeyspaceEvents"))

    @notify_keyspace_events.setter
    def notify_keyspace_events(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f210fd2a2cd4a9968c93943ab10d0fb618285758e42318b5881f619ccdd07a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyKeyspaceEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rdbBackupEnabled")
    def rdb_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rdbBackupEnabled"))

    @rdb_backup_enabled.setter
    def rdb_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab94448141fd6f0f7e6f407e0a2c2354d9ab4a51102a88d265046886b16d3c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbBackupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rdbBackupFrequency")
    def rdb_backup_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rdbBackupFrequency"))

    @rdb_backup_frequency.setter
    def rdb_backup_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89505d544976d15ba3a678c1643e2c18144eda838c1d6ccb8a5cf3db5a26ce12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbBackupFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rdbBackupMaxSnapshotCount")
    def rdb_backup_max_snapshot_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rdbBackupMaxSnapshotCount"))

    @rdb_backup_max_snapshot_count.setter
    def rdb_backup_max_snapshot_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e2ef4c3c8fc1b9fb1d5b6ef9c32216ebbfc409e0d5fd58d72dd17712dde59d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbBackupMaxSnapshotCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rdbStorageConnectionString")
    def rdb_storage_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdbStorageConnectionString"))

    @rdb_storage_connection_string.setter
    def rdb_storage_connection_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d8b4a9c1c148dab7a689263a2f9b429b2db652ac6295227b6c7b23a96b3451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdbStorageConnectionString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountSubscriptionId")
    def storage_account_subscription_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountSubscriptionId"))

    @storage_account_subscription_id.setter
    def storage_account_subscription_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138e0dd1e13cc5b392f2f2a35a0e0902594a1dd7279139eb0a4841a0e17b871a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountSubscriptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RedisCacheRedisConfiguration]:
        return typing.cast(typing.Optional[RedisCacheRedisConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RedisCacheRedisConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c59596414e9be390251a34052172e924be520e2f24f572942485833abe13df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.redisCache.RedisCacheTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class RedisCacheTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#create RedisCache#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#delete RedisCache#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#read RedisCache#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#update RedisCache#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05716320daffa76862c0353c8a5a85cb090c4dd426a8795e58f7bf5383c53b9a)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#create RedisCache#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#delete RedisCache#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#read RedisCache#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/redis_cache#update RedisCache#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedisCacheTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedisCacheTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.redisCache.RedisCacheTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0e11ab5f79ac31be41c61ed31af9d77fd205b65fe1e3a2986c2a8e30ada452b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a1c4221a5ae81d87fbf415b0d88aae4894b95ad271239c8826edd5ca06098b4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e72fcbf8168a4b26d2c3591723cae87f927419edad815565b47cde8e61e717ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4240ca74c959042ff853cbc445438e591ddc13b1625379ced9506a17099f40a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39fc5f14d6a87f9ac59301dd405734648bc7d6d29b163f6545166459f8ee83bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisCacheTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisCacheTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisCacheTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a144359689ebf0c73bd83ed24541ffec2da99d5a50f18ac522d35f58b5b117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RedisCache",
    "RedisCacheConfig",
    "RedisCacheIdentity",
    "RedisCacheIdentityOutputReference",
    "RedisCachePatchSchedule",
    "RedisCachePatchScheduleList",
    "RedisCachePatchScheduleOutputReference",
    "RedisCacheRedisConfiguration",
    "RedisCacheRedisConfigurationOutputReference",
    "RedisCacheTimeouts",
    "RedisCacheTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__eeaaf0a6422abbe43b925106121aa0f645fc74b48706b58fc82ad889d5b9f158(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    capacity: jsii.Number,
    family: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku_name: builtins.str,
    access_keys_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[RedisCacheIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    minimum_tls_version: typing.Optional[builtins.str] = None,
    non_ssl_port_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    patch_schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisCachePatchSchedule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    private_static_ip_address: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    redis_configuration: typing.Optional[typing.Union[RedisCacheRedisConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    redis_version: typing.Optional[builtins.str] = None,
    replicas_per_master: typing.Optional[jsii.Number] = None,
    replicas_per_primary: typing.Optional[jsii.Number] = None,
    shard_count: typing.Optional[jsii.Number] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenant_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RedisCacheTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__684ca5039fb00f21659d78a4f73e5f131ba5af6f4029c55792d5f405889ff0b7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232fb5b1d59835d910902483c34f146479f81cc0e83cddee65f429ae82f3a4db(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisCachePatchSchedule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7813cfb4d3da89af531656bf59064eb75f1277bae6eb55a6ee30f41f99501b90(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7899296ec33d4477c9e2340dca53c5386c3a374097a28e91b003b5aff5b394(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4583a20171473d835d5234e4283aed10b439d203c3095b10a1d86f01dd91ba2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d6133b1cad7b1d33498196005d0296093aaa1735b54353590d4880583088f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1a053b6442424ac9ee397d6d5efd32a774672819bdabacbb9932b0c6fcee60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed987113b8b4b56149d92f85ec96de9b6cdb2acde4938f8c3c0da0cbc6af8061(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c2470d5d063975f89197797c4b3c60c2f66b600c02238716d8774ccdcc37d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26449550c8dd19ab4addc7cb291e413d345a3f718fedf34d87a7ac8ef1cf4115(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b070e98b74e6b9cb7434f20a931b9917a48451923ab86113899e0e525bc7cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481bf4ccbdc63fa953dc8afc6e6baf019464cab0444097faa73f33898f06c9e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a4e5d5671ca38a2c61a074c636894763a240db8dd69d966f0222b9933ea757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e584a93ea7c9640426153433f17b0fdbbbc670d85f459434524519fb8deedc47(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324233a6232bfe0de0aaca4d3d0d2d3049355a35c53bddd83575a42606ec39df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1fd1f3f7882f017887d4cb5120226ce90870c3098e7c596686f5bf051c0939(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad17b57ae7224502e6bdda7b68283707547451e9d2ab2cbebcf9e2d320f89ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e186d7ad22f1a2e22dac569bdab5bb76fbee16aa2c882901c19ce528ffc9cc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375a790eb5d6c9de7c78c25500ca774c1a0528a3aa61cea43fcf633eaf1713eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f5f735e763ebeb1da1c247d7c0293c310fcc300e7549e982897037b786682b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03dab2a45274f1119766c2a84fe117e55099eb117de906ec078126a9f2dee0a2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc2a8bd49f685944ac1659d0351b832b180bc9abbf2277d8d43cc064b32b1a7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2694780dc864929ce36bd43db7a3489c908bb98a87bf629157e697b7c4434ea(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity: jsii.Number,
    family: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku_name: builtins.str,
    access_keys_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[RedisCacheIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    minimum_tls_version: typing.Optional[builtins.str] = None,
    non_ssl_port_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    patch_schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RedisCachePatchSchedule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    private_static_ip_address: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    redis_configuration: typing.Optional[typing.Union[RedisCacheRedisConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    redis_version: typing.Optional[builtins.str] = None,
    replicas_per_master: typing.Optional[jsii.Number] = None,
    replicas_per_primary: typing.Optional[jsii.Number] = None,
    shard_count: typing.Optional[jsii.Number] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenant_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[RedisCacheTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225b0d4fa429315c2f655b029ca86065fcbd6a7dfd0a39a4042b08f088de10eb(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aebbc3102de335ce86ed3af59db872edf0deed9e41b8ceb05479672ee49a680(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3983be2caf755627b810d8790e3ca70a86682d03a641a52a0e5372cae1d0b970(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d849d98632d1d133f9811374043c07ab8616c161dc5472b3a7fed378640867ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123e6791824321b885505751a7034f37771833d1ab18752461f5fa002e48ed7c(
    value: typing.Optional[RedisCacheIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d26c87a7285aba89aac873c38521f2031edc785cad6d093f4d685bb4f879d9(
    *,
    day_of_week: builtins.str,
    maintenance_window: typing.Optional[builtins.str] = None,
    start_hour_utc: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ddbec86df9315a21519538dad56e6279c544c6e1dbbf67658c5f2acc578fe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4d84fceb05f81022a22cc2749dc4348201b0468a6707825443dec1ef2729af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4194cf3fff6ac63145a8d386684a9e55a5ab0ae51bcd6b8dad3a9d1eeae69b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369ebdeaf3eddd805d5442cb2327005dc76702ebf6bf3a34acc11bab370928b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05290112ad1277ab3c8fb64069eea83d6d9269c74d1954a15d2ad15a2721c159(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3585e8d5fe5e318667270eb18b8b299d676fe249cd48e2e03557c59f20f9fbcf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RedisCachePatchSchedule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5391f66d5fca6ff2c41ecbd39b7f1e6a85e7a3be622348e4ba56b13d95124d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3988e022df2449ddcda4ff1fb94591c352d889bd6bc14dd53fbffceaf412c066(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2452617c8e177e3eb54260e00fec0c087cb294104ca662604b95d59a5e5db7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad822485de43508c1e0a0765e41db5aec379a23811e20bf5a19b23af2b4710e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8129a85a59d404c642da0d04497c9276cf1c97a666d4a51a7382854f7ca505(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisCachePatchSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f70c63e765f0bdc7bc585f64cce8371aa515b0b34bd00a79a2324a6dfc9e3c6(
    *,
    active_directory_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    aof_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    aof_storage_connection_string0: typing.Optional[builtins.str] = None,
    aof_storage_connection_string1: typing.Optional[builtins.str] = None,
    authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    data_persistence_authentication_method: typing.Optional[builtins.str] = None,
    maxfragmentationmemory_reserved: typing.Optional[jsii.Number] = None,
    maxmemory_delta: typing.Optional[jsii.Number] = None,
    maxmemory_policy: typing.Optional[builtins.str] = None,
    maxmemory_reserved: typing.Optional[jsii.Number] = None,
    notify_keyspace_events: typing.Optional[builtins.str] = None,
    rdb_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rdb_backup_frequency: typing.Optional[jsii.Number] = None,
    rdb_backup_max_snapshot_count: typing.Optional[jsii.Number] = None,
    rdb_storage_connection_string: typing.Optional[builtins.str] = None,
    storage_account_subscription_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba3a73f7ce31359c15ea011c40505c9398cf52f3f1a6d8dde142cee042860a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa904894faa7e4c891e8e899d7208463b1b905c32a4016dbd88ac43fa6793ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ec3223fe55246a4eee1896443d4e9a509fceef518bb03bf0484941364c01f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5c6513beacaf5fb4168c998ec18522155d38ebdd0733b09255e3a04b968ac2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb40e4271c318718c38e2e9b9e3def29ce178cc2f8524fb8c92f67466b03f54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f25b5fe50899932b8e2d4a7e7b04c35485e2e6cdb538ece2c39556f3194dcf9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8695da1dcf102ce1825d61111762462345bc097f83437c2b10715302ec7df0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496ffaae3fa9b216e7b36e6bf53f805a3602d76cc0ce16671e51c0f1bb41dd1c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f77adbe766e5c76a49cd4bcdde7f019b87358928fe4962f244ca1014227043(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f15d3ae44338dbf529662451dff41b45c9003019ad6730929bfdba045aaa17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14dac744005627a9790180b3de53e42118de02974c5afb4df94d636e5d8f9371(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f210fd2a2cd4a9968c93943ab10d0fb618285758e42318b5881f619ccdd07a11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab94448141fd6f0f7e6f407e0a2c2354d9ab4a51102a88d265046886b16d3c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89505d544976d15ba3a678c1643e2c18144eda838c1d6ccb8a5cf3db5a26ce12(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e2ef4c3c8fc1b9fb1d5b6ef9c32216ebbfc409e0d5fd58d72dd17712dde59d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d8b4a9c1c148dab7a689263a2f9b429b2db652ac6295227b6c7b23a96b3451(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138e0dd1e13cc5b392f2f2a35a0e0902594a1dd7279139eb0a4841a0e17b871a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c59596414e9be390251a34052172e924be520e2f24f572942485833abe13df(
    value: typing.Optional[RedisCacheRedisConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05716320daffa76862c0353c8a5a85cb090c4dd426a8795e58f7bf5383c53b9a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e11ab5f79ac31be41c61ed31af9d77fd205b65fe1e3a2986c2a8e30ada452b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c4221a5ae81d87fbf415b0d88aae4894b95ad271239c8826edd5ca06098b4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72fcbf8168a4b26d2c3591723cae87f927419edad815565b47cde8e61e717ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4240ca74c959042ff853cbc445438e591ddc13b1625379ced9506a17099f40a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39fc5f14d6a87f9ac59301dd405734648bc7d6d29b163f6545166459f8ee83bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a144359689ebf0c73bd83ed24541ffec2da99d5a50f18ac522d35f58b5b117(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RedisCacheTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
