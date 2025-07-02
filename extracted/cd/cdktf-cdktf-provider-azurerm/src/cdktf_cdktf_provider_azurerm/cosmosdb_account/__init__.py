r'''
# `azurerm_cosmosdb_account`

Refer to the Terraform Registry for docs: [`azurerm_cosmosdb_account`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account).
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


class CosmosdbAccount(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccount",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account azurerm_cosmosdb_account}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        consistency_policy: typing.Union["CosmosdbAccountConsistencyPolicy", typing.Dict[builtins.str, typing.Any]],
        geo_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountGeoLocation", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        offer_type: builtins.str,
        resource_group_name: builtins.str,
        access_key_metadata_writes_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        analytical_storage: typing.Optional[typing.Union["CosmosdbAccountAnalyticalStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        analytical_storage_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backup: typing.Optional[typing.Union["CosmosdbAccountBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        burst_capacity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        capabilities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountCapabilities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        capacity: typing.Optional[typing.Union["CosmosdbAccountCapacity", typing.Dict[builtins.str, typing.Any]]] = None,
        cors_rule: typing.Optional[typing.Union["CosmosdbAccountCorsRule", typing.Dict[builtins.str, typing.Any]]] = None,
        create_mode: typing.Optional[builtins.str] = None,
        default_identity_type: typing.Optional[builtins.str] = None,
        free_tier_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["CosmosdbAccountIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_range_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_virtual_network_filter_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_vault_key_id: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        local_authentication_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        managed_hsm_key_id: typing.Optional[builtins.str] = None,
        minimal_tls_version: typing.Optional[builtins.str] = None,
        mongo_server_version: typing.Optional[builtins.str] = None,
        multiple_write_locations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_acl_bypass_for_azure_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_acl_bypass_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        partition_merge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restore: typing.Optional[typing.Union["CosmosdbAccountRestore", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CosmosdbAccountTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountVirtualNetworkRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account azurerm_cosmosdb_account} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param consistency_policy: consistency_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#consistency_policy CosmosdbAccount#consistency_policy}
        :param geo_location: geo_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#geo_location CosmosdbAccount#geo_location}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#location CosmosdbAccount#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#name CosmosdbAccount#name}.
        :param offer_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#offer_type CosmosdbAccount#offer_type}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#resource_group_name CosmosdbAccount#resource_group_name}.
        :param access_key_metadata_writes_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#access_key_metadata_writes_enabled CosmosdbAccount#access_key_metadata_writes_enabled}.
        :param analytical_storage: analytical_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#analytical_storage CosmosdbAccount#analytical_storage}
        :param analytical_storage_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#analytical_storage_enabled CosmosdbAccount#analytical_storage_enabled}.
        :param automatic_failover_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#automatic_failover_enabled CosmosdbAccount#automatic_failover_enabled}.
        :param backup: backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#backup CosmosdbAccount#backup}
        :param burst_capacity_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#burst_capacity_enabled CosmosdbAccount#burst_capacity_enabled}.
        :param capabilities: capabilities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#capabilities CosmosdbAccount#capabilities}
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#capacity CosmosdbAccount#capacity}
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#cors_rule CosmosdbAccount#cors_rule}
        :param create_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#create_mode CosmosdbAccount#create_mode}.
        :param default_identity_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#default_identity_type CosmosdbAccount#default_identity_type}.
        :param free_tier_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#free_tier_enabled CosmosdbAccount#free_tier_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#id CosmosdbAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#identity CosmosdbAccount#identity}
        :param ip_range_filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#ip_range_filter CosmosdbAccount#ip_range_filter}.
        :param is_virtual_network_filter_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#is_virtual_network_filter_enabled CosmosdbAccount#is_virtual_network_filter_enabled}.
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#key_vault_key_id CosmosdbAccount#key_vault_key_id}.
        :param kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#kind CosmosdbAccount#kind}.
        :param local_authentication_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#local_authentication_disabled CosmosdbAccount#local_authentication_disabled}.
        :param managed_hsm_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#managed_hsm_key_id CosmosdbAccount#managed_hsm_key_id}.
        :param minimal_tls_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#minimal_tls_version CosmosdbAccount#minimal_tls_version}.
        :param mongo_server_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#mongo_server_version CosmosdbAccount#mongo_server_version}.
        :param multiple_write_locations_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#multiple_write_locations_enabled CosmosdbAccount#multiple_write_locations_enabled}.
        :param network_acl_bypass_for_azure_services: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#network_acl_bypass_for_azure_services CosmosdbAccount#network_acl_bypass_for_azure_services}.
        :param network_acl_bypass_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#network_acl_bypass_ids CosmosdbAccount#network_acl_bypass_ids}.
        :param partition_merge_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#partition_merge_enabled CosmosdbAccount#partition_merge_enabled}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#public_network_access_enabled CosmosdbAccount#public_network_access_enabled}.
        :param restore: restore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#restore CosmosdbAccount#restore}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#tags CosmosdbAccount#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#timeouts CosmosdbAccount#timeouts}
        :param virtual_network_rule: virtual_network_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#virtual_network_rule CosmosdbAccount#virtual_network_rule}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085c9339620344e44d06a085f68f0f7b1414f62dba8f9a2e308e32f5ea95320d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CosmosdbAccountConfig(
            consistency_policy=consistency_policy,
            geo_location=geo_location,
            location=location,
            name=name,
            offer_type=offer_type,
            resource_group_name=resource_group_name,
            access_key_metadata_writes_enabled=access_key_metadata_writes_enabled,
            analytical_storage=analytical_storage,
            analytical_storage_enabled=analytical_storage_enabled,
            automatic_failover_enabled=automatic_failover_enabled,
            backup=backup,
            burst_capacity_enabled=burst_capacity_enabled,
            capabilities=capabilities,
            capacity=capacity,
            cors_rule=cors_rule,
            create_mode=create_mode,
            default_identity_type=default_identity_type,
            free_tier_enabled=free_tier_enabled,
            id=id,
            identity=identity,
            ip_range_filter=ip_range_filter,
            is_virtual_network_filter_enabled=is_virtual_network_filter_enabled,
            key_vault_key_id=key_vault_key_id,
            kind=kind,
            local_authentication_disabled=local_authentication_disabled,
            managed_hsm_key_id=managed_hsm_key_id,
            minimal_tls_version=minimal_tls_version,
            mongo_server_version=mongo_server_version,
            multiple_write_locations_enabled=multiple_write_locations_enabled,
            network_acl_bypass_for_azure_services=network_acl_bypass_for_azure_services,
            network_acl_bypass_ids=network_acl_bypass_ids,
            partition_merge_enabled=partition_merge_enabled,
            public_network_access_enabled=public_network_access_enabled,
            restore=restore,
            tags=tags,
            timeouts=timeouts,
            virtual_network_rule=virtual_network_rule,
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
        '''Generates CDKTF code for importing a CosmosdbAccount resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CosmosdbAccount to import.
        :param import_from_id: The id of the existing CosmosdbAccount that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CosmosdbAccount to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd89baba10d5ba119000d8a679240f8f738f6d9e971c04d7aa77682ec0cc16b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAnalyticalStorage")
    def put_analytical_storage(self, *, schema_type: builtins.str) -> None:
        '''
        :param schema_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#schema_type CosmosdbAccount#schema_type}.
        '''
        value = CosmosdbAccountAnalyticalStorage(schema_type=schema_type)

        return typing.cast(None, jsii.invoke(self, "putAnalyticalStorage", [value]))

    @jsii.member(jsii_name="putBackup")
    def put_backup(
        self,
        *,
        type: builtins.str,
        interval_in_minutes: typing.Optional[jsii.Number] = None,
        retention_in_hours: typing.Optional[jsii.Number] = None,
        storage_redundancy: typing.Optional[builtins.str] = None,
        tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#type CosmosdbAccount#type}.
        :param interval_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#interval_in_minutes CosmosdbAccount#interval_in_minutes}.
        :param retention_in_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#retention_in_hours CosmosdbAccount#retention_in_hours}.
        :param storage_redundancy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#storage_redundancy CosmosdbAccount#storage_redundancy}.
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#tier CosmosdbAccount#tier}.
        '''
        value = CosmosdbAccountBackup(
            type=type,
            interval_in_minutes=interval_in_minutes,
            retention_in_hours=retention_in_hours,
            storage_redundancy=storage_redundancy,
            tier=tier,
        )

        return typing.cast(None, jsii.invoke(self, "putBackup", [value]))

    @jsii.member(jsii_name="putCapabilities")
    def put_capabilities(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountCapabilities", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f16af7070edc17b6c874186c7df98e29933a10880d1d6f81c3ebbd78858d5dd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCapabilities", [value]))

    @jsii.member(jsii_name="putCapacity")
    def put_capacity(self, *, total_throughput_limit: jsii.Number) -> None:
        '''
        :param total_throughput_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#total_throughput_limit CosmosdbAccount#total_throughput_limit}.
        '''
        value = CosmosdbAccountCapacity(total_throughput_limit=total_throughput_limit)

        return typing.cast(None, jsii.invoke(self, "putCapacity", [value]))

    @jsii.member(jsii_name="putConsistencyPolicy")
    def put_consistency_policy(
        self,
        *,
        consistency_level: builtins.str,
        max_interval_in_seconds: typing.Optional[jsii.Number] = None,
        max_staleness_prefix: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param consistency_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#consistency_level CosmosdbAccount#consistency_level}.
        :param max_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#max_interval_in_seconds CosmosdbAccount#max_interval_in_seconds}.
        :param max_staleness_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#max_staleness_prefix CosmosdbAccount#max_staleness_prefix}.
        '''
        value = CosmosdbAccountConsistencyPolicy(
            consistency_level=consistency_level,
            max_interval_in_seconds=max_interval_in_seconds,
            max_staleness_prefix=max_staleness_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putConsistencyPolicy", [value]))

    @jsii.member(jsii_name="putCorsRule")
    def put_cors_rule(
        self,
        *,
        allowed_headers: typing.Sequence[builtins.str],
        allowed_methods: typing.Sequence[builtins.str],
        allowed_origins: typing.Sequence[builtins.str],
        exposed_headers: typing.Sequence[builtins.str],
        max_age_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#allowed_headers CosmosdbAccount#allowed_headers}.
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#allowed_methods CosmosdbAccount#allowed_methods}.
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#allowed_origins CosmosdbAccount#allowed_origins}.
        :param exposed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#exposed_headers CosmosdbAccount#exposed_headers}.
        :param max_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#max_age_in_seconds CosmosdbAccount#max_age_in_seconds}.
        '''
        value = CosmosdbAccountCorsRule(
            allowed_headers=allowed_headers,
            allowed_methods=allowed_methods,
            allowed_origins=allowed_origins,
            exposed_headers=exposed_headers,
            max_age_in_seconds=max_age_in_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putCorsRule", [value]))

    @jsii.member(jsii_name="putGeoLocation")
    def put_geo_location(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountGeoLocation", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca0849289cb204bf253c3b4f107578406fb55d63c3984e2a32dbfe4328714d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGeoLocation", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#type CosmosdbAccount#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#identity_ids CosmosdbAccount#identity_ids}.
        '''
        value = CosmosdbAccountIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putRestore")
    def put_restore(
        self,
        *,
        restore_timestamp_in_utc: builtins.str,
        source_cosmosdb_account_id: builtins.str,
        database: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountRestoreDatabase", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gremlin_database: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountRestoreGremlinDatabase", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tables_to_restore: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param restore_timestamp_in_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#restore_timestamp_in_utc CosmosdbAccount#restore_timestamp_in_utc}.
        :param source_cosmosdb_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#source_cosmosdb_account_id CosmosdbAccount#source_cosmosdb_account_id}.
        :param database: database block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#database CosmosdbAccount#database}
        :param gremlin_database: gremlin_database block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#gremlin_database CosmosdbAccount#gremlin_database}
        :param tables_to_restore: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#tables_to_restore CosmosdbAccount#tables_to_restore}.
        '''
        value = CosmosdbAccountRestore(
            restore_timestamp_in_utc=restore_timestamp_in_utc,
            source_cosmosdb_account_id=source_cosmosdb_account_id,
            database=database,
            gremlin_database=gremlin_database,
            tables_to_restore=tables_to_restore,
        )

        return typing.cast(None, jsii.invoke(self, "putRestore", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#create CosmosdbAccount#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#delete CosmosdbAccount#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#read CosmosdbAccount#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#update CosmosdbAccount#update}.
        '''
        value = CosmosdbAccountTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualNetworkRule")
    def put_virtual_network_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountVirtualNetworkRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deeb902d1779b7d0d7ea08b00a55ec11f013ad9baf08db14cb022dfa5f1ebc67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVirtualNetworkRule", [value]))

    @jsii.member(jsii_name="resetAccessKeyMetadataWritesEnabled")
    def reset_access_key_metadata_writes_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKeyMetadataWritesEnabled", []))

    @jsii.member(jsii_name="resetAnalyticalStorage")
    def reset_analytical_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalyticalStorage", []))

    @jsii.member(jsii_name="resetAnalyticalStorageEnabled")
    def reset_analytical_storage_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalyticalStorageEnabled", []))

    @jsii.member(jsii_name="resetAutomaticFailoverEnabled")
    def reset_automatic_failover_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticFailoverEnabled", []))

    @jsii.member(jsii_name="resetBackup")
    def reset_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackup", []))

    @jsii.member(jsii_name="resetBurstCapacityEnabled")
    def reset_burst_capacity_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBurstCapacityEnabled", []))

    @jsii.member(jsii_name="resetCapabilities")
    def reset_capabilities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapabilities", []))

    @jsii.member(jsii_name="resetCapacity")
    def reset_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacity", []))

    @jsii.member(jsii_name="resetCorsRule")
    def reset_cors_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsRule", []))

    @jsii.member(jsii_name="resetCreateMode")
    def reset_create_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateMode", []))

    @jsii.member(jsii_name="resetDefaultIdentityType")
    def reset_default_identity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultIdentityType", []))

    @jsii.member(jsii_name="resetFreeTierEnabled")
    def reset_free_tier_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFreeTierEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetIpRangeFilter")
    def reset_ip_range_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRangeFilter", []))

    @jsii.member(jsii_name="resetIsVirtualNetworkFilterEnabled")
    def reset_is_virtual_network_filter_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsVirtualNetworkFilterEnabled", []))

    @jsii.member(jsii_name="resetKeyVaultKeyId")
    def reset_key_vault_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultKeyId", []))

    @jsii.member(jsii_name="resetKind")
    def reset_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKind", []))

    @jsii.member(jsii_name="resetLocalAuthenticationDisabled")
    def reset_local_authentication_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalAuthenticationDisabled", []))

    @jsii.member(jsii_name="resetManagedHsmKeyId")
    def reset_managed_hsm_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedHsmKeyId", []))

    @jsii.member(jsii_name="resetMinimalTlsVersion")
    def reset_minimal_tls_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimalTlsVersion", []))

    @jsii.member(jsii_name="resetMongoServerVersion")
    def reset_mongo_server_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMongoServerVersion", []))

    @jsii.member(jsii_name="resetMultipleWriteLocationsEnabled")
    def reset_multiple_write_locations_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultipleWriteLocationsEnabled", []))

    @jsii.member(jsii_name="resetNetworkAclBypassForAzureServices")
    def reset_network_acl_bypass_for_azure_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkAclBypassForAzureServices", []))

    @jsii.member(jsii_name="resetNetworkAclBypassIds")
    def reset_network_acl_bypass_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkAclBypassIds", []))

    @jsii.member(jsii_name="resetPartitionMergeEnabled")
    def reset_partition_merge_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionMergeEnabled", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetRestore")
    def reset_restore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestore", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualNetworkRule")
    def reset_virtual_network_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkRule", []))

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
    @jsii.member(jsii_name="analyticalStorage")
    def analytical_storage(self) -> "CosmosdbAccountAnalyticalStorageOutputReference":
        return typing.cast("CosmosdbAccountAnalyticalStorageOutputReference", jsii.get(self, "analyticalStorage"))

    @builtins.property
    @jsii.member(jsii_name="backup")
    def backup(self) -> "CosmosdbAccountBackupOutputReference":
        return typing.cast("CosmosdbAccountBackupOutputReference", jsii.get(self, "backup"))

    @builtins.property
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> "CosmosdbAccountCapabilitiesList":
        return typing.cast("CosmosdbAccountCapabilitiesList", jsii.get(self, "capabilities"))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> "CosmosdbAccountCapacityOutputReference":
        return typing.cast("CosmosdbAccountCapacityOutputReference", jsii.get(self, "capacity"))

    @builtins.property
    @jsii.member(jsii_name="consistencyPolicy")
    def consistency_policy(self) -> "CosmosdbAccountConsistencyPolicyOutputReference":
        return typing.cast("CosmosdbAccountConsistencyPolicyOutputReference", jsii.get(self, "consistencyPolicy"))

    @builtins.property
    @jsii.member(jsii_name="corsRule")
    def cors_rule(self) -> "CosmosdbAccountCorsRuleOutputReference":
        return typing.cast("CosmosdbAccountCorsRuleOutputReference", jsii.get(self, "corsRule"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="geoLocation")
    def geo_location(self) -> "CosmosdbAccountGeoLocationList":
        return typing.cast("CosmosdbAccountGeoLocationList", jsii.get(self, "geoLocation"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "CosmosdbAccountIdentityOutputReference":
        return typing.cast("CosmosdbAccountIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryKey"))

    @builtins.property
    @jsii.member(jsii_name="primaryMongodbConnectionString")
    def primary_mongodb_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryMongodbConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="primaryReadonlyKey")
    def primary_readonly_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryReadonlyKey"))

    @builtins.property
    @jsii.member(jsii_name="primaryReadonlyMongodbConnectionString")
    def primary_readonly_mongodb_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryReadonlyMongodbConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="primaryReadonlySqlConnectionString")
    def primary_readonly_sql_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryReadonlySqlConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="primarySqlConnectionString")
    def primary_sql_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primarySqlConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="readEndpoints")
    def read_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "readEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="restore")
    def restore(self) -> "CosmosdbAccountRestoreOutputReference":
        return typing.cast("CosmosdbAccountRestoreOutputReference", jsii.get(self, "restore"))

    @builtins.property
    @jsii.member(jsii_name="secondaryKey")
    def secondary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryKey"))

    @builtins.property
    @jsii.member(jsii_name="secondaryMongodbConnectionString")
    def secondary_mongodb_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryMongodbConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="secondaryReadonlyKey")
    def secondary_readonly_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryReadonlyKey"))

    @builtins.property
    @jsii.member(jsii_name="secondaryReadonlyMongodbConnectionString")
    def secondary_readonly_mongodb_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryReadonlyMongodbConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="secondaryReadonlySqlConnectionString")
    def secondary_readonly_sql_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryReadonlySqlConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="secondarySqlConnectionString")
    def secondary_sql_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondarySqlConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CosmosdbAccountTimeoutsOutputReference":
        return typing.cast("CosmosdbAccountTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkRule")
    def virtual_network_rule(self) -> "CosmosdbAccountVirtualNetworkRuleList":
        return typing.cast("CosmosdbAccountVirtualNetworkRuleList", jsii.get(self, "virtualNetworkRule"))

    @builtins.property
    @jsii.member(jsii_name="writeEndpoints")
    def write_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "writeEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyMetadataWritesEnabledInput")
    def access_key_metadata_writes_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accessKeyMetadataWritesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="analyticalStorageEnabledInput")
    def analytical_storage_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "analyticalStorageEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="analyticalStorageInput")
    def analytical_storage_input(
        self,
    ) -> typing.Optional["CosmosdbAccountAnalyticalStorage"]:
        return typing.cast(typing.Optional["CosmosdbAccountAnalyticalStorage"], jsii.get(self, "analyticalStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticFailoverEnabledInput")
    def automatic_failover_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automaticFailoverEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(self) -> typing.Optional["CosmosdbAccountBackup"]:
        return typing.cast(typing.Optional["CosmosdbAccountBackup"], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="burstCapacityEnabledInput")
    def burst_capacity_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "burstCapacityEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="capabilitiesInput")
    def capabilities_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountCapabilities"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountCapabilities"]]], jsii.get(self, "capabilitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityInput")
    def capacity_input(self) -> typing.Optional["CosmosdbAccountCapacity"]:
        return typing.cast(typing.Optional["CosmosdbAccountCapacity"], jsii.get(self, "capacityInput"))

    @builtins.property
    @jsii.member(jsii_name="consistencyPolicyInput")
    def consistency_policy_input(
        self,
    ) -> typing.Optional["CosmosdbAccountConsistencyPolicy"]:
        return typing.cast(typing.Optional["CosmosdbAccountConsistencyPolicy"], jsii.get(self, "consistencyPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="corsRuleInput")
    def cors_rule_input(self) -> typing.Optional["CosmosdbAccountCorsRule"]:
        return typing.cast(typing.Optional["CosmosdbAccountCorsRule"], jsii.get(self, "corsRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="createModeInput")
    def create_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createModeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultIdentityTypeInput")
    def default_identity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultIdentityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="freeTierEnabledInput")
    def free_tier_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "freeTierEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="geoLocationInput")
    def geo_location_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountGeoLocation"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountGeoLocation"]]], jsii.get(self, "geoLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["CosmosdbAccountIdentity"]:
        return typing.cast(typing.Optional["CosmosdbAccountIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRangeFilterInput")
    def ip_range_filter_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipRangeFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="isVirtualNetworkFilterEnabledInput")
    def is_virtual_network_filter_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isVirtualNetworkFilterEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyIdInput")
    def key_vault_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="localAuthenticationDisabledInput")
    def local_authentication_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localAuthenticationDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedHsmKeyIdInput")
    def managed_hsm_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedHsmKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="minimalTlsVersionInput")
    def minimal_tls_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimalTlsVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="mongoServerVersionInput")
    def mongo_server_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mongoServerVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="multipleWriteLocationsEnabledInput")
    def multiple_write_locations_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multipleWriteLocationsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkAclBypassForAzureServicesInput")
    def network_acl_bypass_for_azure_services_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "networkAclBypassForAzureServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="networkAclBypassIdsInput")
    def network_acl_bypass_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkAclBypassIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="offerTypeInput")
    def offer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionMergeEnabledInput")
    def partition_merge_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "partitionMergeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreInput")
    def restore_input(self) -> typing.Optional["CosmosdbAccountRestore"]:
        return typing.cast(typing.Optional["CosmosdbAccountRestore"], jsii.get(self, "restoreInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CosmosdbAccountTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CosmosdbAccountTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkRuleInput")
    def virtual_network_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountVirtualNetworkRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountVirtualNetworkRule"]]], jsii.get(self, "virtualNetworkRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyMetadataWritesEnabled")
    def access_key_metadata_writes_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "accessKeyMetadataWritesEnabled"))

    @access_key_metadata_writes_enabled.setter
    def access_key_metadata_writes_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d3b72ea2beb69fa2fc2cc2f7cffa7111cb238cb3a00e5dabcb8360f99000ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyMetadataWritesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="analyticalStorageEnabled")
    def analytical_storage_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "analyticalStorageEnabled"))

    @analytical_storage_enabled.setter
    def analytical_storage_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7402f18d0b5d324f174be6786da548cacb2a7f6a58fc8463763efab007ae62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analyticalStorageEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="automaticFailoverEnabled")
    def automatic_failover_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automaticFailoverEnabled"))

    @automatic_failover_enabled.setter
    def automatic_failover_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c895d2d389dbd3b06b84de3ee3691da7a41989c9e6bbd70cd6e2bf1c45ee2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticFailoverEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="burstCapacityEnabled")
    def burst_capacity_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "burstCapacityEnabled"))

    @burst_capacity_enabled.setter
    def burst_capacity_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a6a15e3495a074afc80fc3277e64d1da4042a96646d9f161deac1c3cf55f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "burstCapacityEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createMode")
    def create_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createMode"))

    @create_mode.setter
    def create_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807b7691fca59dff1bfda7fa67d6fb86c34517f46e381a806c72692619c3ac10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultIdentityType")
    def default_identity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultIdentityType"))

    @default_identity_type.setter
    def default_identity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59bb11319c00cdaff004782ca155acadb3b1b0fda574c8946d7f8ad32fcf71d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultIdentityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="freeTierEnabled")
    def free_tier_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "freeTierEnabled"))

    @free_tier_enabled.setter
    def free_tier_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c0206b625a6c9116a1ea9ad471255efca10e63c1a73a4f6e8ff9ea9df992feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "freeTierEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3771ef220817d3b23c613786087caa41da7eafd377d947166fad3555a7ac1804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipRangeFilter")
    def ip_range_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipRangeFilter"))

    @ip_range_filter.setter
    def ip_range_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c910fbf0cffab83a6c539a5bb2a949ff6df37d04f2756cad61061692bd8972e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipRangeFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isVirtualNetworkFilterEnabled")
    def is_virtual_network_filter_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isVirtualNetworkFilterEnabled"))

    @is_virtual_network_filter_enabled.setter
    def is_virtual_network_filter_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c0261feb8b53f531f74d42c7e7348c8ec3c794990b857d17b9f4d7bec1bb15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isVirtualNetworkFilterEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyId")
    def key_vault_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultKeyId"))

    @key_vault_key_id.setter
    def key_vault_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb1846afefc15a52b2a21716b13b90f43fb0a03111727a48b92a430c5ccc590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5dd761a6b2c4f4abe9e331918b37408c9bb5a720028c34d10cc61419a96b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localAuthenticationDisabled")
    def local_authentication_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "localAuthenticationDisabled"))

    @local_authentication_disabled.setter
    def local_authentication_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60233434a3b02dd06a69838f2a403e0103a71ab891b7c86d25ee65375b1ffcee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAuthenticationDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427ce2e19e14cdd015c52ad87ba816994702884f348ebaf66cfe8ce403b90742)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedHsmKeyId")
    def managed_hsm_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedHsmKeyId"))

    @managed_hsm_key_id.setter
    def managed_hsm_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888c7a6cbcb782fa35c4c0e635f2bd73be176c5a517bc7750047612e55cd42de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedHsmKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimalTlsVersion")
    def minimal_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimalTlsVersion"))

    @minimal_tls_version.setter
    def minimal_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb73cdf0a4fc3f45b13ecfb7816cd4d8a1c5cc606cef432513ecb8e3e0567b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimalTlsVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mongoServerVersion")
    def mongo_server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mongoServerVersion"))

    @mongo_server_version.setter
    def mongo_server_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc802f8a9ad40c5293b99642c3d25b988a0e0bd4ce12efd466f193915b72257a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mongoServerVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multipleWriteLocationsEnabled")
    def multiple_write_locations_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multipleWriteLocationsEnabled"))

    @multiple_write_locations_enabled.setter
    def multiple_write_locations_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b640e789f8d6eedb6c32983de6aaa2606443f871fd550b869043b7066aecb94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multipleWriteLocationsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4af4ac1bf4d073eabedc1801616d5ee30545a22655c0f837e41ef3b45a99bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkAclBypassForAzureServices")
    def network_acl_bypass_for_azure_services(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "networkAclBypassForAzureServices"))

    @network_acl_bypass_for_azure_services.setter
    def network_acl_bypass_for_azure_services(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553951c0bf2b474a4d139c3ab9a8de46e225f1d3bfe4839334c7d1318162abc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAclBypassForAzureServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkAclBypassIds")
    def network_acl_bypass_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkAclBypassIds"))

    @network_acl_bypass_ids.setter
    def network_acl_bypass_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d48e2c1f663da620fee0f5f11222da82e275fc8745b49d2ab72fbd4ccdfc596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAclBypassIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="offerType")
    def offer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offerType"))

    @offer_type.setter
    def offer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6960bdb33a0c9a21fd99dc288733bf1326184a0702bd0c523d628e194604f61f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionMergeEnabled")
    def partition_merge_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "partitionMergeEnabled"))

    @partition_merge_enabled.setter
    def partition_merge_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee3a1d00770855c718f12b8c51e0f664ee0600e8ee7e3cb529148f23b080ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionMergeEnabled", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__39543ce2b7087c596c0c5b9d87dce1c25f327086b368f746b6dac81758ca2cc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa552a2732476860e6d429f04292139a11d21319f9b8a5a53b3689799f00f2f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd44838ebbd99adba8607aa325f9857d2c562da891351ef08f6101ce4fde14a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountAnalyticalStorage",
    jsii_struct_bases=[],
    name_mapping={"schema_type": "schemaType"},
)
class CosmosdbAccountAnalyticalStorage:
    def __init__(self, *, schema_type: builtins.str) -> None:
        '''
        :param schema_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#schema_type CosmosdbAccount#schema_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4424a209bbc91122bcdd6689e7c49269cbf85b99043b3ff22bdefb80d68343dd)
            check_type(argname="argument schema_type", value=schema_type, expected_type=type_hints["schema_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema_type": schema_type,
        }

    @builtins.property
    def schema_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#schema_type CosmosdbAccount#schema_type}.'''
        result = self._values.get("schema_type")
        assert result is not None, "Required property 'schema_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountAnalyticalStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountAnalyticalStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountAnalyticalStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e876cb9f87603b2eae4cc53337966339d862dfc1cab745a814f733141ea4eea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="schemaTypeInput")
    def schema_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaType")
    def schema_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaType"))

    @schema_type.setter
    def schema_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21caa1e215458f99a652e4e422949cc25485f69d81030198cf46fc98a469ae01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbAccountAnalyticalStorage]:
        return typing.cast(typing.Optional[CosmosdbAccountAnalyticalStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CosmosdbAccountAnalyticalStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bdc6b2ada8577369ff0105bbd5073b21aa4ef77dc1aa064ee87bd96d1cde1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountBackup",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "interval_in_minutes": "intervalInMinutes",
        "retention_in_hours": "retentionInHours",
        "storage_redundancy": "storageRedundancy",
        "tier": "tier",
    },
)
class CosmosdbAccountBackup:
    def __init__(
        self,
        *,
        type: builtins.str,
        interval_in_minutes: typing.Optional[jsii.Number] = None,
        retention_in_hours: typing.Optional[jsii.Number] = None,
        storage_redundancy: typing.Optional[builtins.str] = None,
        tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#type CosmosdbAccount#type}.
        :param interval_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#interval_in_minutes CosmosdbAccount#interval_in_minutes}.
        :param retention_in_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#retention_in_hours CosmosdbAccount#retention_in_hours}.
        :param storage_redundancy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#storage_redundancy CosmosdbAccount#storage_redundancy}.
        :param tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#tier CosmosdbAccount#tier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b27f8b74c561ea315a42e1a08ef708c7c47bcd0f5925836c95a443b1953a4e)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument interval_in_minutes", value=interval_in_minutes, expected_type=type_hints["interval_in_minutes"])
            check_type(argname="argument retention_in_hours", value=retention_in_hours, expected_type=type_hints["retention_in_hours"])
            check_type(argname="argument storage_redundancy", value=storage_redundancy, expected_type=type_hints["storage_redundancy"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if interval_in_minutes is not None:
            self._values["interval_in_minutes"] = interval_in_minutes
        if retention_in_hours is not None:
            self._values["retention_in_hours"] = retention_in_hours
        if storage_redundancy is not None:
            self._values["storage_redundancy"] = storage_redundancy
        if tier is not None:
            self._values["tier"] = tier

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#type CosmosdbAccount#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def interval_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#interval_in_minutes CosmosdbAccount#interval_in_minutes}.'''
        result = self._values.get("interval_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retention_in_hours(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#retention_in_hours CosmosdbAccount#retention_in_hours}.'''
        result = self._values.get("retention_in_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_redundancy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#storage_redundancy CosmosdbAccount#storage_redundancy}.'''
        result = self._values.get("storage_redundancy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#tier CosmosdbAccount#tier}.'''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__472279438cfd3c0165d67c4011da04cfdd08bacb352f348de8cf8945a56e39c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIntervalInMinutes")
    def reset_interval_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalInMinutes", []))

    @jsii.member(jsii_name="resetRetentionInHours")
    def reset_retention_in_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionInHours", []))

    @jsii.member(jsii_name="resetStorageRedundancy")
    def reset_storage_redundancy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageRedundancy", []))

    @jsii.member(jsii_name="resetTier")
    def reset_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTier", []))

    @builtins.property
    @jsii.member(jsii_name="intervalInMinutesInput")
    def interval_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionInHoursInput")
    def retention_in_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionInHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="storageRedundancyInput")
    def storage_redundancy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageRedundancyInput"))

    @builtins.property
    @jsii.member(jsii_name="tierInput")
    def tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInMinutes")
    def interval_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalInMinutes"))

    @interval_in_minutes.setter
    def interval_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f74e653bf12aef76fa86be341a16489a1a16ea4299ba77e485d4d2a6d35a6fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionInHours")
    def retention_in_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionInHours"))

    @retention_in_hours.setter
    def retention_in_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e563f193bce7a3c1c75182352fc3a537a868b2e49256d77812bc7aa9c1489e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionInHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageRedundancy")
    def storage_redundancy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageRedundancy"))

    @storage_redundancy.setter
    def storage_redundancy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39de1884ce786abb7143a691d9efd313b04afe169fa9c9895e31e746a5d174ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageRedundancy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tier"))

    @tier.setter
    def tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45df28ca6500201e6eb8c694a30e3f8e351d28706d2faf2ce8cdc798e5819e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d48bbab2d21571902797a14d7b3747b065822f9ec5c8f6db192fb91cadfb95d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbAccountBackup]:
        return typing.cast(typing.Optional[CosmosdbAccountBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CosmosdbAccountBackup]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d109304de2f04f69323566ac4a306c8282d5b66784cf8b01a993a03aeae06f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountCapabilities",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class CosmosdbAccountCapabilities:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#name CosmosdbAccount#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e66f8fcca563b812014289638b7bc12fda6a16e5296f4c59f4c439bd033e2b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#name CosmosdbAccount#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountCapabilities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountCapabilitiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountCapabilitiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2cdb9369938ca78420243a440ab5d452254e1af476277d1c366b625903b76f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CosmosdbAccountCapabilitiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175d6bda5686978d482bcc8b5f35e0f84b88a2a357cd0f154de69290afe97d98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbAccountCapabilitiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__371de3fdff355ce3c12b6784b3202c180af78cb86294e884afc5e23d25f803fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b1e9dcb8a627c79213996a67dde33cb0fddd9154f67d5f7b349da7b03a5d65a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abcbf5fed54d9f584d514027dbfe8487b2e8ae5e18a3ee9f04dae35b1e888ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountCapabilities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountCapabilities]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountCapabilities]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ddbb135414751d18452466036b0b70e61bd58c861a9ceb809c19b823d562c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbAccountCapabilitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountCapabilitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e56a5b2c56ddc32b0624bc774cbd354260a7785646f02b749510754efd9dd8f5)
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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7bf4968c5e502b71d4391df3aae48181cb93b8d4e92e92265c829adcb3ad87b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountCapabilities]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountCapabilities]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountCapabilities]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2976e3361ec821e1d9beb5eba7c35ab6b9eba229608a3c24508462d1f604df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountCapacity",
    jsii_struct_bases=[],
    name_mapping={"total_throughput_limit": "totalThroughputLimit"},
)
class CosmosdbAccountCapacity:
    def __init__(self, *, total_throughput_limit: jsii.Number) -> None:
        '''
        :param total_throughput_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#total_throughput_limit CosmosdbAccount#total_throughput_limit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__926aef6602376cd0db56e1500698492470c73800b02321ced39e244f83f4a1e3)
            check_type(argname="argument total_throughput_limit", value=total_throughput_limit, expected_type=type_hints["total_throughput_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "total_throughput_limit": total_throughput_limit,
        }

    @builtins.property
    def total_throughput_limit(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#total_throughput_limit CosmosdbAccount#total_throughput_limit}.'''
        result = self._values.get("total_throughput_limit")
        assert result is not None, "Required property 'total_throughput_limit' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountCapacity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountCapacityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountCapacityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f2e73dd1cb8ddb8d28366dc6128a541b15d73f26ed8debe443d62826393fe86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="totalThroughputLimitInput")
    def total_throughput_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "totalThroughputLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="totalThroughputLimit")
    def total_throughput_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalThroughputLimit"))

    @total_throughput_limit.setter
    def total_throughput_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d01c3182c78b9dfdf31f134cdbeb46bf02af5f61921d5092af6092729f5c36fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalThroughputLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbAccountCapacity]:
        return typing.cast(typing.Optional[CosmosdbAccountCapacity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CosmosdbAccountCapacity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19eb36c3c5eb9fa85caff9a2cad80fd7c29effaa04875235fe0f68a689837f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "consistency_policy": "consistencyPolicy",
        "geo_location": "geoLocation",
        "location": "location",
        "name": "name",
        "offer_type": "offerType",
        "resource_group_name": "resourceGroupName",
        "access_key_metadata_writes_enabled": "accessKeyMetadataWritesEnabled",
        "analytical_storage": "analyticalStorage",
        "analytical_storage_enabled": "analyticalStorageEnabled",
        "automatic_failover_enabled": "automaticFailoverEnabled",
        "backup": "backup",
        "burst_capacity_enabled": "burstCapacityEnabled",
        "capabilities": "capabilities",
        "capacity": "capacity",
        "cors_rule": "corsRule",
        "create_mode": "createMode",
        "default_identity_type": "defaultIdentityType",
        "free_tier_enabled": "freeTierEnabled",
        "id": "id",
        "identity": "identity",
        "ip_range_filter": "ipRangeFilter",
        "is_virtual_network_filter_enabled": "isVirtualNetworkFilterEnabled",
        "key_vault_key_id": "keyVaultKeyId",
        "kind": "kind",
        "local_authentication_disabled": "localAuthenticationDisabled",
        "managed_hsm_key_id": "managedHsmKeyId",
        "minimal_tls_version": "minimalTlsVersion",
        "mongo_server_version": "mongoServerVersion",
        "multiple_write_locations_enabled": "multipleWriteLocationsEnabled",
        "network_acl_bypass_for_azure_services": "networkAclBypassForAzureServices",
        "network_acl_bypass_ids": "networkAclBypassIds",
        "partition_merge_enabled": "partitionMergeEnabled",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "restore": "restore",
        "tags": "tags",
        "timeouts": "timeouts",
        "virtual_network_rule": "virtualNetworkRule",
    },
)
class CosmosdbAccountConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        consistency_policy: typing.Union["CosmosdbAccountConsistencyPolicy", typing.Dict[builtins.str, typing.Any]],
        geo_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountGeoLocation", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        offer_type: builtins.str,
        resource_group_name: builtins.str,
        access_key_metadata_writes_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        analytical_storage: typing.Optional[typing.Union[CosmosdbAccountAnalyticalStorage, typing.Dict[builtins.str, typing.Any]]] = None,
        analytical_storage_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backup: typing.Optional[typing.Union[CosmosdbAccountBackup, typing.Dict[builtins.str, typing.Any]]] = None,
        burst_capacity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        capabilities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountCapabilities, typing.Dict[builtins.str, typing.Any]]]]] = None,
        capacity: typing.Optional[typing.Union[CosmosdbAccountCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
        cors_rule: typing.Optional[typing.Union["CosmosdbAccountCorsRule", typing.Dict[builtins.str, typing.Any]]] = None,
        create_mode: typing.Optional[builtins.str] = None,
        default_identity_type: typing.Optional[builtins.str] = None,
        free_tier_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["CosmosdbAccountIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        ip_range_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_virtual_network_filter_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_vault_key_id: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        local_authentication_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        managed_hsm_key_id: typing.Optional[builtins.str] = None,
        minimal_tls_version: typing.Optional[builtins.str] = None,
        mongo_server_version: typing.Optional[builtins.str] = None,
        multiple_write_locations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_acl_bypass_for_azure_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        network_acl_bypass_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        partition_merge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restore: typing.Optional[typing.Union["CosmosdbAccountRestore", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CosmosdbAccountTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountVirtualNetworkRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param consistency_policy: consistency_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#consistency_policy CosmosdbAccount#consistency_policy}
        :param geo_location: geo_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#geo_location CosmosdbAccount#geo_location}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#location CosmosdbAccount#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#name CosmosdbAccount#name}.
        :param offer_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#offer_type CosmosdbAccount#offer_type}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#resource_group_name CosmosdbAccount#resource_group_name}.
        :param access_key_metadata_writes_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#access_key_metadata_writes_enabled CosmosdbAccount#access_key_metadata_writes_enabled}.
        :param analytical_storage: analytical_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#analytical_storage CosmosdbAccount#analytical_storage}
        :param analytical_storage_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#analytical_storage_enabled CosmosdbAccount#analytical_storage_enabled}.
        :param automatic_failover_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#automatic_failover_enabled CosmosdbAccount#automatic_failover_enabled}.
        :param backup: backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#backup CosmosdbAccount#backup}
        :param burst_capacity_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#burst_capacity_enabled CosmosdbAccount#burst_capacity_enabled}.
        :param capabilities: capabilities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#capabilities CosmosdbAccount#capabilities}
        :param capacity: capacity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#capacity CosmosdbAccount#capacity}
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#cors_rule CosmosdbAccount#cors_rule}
        :param create_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#create_mode CosmosdbAccount#create_mode}.
        :param default_identity_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#default_identity_type CosmosdbAccount#default_identity_type}.
        :param free_tier_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#free_tier_enabled CosmosdbAccount#free_tier_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#id CosmosdbAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#identity CosmosdbAccount#identity}
        :param ip_range_filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#ip_range_filter CosmosdbAccount#ip_range_filter}.
        :param is_virtual_network_filter_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#is_virtual_network_filter_enabled CosmosdbAccount#is_virtual_network_filter_enabled}.
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#key_vault_key_id CosmosdbAccount#key_vault_key_id}.
        :param kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#kind CosmosdbAccount#kind}.
        :param local_authentication_disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#local_authentication_disabled CosmosdbAccount#local_authentication_disabled}.
        :param managed_hsm_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#managed_hsm_key_id CosmosdbAccount#managed_hsm_key_id}.
        :param minimal_tls_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#minimal_tls_version CosmosdbAccount#minimal_tls_version}.
        :param mongo_server_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#mongo_server_version CosmosdbAccount#mongo_server_version}.
        :param multiple_write_locations_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#multiple_write_locations_enabled CosmosdbAccount#multiple_write_locations_enabled}.
        :param network_acl_bypass_for_azure_services: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#network_acl_bypass_for_azure_services CosmosdbAccount#network_acl_bypass_for_azure_services}.
        :param network_acl_bypass_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#network_acl_bypass_ids CosmosdbAccount#network_acl_bypass_ids}.
        :param partition_merge_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#partition_merge_enabled CosmosdbAccount#partition_merge_enabled}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#public_network_access_enabled CosmosdbAccount#public_network_access_enabled}.
        :param restore: restore block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#restore CosmosdbAccount#restore}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#tags CosmosdbAccount#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#timeouts CosmosdbAccount#timeouts}
        :param virtual_network_rule: virtual_network_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#virtual_network_rule CosmosdbAccount#virtual_network_rule}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(consistency_policy, dict):
            consistency_policy = CosmosdbAccountConsistencyPolicy(**consistency_policy)
        if isinstance(analytical_storage, dict):
            analytical_storage = CosmosdbAccountAnalyticalStorage(**analytical_storage)
        if isinstance(backup, dict):
            backup = CosmosdbAccountBackup(**backup)
        if isinstance(capacity, dict):
            capacity = CosmosdbAccountCapacity(**capacity)
        if isinstance(cors_rule, dict):
            cors_rule = CosmosdbAccountCorsRule(**cors_rule)
        if isinstance(identity, dict):
            identity = CosmosdbAccountIdentity(**identity)
        if isinstance(restore, dict):
            restore = CosmosdbAccountRestore(**restore)
        if isinstance(timeouts, dict):
            timeouts = CosmosdbAccountTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e055a1f70fcd95fb3bdf526c9e20260df99edb887409a1245f6e1fbaf4da7f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument consistency_policy", value=consistency_policy, expected_type=type_hints["consistency_policy"])
            check_type(argname="argument geo_location", value=geo_location, expected_type=type_hints["geo_location"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument offer_type", value=offer_type, expected_type=type_hints["offer_type"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument access_key_metadata_writes_enabled", value=access_key_metadata_writes_enabled, expected_type=type_hints["access_key_metadata_writes_enabled"])
            check_type(argname="argument analytical_storage", value=analytical_storage, expected_type=type_hints["analytical_storage"])
            check_type(argname="argument analytical_storage_enabled", value=analytical_storage_enabled, expected_type=type_hints["analytical_storage_enabled"])
            check_type(argname="argument automatic_failover_enabled", value=automatic_failover_enabled, expected_type=type_hints["automatic_failover_enabled"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument burst_capacity_enabled", value=burst_capacity_enabled, expected_type=type_hints["burst_capacity_enabled"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument cors_rule", value=cors_rule, expected_type=type_hints["cors_rule"])
            check_type(argname="argument create_mode", value=create_mode, expected_type=type_hints["create_mode"])
            check_type(argname="argument default_identity_type", value=default_identity_type, expected_type=type_hints["default_identity_type"])
            check_type(argname="argument free_tier_enabled", value=free_tier_enabled, expected_type=type_hints["free_tier_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument ip_range_filter", value=ip_range_filter, expected_type=type_hints["ip_range_filter"])
            check_type(argname="argument is_virtual_network_filter_enabled", value=is_virtual_network_filter_enabled, expected_type=type_hints["is_virtual_network_filter_enabled"])
            check_type(argname="argument key_vault_key_id", value=key_vault_key_id, expected_type=type_hints["key_vault_key_id"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument local_authentication_disabled", value=local_authentication_disabled, expected_type=type_hints["local_authentication_disabled"])
            check_type(argname="argument managed_hsm_key_id", value=managed_hsm_key_id, expected_type=type_hints["managed_hsm_key_id"])
            check_type(argname="argument minimal_tls_version", value=minimal_tls_version, expected_type=type_hints["minimal_tls_version"])
            check_type(argname="argument mongo_server_version", value=mongo_server_version, expected_type=type_hints["mongo_server_version"])
            check_type(argname="argument multiple_write_locations_enabled", value=multiple_write_locations_enabled, expected_type=type_hints["multiple_write_locations_enabled"])
            check_type(argname="argument network_acl_bypass_for_azure_services", value=network_acl_bypass_for_azure_services, expected_type=type_hints["network_acl_bypass_for_azure_services"])
            check_type(argname="argument network_acl_bypass_ids", value=network_acl_bypass_ids, expected_type=type_hints["network_acl_bypass_ids"])
            check_type(argname="argument partition_merge_enabled", value=partition_merge_enabled, expected_type=type_hints["partition_merge_enabled"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument restore", value=restore, expected_type=type_hints["restore"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_network_rule", value=virtual_network_rule, expected_type=type_hints["virtual_network_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consistency_policy": consistency_policy,
            "geo_location": geo_location,
            "location": location,
            "name": name,
            "offer_type": offer_type,
            "resource_group_name": resource_group_name,
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
        if access_key_metadata_writes_enabled is not None:
            self._values["access_key_metadata_writes_enabled"] = access_key_metadata_writes_enabled
        if analytical_storage is not None:
            self._values["analytical_storage"] = analytical_storage
        if analytical_storage_enabled is not None:
            self._values["analytical_storage_enabled"] = analytical_storage_enabled
        if automatic_failover_enabled is not None:
            self._values["automatic_failover_enabled"] = automatic_failover_enabled
        if backup is not None:
            self._values["backup"] = backup
        if burst_capacity_enabled is not None:
            self._values["burst_capacity_enabled"] = burst_capacity_enabled
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if capacity is not None:
            self._values["capacity"] = capacity
        if cors_rule is not None:
            self._values["cors_rule"] = cors_rule
        if create_mode is not None:
            self._values["create_mode"] = create_mode
        if default_identity_type is not None:
            self._values["default_identity_type"] = default_identity_type
        if free_tier_enabled is not None:
            self._values["free_tier_enabled"] = free_tier_enabled
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if ip_range_filter is not None:
            self._values["ip_range_filter"] = ip_range_filter
        if is_virtual_network_filter_enabled is not None:
            self._values["is_virtual_network_filter_enabled"] = is_virtual_network_filter_enabled
        if key_vault_key_id is not None:
            self._values["key_vault_key_id"] = key_vault_key_id
        if kind is not None:
            self._values["kind"] = kind
        if local_authentication_disabled is not None:
            self._values["local_authentication_disabled"] = local_authentication_disabled
        if managed_hsm_key_id is not None:
            self._values["managed_hsm_key_id"] = managed_hsm_key_id
        if minimal_tls_version is not None:
            self._values["minimal_tls_version"] = minimal_tls_version
        if mongo_server_version is not None:
            self._values["mongo_server_version"] = mongo_server_version
        if multiple_write_locations_enabled is not None:
            self._values["multiple_write_locations_enabled"] = multiple_write_locations_enabled
        if network_acl_bypass_for_azure_services is not None:
            self._values["network_acl_bypass_for_azure_services"] = network_acl_bypass_for_azure_services
        if network_acl_bypass_ids is not None:
            self._values["network_acl_bypass_ids"] = network_acl_bypass_ids
        if partition_merge_enabled is not None:
            self._values["partition_merge_enabled"] = partition_merge_enabled
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if restore is not None:
            self._values["restore"] = restore
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_network_rule is not None:
            self._values["virtual_network_rule"] = virtual_network_rule

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
    def consistency_policy(self) -> "CosmosdbAccountConsistencyPolicy":
        '''consistency_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#consistency_policy CosmosdbAccount#consistency_policy}
        '''
        result = self._values.get("consistency_policy")
        assert result is not None, "Required property 'consistency_policy' is missing"
        return typing.cast("CosmosdbAccountConsistencyPolicy", result)

    @builtins.property
    def geo_location(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountGeoLocation"]]:
        '''geo_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#geo_location CosmosdbAccount#geo_location}
        '''
        result = self._values.get("geo_location")
        assert result is not None, "Required property 'geo_location' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountGeoLocation"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#location CosmosdbAccount#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#name CosmosdbAccount#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def offer_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#offer_type CosmosdbAccount#offer_type}.'''
        result = self._values.get("offer_type")
        assert result is not None, "Required property 'offer_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#resource_group_name CosmosdbAccount#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key_metadata_writes_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#access_key_metadata_writes_enabled CosmosdbAccount#access_key_metadata_writes_enabled}.'''
        result = self._values.get("access_key_metadata_writes_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def analytical_storage(self) -> typing.Optional[CosmosdbAccountAnalyticalStorage]:
        '''analytical_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#analytical_storage CosmosdbAccount#analytical_storage}
        '''
        result = self._values.get("analytical_storage")
        return typing.cast(typing.Optional[CosmosdbAccountAnalyticalStorage], result)

    @builtins.property
    def analytical_storage_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#analytical_storage_enabled CosmosdbAccount#analytical_storage_enabled}.'''
        result = self._values.get("analytical_storage_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def automatic_failover_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#automatic_failover_enabled CosmosdbAccount#automatic_failover_enabled}.'''
        result = self._values.get("automatic_failover_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def backup(self) -> typing.Optional[CosmosdbAccountBackup]:
        '''backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#backup CosmosdbAccount#backup}
        '''
        result = self._values.get("backup")
        return typing.cast(typing.Optional[CosmosdbAccountBackup], result)

    @builtins.property
    def burst_capacity_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#burst_capacity_enabled CosmosdbAccount#burst_capacity_enabled}.'''
        result = self._values.get("burst_capacity_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def capabilities(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountCapabilities]]]:
        '''capabilities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#capabilities CosmosdbAccount#capabilities}
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountCapabilities]]], result)

    @builtins.property
    def capacity(self) -> typing.Optional[CosmosdbAccountCapacity]:
        '''capacity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#capacity CosmosdbAccount#capacity}
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[CosmosdbAccountCapacity], result)

    @builtins.property
    def cors_rule(self) -> typing.Optional["CosmosdbAccountCorsRule"]:
        '''cors_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#cors_rule CosmosdbAccount#cors_rule}
        '''
        result = self._values.get("cors_rule")
        return typing.cast(typing.Optional["CosmosdbAccountCorsRule"], result)

    @builtins.property
    def create_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#create_mode CosmosdbAccount#create_mode}.'''
        result = self._values.get("create_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_identity_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#default_identity_type CosmosdbAccount#default_identity_type}.'''
        result = self._values.get("default_identity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def free_tier_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#free_tier_enabled CosmosdbAccount#free_tier_enabled}.'''
        result = self._values.get("free_tier_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#id CosmosdbAccount#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["CosmosdbAccountIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#identity CosmosdbAccount#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["CosmosdbAccountIdentity"], result)

    @builtins.property
    def ip_range_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#ip_range_filter CosmosdbAccount#ip_range_filter}.'''
        result = self._values.get("ip_range_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def is_virtual_network_filter_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#is_virtual_network_filter_enabled CosmosdbAccount#is_virtual_network_filter_enabled}.'''
        result = self._values.get("is_virtual_network_filter_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_vault_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#key_vault_key_id CosmosdbAccount#key_vault_key_id}.'''
        result = self._values.get("key_vault_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#kind CosmosdbAccount#kind}.'''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_authentication_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#local_authentication_disabled CosmosdbAccount#local_authentication_disabled}.'''
        result = self._values.get("local_authentication_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def managed_hsm_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#managed_hsm_key_id CosmosdbAccount#managed_hsm_key_id}.'''
        result = self._values.get("managed_hsm_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimal_tls_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#minimal_tls_version CosmosdbAccount#minimal_tls_version}.'''
        result = self._values.get("minimal_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mongo_server_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#mongo_server_version CosmosdbAccount#mongo_server_version}.'''
        result = self._values.get("mongo_server_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multiple_write_locations_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#multiple_write_locations_enabled CosmosdbAccount#multiple_write_locations_enabled}.'''
        result = self._values.get("multiple_write_locations_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network_acl_bypass_for_azure_services(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#network_acl_bypass_for_azure_services CosmosdbAccount#network_acl_bypass_for_azure_services}.'''
        result = self._values.get("network_acl_bypass_for_azure_services")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def network_acl_bypass_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#network_acl_bypass_ids CosmosdbAccount#network_acl_bypass_ids}.'''
        result = self._values.get("network_acl_bypass_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def partition_merge_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#partition_merge_enabled CosmosdbAccount#partition_merge_enabled}.'''
        result = self._values.get("partition_merge_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#public_network_access_enabled CosmosdbAccount#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restore(self) -> typing.Optional["CosmosdbAccountRestore"]:
        '''restore block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#restore CosmosdbAccount#restore}
        '''
        result = self._values.get("restore")
        return typing.cast(typing.Optional["CosmosdbAccountRestore"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#tags CosmosdbAccount#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CosmosdbAccountTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#timeouts CosmosdbAccount#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CosmosdbAccountTimeouts"], result)

    @builtins.property
    def virtual_network_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountVirtualNetworkRule"]]]:
        '''virtual_network_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#virtual_network_rule CosmosdbAccount#virtual_network_rule}
        '''
        result = self._values.get("virtual_network_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountVirtualNetworkRule"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountConsistencyPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "consistency_level": "consistencyLevel",
        "max_interval_in_seconds": "maxIntervalInSeconds",
        "max_staleness_prefix": "maxStalenessPrefix",
    },
)
class CosmosdbAccountConsistencyPolicy:
    def __init__(
        self,
        *,
        consistency_level: builtins.str,
        max_interval_in_seconds: typing.Optional[jsii.Number] = None,
        max_staleness_prefix: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param consistency_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#consistency_level CosmosdbAccount#consistency_level}.
        :param max_interval_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#max_interval_in_seconds CosmosdbAccount#max_interval_in_seconds}.
        :param max_staleness_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#max_staleness_prefix CosmosdbAccount#max_staleness_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216db6b25eefb34604ee28a3f3161bbc5a4474e1badcf80773c79cb515a0910f)
            check_type(argname="argument consistency_level", value=consistency_level, expected_type=type_hints["consistency_level"])
            check_type(argname="argument max_interval_in_seconds", value=max_interval_in_seconds, expected_type=type_hints["max_interval_in_seconds"])
            check_type(argname="argument max_staleness_prefix", value=max_staleness_prefix, expected_type=type_hints["max_staleness_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consistency_level": consistency_level,
        }
        if max_interval_in_seconds is not None:
            self._values["max_interval_in_seconds"] = max_interval_in_seconds
        if max_staleness_prefix is not None:
            self._values["max_staleness_prefix"] = max_staleness_prefix

    @builtins.property
    def consistency_level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#consistency_level CosmosdbAccount#consistency_level}.'''
        result = self._values.get("consistency_level")
        assert result is not None, "Required property 'consistency_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_interval_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#max_interval_in_seconds CosmosdbAccount#max_interval_in_seconds}.'''
        result = self._values.get("max_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_staleness_prefix(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#max_staleness_prefix CosmosdbAccount#max_staleness_prefix}.'''
        result = self._values.get("max_staleness_prefix")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountConsistencyPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountConsistencyPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountConsistencyPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55bdc20e15bdfea07454c3f79d2cd29b9c321bc72d19218e56f92c3a6d5bc9f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxIntervalInSeconds")
    def reset_max_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIntervalInSeconds", []))

    @jsii.member(jsii_name="resetMaxStalenessPrefix")
    def reset_max_staleness_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxStalenessPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="consistencyLevelInput")
    def consistency_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consistencyLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIntervalInSecondsInput")
    def max_interval_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxStalenessPrefixInput")
    def max_staleness_prefix_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxStalenessPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="consistencyLevel")
    def consistency_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consistencyLevel"))

    @consistency_level.setter
    def consistency_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff3097b4f79ca942dbdedb6a8748203bfb94bc6b34a01f3225c82326c352e9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consistencyLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxIntervalInSeconds")
    def max_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIntervalInSeconds"))

    @max_interval_in_seconds.setter
    def max_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8f0f0507908d3020e20f099a877864b9606dec866ce703191e698576350498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxStalenessPrefix")
    def max_staleness_prefix(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxStalenessPrefix"))

    @max_staleness_prefix.setter
    def max_staleness_prefix(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2817e238fe0eab435e6d8c540b0044db970e651438c29180ab189ffec8cd384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxStalenessPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbAccountConsistencyPolicy]:
        return typing.cast(typing.Optional[CosmosdbAccountConsistencyPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CosmosdbAccountConsistencyPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491aee0f35a8a65fa920535836bbe1c40c0c3e405bd3096975ef630ed0d7c23b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountCorsRule",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_headers": "allowedHeaders",
        "allowed_methods": "allowedMethods",
        "allowed_origins": "allowedOrigins",
        "exposed_headers": "exposedHeaders",
        "max_age_in_seconds": "maxAgeInSeconds",
    },
)
class CosmosdbAccountCorsRule:
    def __init__(
        self,
        *,
        allowed_headers: typing.Sequence[builtins.str],
        allowed_methods: typing.Sequence[builtins.str],
        allowed_origins: typing.Sequence[builtins.str],
        exposed_headers: typing.Sequence[builtins.str],
        max_age_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#allowed_headers CosmosdbAccount#allowed_headers}.
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#allowed_methods CosmosdbAccount#allowed_methods}.
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#allowed_origins CosmosdbAccount#allowed_origins}.
        :param exposed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#exposed_headers CosmosdbAccount#exposed_headers}.
        :param max_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#max_age_in_seconds CosmosdbAccount#max_age_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56f5e2125a799ef0f9c2f66ccca11d2c4ba1d5737501bfdd19587cad1f2160d2)
            check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument exposed_headers", value=exposed_headers, expected_type=type_hints["exposed_headers"])
            check_type(argname="argument max_age_in_seconds", value=max_age_in_seconds, expected_type=type_hints["max_age_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_headers": allowed_headers,
            "allowed_methods": allowed_methods,
            "allowed_origins": allowed_origins,
            "exposed_headers": exposed_headers,
        }
        if max_age_in_seconds is not None:
            self._values["max_age_in_seconds"] = max_age_in_seconds

    @builtins.property
    def allowed_headers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#allowed_headers CosmosdbAccount#allowed_headers}.'''
        result = self._values.get("allowed_headers")
        assert result is not None, "Required property 'allowed_headers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#allowed_methods CosmosdbAccount#allowed_methods}.'''
        result = self._values.get("allowed_methods")
        assert result is not None, "Required property 'allowed_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_origins(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#allowed_origins CosmosdbAccount#allowed_origins}.'''
        result = self._values.get("allowed_origins")
        assert result is not None, "Required property 'allowed_origins' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def exposed_headers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#exposed_headers CosmosdbAccount#exposed_headers}.'''
        result = self._values.get("exposed_headers")
        assert result is not None, "Required property 'exposed_headers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def max_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#max_age_in_seconds CosmosdbAccount#max_age_in_seconds}.'''
        result = self._values.get("max_age_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountCorsRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountCorsRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountCorsRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86ca6c2f6a90ee65d7fcba0c1af5eadb4acb4b6b30b6d9e30502f5812169ac5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxAgeInSeconds")
    def reset_max_age_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAgeInSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="allowedHeadersInput")
    def allowed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="exposedHeadersInput")
    def exposed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exposedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSecondsInput")
    def max_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186f58758d45666737984dcb8ca1123c4e280cdc12800cb7d6f4bdec42ef8f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2de4455ff002a1e90ba90f2ca21f51bded088bc5b93807f3b3210669f572e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c63c0a6dd8d7bc0c729a5a546183b255af6af8ce992a7e7bed8770cc8627faa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposedHeaders")
    def exposed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposedHeaders"))

    @exposed_headers.setter
    def exposed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cf87e20d644320421d77260b97acb97906cdcdbed59070dd5072b00f1dcea95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSeconds")
    def max_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAgeInSeconds"))

    @max_age_in_seconds.setter
    def max_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4edcf8013daf653ea18e980b20f43e3de77f9ccebee6c08a2881c8b7e591805c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbAccountCorsRule]:
        return typing.cast(typing.Optional[CosmosdbAccountCorsRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CosmosdbAccountCorsRule]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5cb3bfd9db5b712a2548d4dcba75303dffbd4d136eac1be0d997526fd17bd16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountGeoLocation",
    jsii_struct_bases=[],
    name_mapping={
        "failover_priority": "failoverPriority",
        "location": "location",
        "zone_redundant": "zoneRedundant",
    },
)
class CosmosdbAccountGeoLocation:
    def __init__(
        self,
        *,
        failover_priority: jsii.Number,
        location: builtins.str,
        zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param failover_priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#failover_priority CosmosdbAccount#failover_priority}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#location CosmosdbAccount#location}.
        :param zone_redundant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#zone_redundant CosmosdbAccount#zone_redundant}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ea689418f13aff93f1603ae3c1fb19f507d106f95ec6b670c09b88f869663c)
            check_type(argname="argument failover_priority", value=failover_priority, expected_type=type_hints["failover_priority"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument zone_redundant", value=zone_redundant, expected_type=type_hints["zone_redundant"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "failover_priority": failover_priority,
            "location": location,
        }
        if zone_redundant is not None:
            self._values["zone_redundant"] = zone_redundant

    @builtins.property
    def failover_priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#failover_priority CosmosdbAccount#failover_priority}.'''
        result = self._values.get("failover_priority")
        assert result is not None, "Required property 'failover_priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#location CosmosdbAccount#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone_redundant(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#zone_redundant CosmosdbAccount#zone_redundant}.'''
        result = self._values.get("zone_redundant")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountGeoLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountGeoLocationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountGeoLocationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4da8f8f4c536f2bb4523616ae7926671d03b571d41ba3ec9375c8e55832e267)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CosmosdbAccountGeoLocationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a089b6e49b56ae5e2013e800832ad09beb02adc6a4ad546b9e1da008ff8ec516)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbAccountGeoLocationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2507a24126f305ddb1e114a3b10db29f9abfd032e2e4b57095e1a8c26d9fb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51825d99d94634606979f5e80810438c2d283db9eb4ea897dcfe35d61e29c4b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4af04077834dc6857e5a64b3b782ae4ee31a811c86031d820347c8c0329f2af8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountGeoLocation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountGeoLocation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountGeoLocation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb52f2053973b7fa638af177e56e888a5f6ce867f81ae3b145383cad74ebc915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbAccountGeoLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountGeoLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11a86cf54003312fb4f3f85cfe2438058188f73c21852089b2d53ce707a11ee5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetZoneRedundant")
    def reset_zone_redundant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneRedundant", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="failoverPriorityInput")
    def failover_priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failoverPriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneRedundantInput")
    def zone_redundant_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zoneRedundantInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverPriority")
    def failover_priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failoverPriority"))

    @failover_priority.setter
    def failover_priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d347fbbb3e589f787c60479e4f585f432e9753b7f1d14d352b424bf5f6b1b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverPriority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb3b6887589a4e65e302ede44de24fd0bd8da037ecbc8594d0b3871a19e8ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneRedundant")
    def zone_redundant(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zoneRedundant"))

    @zone_redundant.setter
    def zone_redundant(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9bbfd7c754b746622fbd9413261f3433d9dd3163f31ce35d108a314e2f1aadf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneRedundant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountGeoLocation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountGeoLocation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountGeoLocation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18407c5e76d02c53f72b463ea5b7c953ee2fdf807a36bbd26a62dde990d67be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class CosmosdbAccountIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#type CosmosdbAccount#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#identity_ids CosmosdbAccount#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf876e71ec99606ccb75f7db07c0f5e6d2c1a81e6133bf6037316974a1ae6af)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#type CosmosdbAccount#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#identity_ids CosmosdbAccount#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37c6fe996e258bfb4f202cb0613f018e3150cc87aa19da42fb71f5e4c1a451b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4f776742e1e72098cfce830e9a737d2bf4c229a0ce4e5cecddb375f0aa27502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45e988a44148cdf502c36cd87a78bf26241b3da4ce1e7b4886073ca041e35d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbAccountIdentity]:
        return typing.cast(typing.Optional[CosmosdbAccountIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CosmosdbAccountIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be0ff35faa7da77a3f1068a4535cb4bfc45da085edb83e766922223e3b59472f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountRestore",
    jsii_struct_bases=[],
    name_mapping={
        "restore_timestamp_in_utc": "restoreTimestampInUtc",
        "source_cosmosdb_account_id": "sourceCosmosdbAccountId",
        "database": "database",
        "gremlin_database": "gremlinDatabase",
        "tables_to_restore": "tablesToRestore",
    },
)
class CosmosdbAccountRestore:
    def __init__(
        self,
        *,
        restore_timestamp_in_utc: builtins.str,
        source_cosmosdb_account_id: builtins.str,
        database: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountRestoreDatabase", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gremlin_database: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CosmosdbAccountRestoreGremlinDatabase", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tables_to_restore: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param restore_timestamp_in_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#restore_timestamp_in_utc CosmosdbAccount#restore_timestamp_in_utc}.
        :param source_cosmosdb_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#source_cosmosdb_account_id CosmosdbAccount#source_cosmosdb_account_id}.
        :param database: database block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#database CosmosdbAccount#database}
        :param gremlin_database: gremlin_database block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#gremlin_database CosmosdbAccount#gremlin_database}
        :param tables_to_restore: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#tables_to_restore CosmosdbAccount#tables_to_restore}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b430088fd31eabdc8c3ce9c7d66c4b6c2f2fca2f425d3c55afa5e87f1b7d73fd)
            check_type(argname="argument restore_timestamp_in_utc", value=restore_timestamp_in_utc, expected_type=type_hints["restore_timestamp_in_utc"])
            check_type(argname="argument source_cosmosdb_account_id", value=source_cosmosdb_account_id, expected_type=type_hints["source_cosmosdb_account_id"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument gremlin_database", value=gremlin_database, expected_type=type_hints["gremlin_database"])
            check_type(argname="argument tables_to_restore", value=tables_to_restore, expected_type=type_hints["tables_to_restore"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "restore_timestamp_in_utc": restore_timestamp_in_utc,
            "source_cosmosdb_account_id": source_cosmosdb_account_id,
        }
        if database is not None:
            self._values["database"] = database
        if gremlin_database is not None:
            self._values["gremlin_database"] = gremlin_database
        if tables_to_restore is not None:
            self._values["tables_to_restore"] = tables_to_restore

    @builtins.property
    def restore_timestamp_in_utc(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#restore_timestamp_in_utc CosmosdbAccount#restore_timestamp_in_utc}.'''
        result = self._values.get("restore_timestamp_in_utc")
        assert result is not None, "Required property 'restore_timestamp_in_utc' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_cosmosdb_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#source_cosmosdb_account_id CosmosdbAccount#source_cosmosdb_account_id}.'''
        result = self._values.get("source_cosmosdb_account_id")
        assert result is not None, "Required property 'source_cosmosdb_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountRestoreDatabase"]]]:
        '''database block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#database CosmosdbAccount#database}
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountRestoreDatabase"]]], result)

    @builtins.property
    def gremlin_database(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountRestoreGremlinDatabase"]]]:
        '''gremlin_database block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#gremlin_database CosmosdbAccount#gremlin_database}
        '''
        result = self._values.get("gremlin_database")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CosmosdbAccountRestoreGremlinDatabase"]]], result)

    @builtins.property
    def tables_to_restore(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#tables_to_restore CosmosdbAccount#tables_to_restore}.'''
        result = self._values.get("tables_to_restore")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountRestore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountRestoreDatabase",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "collection_names": "collectionNames"},
)
class CosmosdbAccountRestoreDatabase:
    def __init__(
        self,
        *,
        name: builtins.str,
        collection_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#name CosmosdbAccount#name}.
        :param collection_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#collection_names CosmosdbAccount#collection_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0b056bb95624b65c9178b5a8261ed935fb72349f733d57f8c3a96218298b5f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument collection_names", value=collection_names, expected_type=type_hints["collection_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if collection_names is not None:
            self._values["collection_names"] = collection_names

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#name CosmosdbAccount#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def collection_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#collection_names CosmosdbAccount#collection_names}.'''
        result = self._values.get("collection_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountRestoreDatabase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountRestoreDatabaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountRestoreDatabaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f718e769af6ad6d9dfc1626c6bdd42460f4458b5d72936fec33dce95dbe7b708)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbAccountRestoreDatabaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30a5de7db76d7051b44cb377cb9adb967a96d842b728c982ac6be0b00fc7e21)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbAccountRestoreDatabaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0746d6a7b8a3e97ed44b0d82c6d0c5992ff9426fc0a59e43ae51557e145a95b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__468203520c3ed1f218ce8053710cb941fefe3c647473f5b51a5af214336b2079)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bf7210a5e28463c2d13a8c57031d1986b72161bd3597e2d13e751f758586fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreDatabase]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreDatabase]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreDatabase]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c768d544121859d71267990aa5f0d6a9b60aa93b46f868fdfbd37be8dc08b0ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbAccountRestoreDatabaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountRestoreDatabaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8006fb73c35c5f30c377fb002533d6b395434d00a7714f4b808e3e45b86d84a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCollectionNames")
    def reset_collection_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollectionNames", []))

    @builtins.property
    @jsii.member(jsii_name="collectionNamesInput")
    def collection_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "collectionNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionNames")
    def collection_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "collectionNames"))

    @collection_names.setter
    def collection_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233cec59ddc9053880afd66ff3c608e57955bf4438d9b4546278973d9c5c8289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544d21c1d34bb9935cc14a4e4f1c48be32028900d5616fb874c652445699b517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountRestoreDatabase]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountRestoreDatabase]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountRestoreDatabase]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__004ddf9af022abe4ebff71db084fc8c7724051eecda3ecdd7772f395ba7a3051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountRestoreGremlinDatabase",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "graph_names": "graphNames"},
)
class CosmosdbAccountRestoreGremlinDatabase:
    def __init__(
        self,
        *,
        name: builtins.str,
        graph_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#name CosmosdbAccount#name}.
        :param graph_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#graph_names CosmosdbAccount#graph_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4152e99fc5bd13a5b59e26efacd9e1dec68ba96ea3ab02d27e38702c105f2e59)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument graph_names", value=graph_names, expected_type=type_hints["graph_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if graph_names is not None:
            self._values["graph_names"] = graph_names

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#name CosmosdbAccount#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def graph_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#graph_names CosmosdbAccount#graph_names}.'''
        result = self._values.get("graph_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountRestoreGremlinDatabase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountRestoreGremlinDatabaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountRestoreGremlinDatabaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee5140ad28330516236a9498939a99db8fe9d40b87513b1799a964982a0019de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbAccountRestoreGremlinDatabaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10fded7afcb61e344297ac34f47eeeac4cda412374249c60ecf4c04b7514ce2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbAccountRestoreGremlinDatabaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb31139e8bb7a04e78ea90e6e47e83c96d355059fbf6ed6a321fc663fce2d43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eeb9092b5e9a7e84dde16c0b2a38ac6e21e20f4187fc3198a24e16f4e2256838)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79df9ae03b063831434b8714b3a4b2d5b3717affde133f840ecb58343f9805c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreGremlinDatabase]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreGremlinDatabase]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreGremlinDatabase]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e38ebdea4d7063f5fdc45880873a099fa1b2230cb24828b220ab01c59db1cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbAccountRestoreGremlinDatabaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountRestoreGremlinDatabaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9216d89031c53f2cd0b1d0f40ed59e9f365eb65378b3448882888a8639a0378a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGraphNames")
    def reset_graph_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGraphNames", []))

    @builtins.property
    @jsii.member(jsii_name="graphNamesInput")
    def graph_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "graphNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="graphNames")
    def graph_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "graphNames"))

    @graph_names.setter
    def graph_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a947e33c7c0f696ecd097701227d0053f5e81edebf4c0887f268578b00563da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "graphNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6500d222332d1e0198ae77a150e31b1fc0f45be841690f4c1894489d88b19b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountRestoreGremlinDatabase]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountRestoreGremlinDatabase]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountRestoreGremlinDatabase]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fbfc3325b2ccaabfa725a689857598063a31e3998734ca443008817293cae75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbAccountRestoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountRestoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__964996d24d1e6fe50eef442c40699f39a01ff405a6c8bd8d836c12ad8cf30f41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDatabase")
    def put_database(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountRestoreDatabase, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90a112688869d389733c102ee6d41a6f1b530dd11b811641abbe019ab1abc43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDatabase", [value]))

    @jsii.member(jsii_name="putGremlinDatabase")
    def put_gremlin_database(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountRestoreGremlinDatabase, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500b55d0c66b037f28f642746697216726a3c544cf037a7b82762e09a6750cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGremlinDatabase", [value]))

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetGremlinDatabase")
    def reset_gremlin_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGremlinDatabase", []))

    @jsii.member(jsii_name="resetTablesToRestore")
    def reset_tables_to_restore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTablesToRestore", []))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> CosmosdbAccountRestoreDatabaseList:
        return typing.cast(CosmosdbAccountRestoreDatabaseList, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="gremlinDatabase")
    def gremlin_database(self) -> CosmosdbAccountRestoreGremlinDatabaseList:
        return typing.cast(CosmosdbAccountRestoreGremlinDatabaseList, jsii.get(self, "gremlinDatabase"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreDatabase]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreDatabase]]], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="gremlinDatabaseInput")
    def gremlin_database_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreGremlinDatabase]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreGremlinDatabase]]], jsii.get(self, "gremlinDatabaseInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreTimestampInUtcInput")
    def restore_timestamp_in_utc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restoreTimestampInUtcInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceCosmosdbAccountIdInput")
    def source_cosmosdb_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceCosmosdbAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tablesToRestoreInput")
    def tables_to_restore_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tablesToRestoreInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreTimestampInUtc")
    def restore_timestamp_in_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restoreTimestampInUtc"))

    @restore_timestamp_in_utc.setter
    def restore_timestamp_in_utc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deedf3cfdc9bd16dff21f1e4c8eb9a1ca8deb4c4ae8938b9fff630b32131946a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restoreTimestampInUtc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceCosmosdbAccountId")
    def source_cosmosdb_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceCosmosdbAccountId"))

    @source_cosmosdb_account_id.setter
    def source_cosmosdb_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f214cc1f5ed5da7dd57421d52d6bd0619b6a9b014b9c8c702a68fc9908792a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceCosmosdbAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tablesToRestore")
    def tables_to_restore(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tablesToRestore"))

    @tables_to_restore.setter
    def tables_to_restore(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9df0581415d97e7c42b614360b65e137ae9841786115335e424fe336ad14417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tablesToRestore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbAccountRestore]:
        return typing.cast(typing.Optional[CosmosdbAccountRestore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CosmosdbAccountRestore]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2e3a1c8b404bd93fc25ae44f936ec822015e0a59bd686d462ef69f797bd1a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class CosmosdbAccountTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#create CosmosdbAccount#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#delete CosmosdbAccount#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#read CosmosdbAccount#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#update CosmosdbAccount#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af732f9f83dabda6ad16b995792372f3f79ce7c66eab5259f24f53e8cb1f6953)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#create CosmosdbAccount#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#delete CosmosdbAccount#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#read CosmosdbAccount#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#update CosmosdbAccount#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7d96403fb6211a0227bd721ac8bbcfc94952072809e6f96d77ad833c3bde838)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0ee8ed388184c6dc38cd11899286dcc91c5ccb0e0aa4d8fb0cfb030163f8f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7e1b62d7c3b4184b22e4bcb8817f05b2c02b53d037b42069955a223f96e40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9731f01e8658ed2e0cb4fb2a251a978ac410aab43b39028910fa1b1004141e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f461ab42ed2060b221cf4bf8f8bce96755f49fdd0d061b3198f55ac503fa2df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f8e77db2e044111d8bdf263816a86a2963ac53042795b3d4798914a65baea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountVirtualNetworkRule",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "ignore_missing_vnet_service_endpoint": "ignoreMissingVnetServiceEndpoint",
    },
)
class CosmosdbAccountVirtualNetworkRule:
    def __init__(
        self,
        *,
        id: builtins.str,
        ignore_missing_vnet_service_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#id CosmosdbAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_missing_vnet_service_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#ignore_missing_vnet_service_endpoint CosmosdbAccount#ignore_missing_vnet_service_endpoint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4c3562116e2fb4008724dbd0e94d22c2481450fe3c12c4e5214a91c36ba7d6)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_missing_vnet_service_endpoint", value=ignore_missing_vnet_service_endpoint, expected_type=type_hints["ignore_missing_vnet_service_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if ignore_missing_vnet_service_endpoint is not None:
            self._values["ignore_missing_vnet_service_endpoint"] = ignore_missing_vnet_service_endpoint

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#id CosmosdbAccount#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ignore_missing_vnet_service_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_account#ignore_missing_vnet_service_endpoint CosmosdbAccount#ignore_missing_vnet_service_endpoint}.'''
        result = self._values.get("ignore_missing_vnet_service_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbAccountVirtualNetworkRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbAccountVirtualNetworkRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountVirtualNetworkRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bb9674460756c0d33fb104c1d093a55fca72e4938061735db8f0e06c9b1a74d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbAccountVirtualNetworkRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241334c0cf6cde8daf4a27c1bff373b9a896004415b99c88a5b6099a693fe103)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbAccountVirtualNetworkRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de71f9acfb08fb549652c0539942d5b7f9c4de5fee402250a447ee74e3a71d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6da2d4d8e5e9173cfda741e39f8114be58f125f98cb895a937ecd69417561518)
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
            type_hints = typing.get_type_hints(_typecheckingstub__198495cff33f5b2a74d2c4d65bbfd95e4f65b2465d1f9b355ae2bc29d9b7d8bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountVirtualNetworkRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountVirtualNetworkRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountVirtualNetworkRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340c6476ed72a40c161ec3e58b745c4e4d740fcfe6a3087f8555a4c44d985e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CosmosdbAccountVirtualNetworkRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbAccount.CosmosdbAccountVirtualNetworkRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7523fc8bfd2516fe18abeeeed08e1c0989662e626c13daa39cec92cc946a4fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIgnoreMissingVnetServiceEndpoint")
    def reset_ignore_missing_vnet_service_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreMissingVnetServiceEndpoint", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreMissingVnetServiceEndpointInput")
    def ignore_missing_vnet_service_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreMissingVnetServiceEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c43807abe551dbb04d014b6249ff93ea900d68ebd88bbd79e83ad20695e1138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreMissingVnetServiceEndpoint")
    def ignore_missing_vnet_service_endpoint(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreMissingVnetServiceEndpoint"))

    @ignore_missing_vnet_service_endpoint.setter
    def ignore_missing_vnet_service_endpoint(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7236232f2c7056901df79625f04947ac296bb966d0b6880afb56804e41de1593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreMissingVnetServiceEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountVirtualNetworkRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountVirtualNetworkRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountVirtualNetworkRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb8a813dbaedf494f899cc542680c5280b935f29a0956d995687f16305fe612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CosmosdbAccount",
    "CosmosdbAccountAnalyticalStorage",
    "CosmosdbAccountAnalyticalStorageOutputReference",
    "CosmosdbAccountBackup",
    "CosmosdbAccountBackupOutputReference",
    "CosmosdbAccountCapabilities",
    "CosmosdbAccountCapabilitiesList",
    "CosmosdbAccountCapabilitiesOutputReference",
    "CosmosdbAccountCapacity",
    "CosmosdbAccountCapacityOutputReference",
    "CosmosdbAccountConfig",
    "CosmosdbAccountConsistencyPolicy",
    "CosmosdbAccountConsistencyPolicyOutputReference",
    "CosmosdbAccountCorsRule",
    "CosmosdbAccountCorsRuleOutputReference",
    "CosmosdbAccountGeoLocation",
    "CosmosdbAccountGeoLocationList",
    "CosmosdbAccountGeoLocationOutputReference",
    "CosmosdbAccountIdentity",
    "CosmosdbAccountIdentityOutputReference",
    "CosmosdbAccountRestore",
    "CosmosdbAccountRestoreDatabase",
    "CosmosdbAccountRestoreDatabaseList",
    "CosmosdbAccountRestoreDatabaseOutputReference",
    "CosmosdbAccountRestoreGremlinDatabase",
    "CosmosdbAccountRestoreGremlinDatabaseList",
    "CosmosdbAccountRestoreGremlinDatabaseOutputReference",
    "CosmosdbAccountRestoreOutputReference",
    "CosmosdbAccountTimeouts",
    "CosmosdbAccountTimeoutsOutputReference",
    "CosmosdbAccountVirtualNetworkRule",
    "CosmosdbAccountVirtualNetworkRuleList",
    "CosmosdbAccountVirtualNetworkRuleOutputReference",
]

publication.publish()

def _typecheckingstub__085c9339620344e44d06a085f68f0f7b1414f62dba8f9a2e308e32f5ea95320d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    consistency_policy: typing.Union[CosmosdbAccountConsistencyPolicy, typing.Dict[builtins.str, typing.Any]],
    geo_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountGeoLocation, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    offer_type: builtins.str,
    resource_group_name: builtins.str,
    access_key_metadata_writes_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    analytical_storage: typing.Optional[typing.Union[CosmosdbAccountAnalyticalStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    analytical_storage_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backup: typing.Optional[typing.Union[CosmosdbAccountBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    burst_capacity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    capabilities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountCapabilities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity: typing.Optional[typing.Union[CosmosdbAccountCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
    cors_rule: typing.Optional[typing.Union[CosmosdbAccountCorsRule, typing.Dict[builtins.str, typing.Any]]] = None,
    create_mode: typing.Optional[builtins.str] = None,
    default_identity_type: typing.Optional[builtins.str] = None,
    free_tier_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[CosmosdbAccountIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_range_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_virtual_network_filter_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_vault_key_id: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
    local_authentication_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    managed_hsm_key_id: typing.Optional[builtins.str] = None,
    minimal_tls_version: typing.Optional[builtins.str] = None,
    mongo_server_version: typing.Optional[builtins.str] = None,
    multiple_write_locations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_acl_bypass_for_azure_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_acl_bypass_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    partition_merge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restore: typing.Optional[typing.Union[CosmosdbAccountRestore, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CosmosdbAccountTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountVirtualNetworkRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__dd89baba10d5ba119000d8a679240f8f738f6d9e971c04d7aa77682ec0cc16b1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16af7070edc17b6c874186c7df98e29933a10880d1d6f81c3ebbd78858d5dd8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountCapabilities, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca0849289cb204bf253c3b4f107578406fb55d63c3984e2a32dbfe4328714d7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountGeoLocation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deeb902d1779b7d0d7ea08b00a55ec11f013ad9baf08db14cb022dfa5f1ebc67(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountVirtualNetworkRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d3b72ea2beb69fa2fc2cc2f7cffa7111cb238cb3a00e5dabcb8360f99000ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7402f18d0b5d324f174be6786da548cacb2a7f6a58fc8463763efab007ae62(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c895d2d389dbd3b06b84de3ee3691da7a41989c9e6bbd70cd6e2bf1c45ee2e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a6a15e3495a074afc80fc3277e64d1da4042a96646d9f161deac1c3cf55f49(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807b7691fca59dff1bfda7fa67d6fb86c34517f46e381a806c72692619c3ac10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59bb11319c00cdaff004782ca155acadb3b1b0fda574c8946d7f8ad32fcf71d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0206b625a6c9116a1ea9ad471255efca10e63c1a73a4f6e8ff9ea9df992feb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3771ef220817d3b23c613786087caa41da7eafd377d947166fad3555a7ac1804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c910fbf0cffab83a6c539a5bb2a949ff6df37d04f2756cad61061692bd8972e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c0261feb8b53f531f74d42c7e7348c8ec3c794990b857d17b9f4d7bec1bb15(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb1846afefc15a52b2a21716b13b90f43fb0a03111727a48b92a430c5ccc590(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5dd761a6b2c4f4abe9e331918b37408c9bb5a720028c34d10cc61419a96b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60233434a3b02dd06a69838f2a403e0103a71ab891b7c86d25ee65375b1ffcee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427ce2e19e14cdd015c52ad87ba816994702884f348ebaf66cfe8ce403b90742(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888c7a6cbcb782fa35c4c0e635f2bd73be176c5a517bc7750047612e55cd42de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb73cdf0a4fc3f45b13ecfb7816cd4d8a1c5cc606cef432513ecb8e3e0567b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc802f8a9ad40c5293b99642c3d25b988a0e0bd4ce12efd466f193915b72257a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b640e789f8d6eedb6c32983de6aaa2606443f871fd550b869043b7066aecb94(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4af4ac1bf4d073eabedc1801616d5ee30545a22655c0f837e41ef3b45a99bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553951c0bf2b474a4d139c3ab9a8de46e225f1d3bfe4839334c7d1318162abc9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d48e2c1f663da620fee0f5f11222da82e275fc8745b49d2ab72fbd4ccdfc596(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6960bdb33a0c9a21fd99dc288733bf1326184a0702bd0c523d628e194604f61f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee3a1d00770855c718f12b8c51e0f664ee0600e8ee7e3cb529148f23b080ae2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39543ce2b7087c596c0c5b9d87dce1c25f327086b368f746b6dac81758ca2cc3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa552a2732476860e6d429f04292139a11d21319f9b8a5a53b3689799f00f2f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd44838ebbd99adba8607aa325f9857d2c562da891351ef08f6101ce4fde14a7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4424a209bbc91122bcdd6689e7c49269cbf85b99043b3ff22bdefb80d68343dd(
    *,
    schema_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e876cb9f87603b2eae4cc53337966339d862dfc1cab745a814f733141ea4eea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21caa1e215458f99a652e4e422949cc25485f69d81030198cf46fc98a469ae01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bdc6b2ada8577369ff0105bbd5073b21aa4ef77dc1aa064ee87bd96d1cde1a3(
    value: typing.Optional[CosmosdbAccountAnalyticalStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b27f8b74c561ea315a42e1a08ef708c7c47bcd0f5925836c95a443b1953a4e(
    *,
    type: builtins.str,
    interval_in_minutes: typing.Optional[jsii.Number] = None,
    retention_in_hours: typing.Optional[jsii.Number] = None,
    storage_redundancy: typing.Optional[builtins.str] = None,
    tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472279438cfd3c0165d67c4011da04cfdd08bacb352f348de8cf8945a56e39c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74e653bf12aef76fa86be341a16489a1a16ea4299ba77e485d4d2a6d35a6fc2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e563f193bce7a3c1c75182352fc3a537a868b2e49256d77812bc7aa9c1489e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39de1884ce786abb7143a691d9efd313b04afe169fa9c9895e31e746a5d174ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45df28ca6500201e6eb8c694a30e3f8e351d28706d2faf2ce8cdc798e5819e23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d48bbab2d21571902797a14d7b3747b065822f9ec5c8f6db192fb91cadfb95d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d109304de2f04f69323566ac4a306c8282d5b66784cf8b01a993a03aeae06f(
    value: typing.Optional[CosmosdbAccountBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e66f8fcca563b812014289638b7bc12fda6a16e5296f4c59f4c439bd033e2b(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2cdb9369938ca78420243a440ab5d452254e1af476277d1c366b625903b76f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175d6bda5686978d482bcc8b5f35e0f84b88a2a357cd0f154de69290afe97d98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371de3fdff355ce3c12b6784b3202c180af78cb86294e884afc5e23d25f803fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1e9dcb8a627c79213996a67dde33cb0fddd9154f67d5f7b349da7b03a5d65a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcbf5fed54d9f584d514027dbfe8487b2e8ae5e18a3ee9f04dae35b1e888ac3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ddbb135414751d18452466036b0b70e61bd58c861a9ceb809c19b823d562c46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountCapabilities]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56a5b2c56ddc32b0624bc774cbd354260a7785646f02b749510754efd9dd8f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bf4968c5e502b71d4391df3aae48181cb93b8d4e92e92265c829adcb3ad87b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2976e3361ec821e1d9beb5eba7c35ab6b9eba229608a3c24508462d1f604df2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountCapabilities]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926aef6602376cd0db56e1500698492470c73800b02321ced39e244f83f4a1e3(
    *,
    total_throughput_limit: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2e73dd1cb8ddb8d28366dc6128a541b15d73f26ed8debe443d62826393fe86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01c3182c78b9dfdf31f134cdbeb46bf02af5f61921d5092af6092729f5c36fe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19eb36c3c5eb9fa85caff9a2cad80fd7c29effaa04875235fe0f68a689837f66(
    value: typing.Optional[CosmosdbAccountCapacity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e055a1f70fcd95fb3bdf526c9e20260df99edb887409a1245f6e1fbaf4da7f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    consistency_policy: typing.Union[CosmosdbAccountConsistencyPolicy, typing.Dict[builtins.str, typing.Any]],
    geo_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountGeoLocation, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    offer_type: builtins.str,
    resource_group_name: builtins.str,
    access_key_metadata_writes_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    analytical_storage: typing.Optional[typing.Union[CosmosdbAccountAnalyticalStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    analytical_storage_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backup: typing.Optional[typing.Union[CosmosdbAccountBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    burst_capacity_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    capabilities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountCapabilities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity: typing.Optional[typing.Union[CosmosdbAccountCapacity, typing.Dict[builtins.str, typing.Any]]] = None,
    cors_rule: typing.Optional[typing.Union[CosmosdbAccountCorsRule, typing.Dict[builtins.str, typing.Any]]] = None,
    create_mode: typing.Optional[builtins.str] = None,
    default_identity_type: typing.Optional[builtins.str] = None,
    free_tier_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[CosmosdbAccountIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_range_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_virtual_network_filter_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_vault_key_id: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
    local_authentication_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    managed_hsm_key_id: typing.Optional[builtins.str] = None,
    minimal_tls_version: typing.Optional[builtins.str] = None,
    mongo_server_version: typing.Optional[builtins.str] = None,
    multiple_write_locations_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_acl_bypass_for_azure_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    network_acl_bypass_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    partition_merge_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restore: typing.Optional[typing.Union[CosmosdbAccountRestore, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CosmosdbAccountTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountVirtualNetworkRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216db6b25eefb34604ee28a3f3161bbc5a4474e1badcf80773c79cb515a0910f(
    *,
    consistency_level: builtins.str,
    max_interval_in_seconds: typing.Optional[jsii.Number] = None,
    max_staleness_prefix: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bdc20e15bdfea07454c3f79d2cd29b9c321bc72d19218e56f92c3a6d5bc9f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff3097b4f79ca942dbdedb6a8748203bfb94bc6b34a01f3225c82326c352e9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8f0f0507908d3020e20f099a877864b9606dec866ce703191e698576350498(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2817e238fe0eab435e6d8c540b0044db970e651438c29180ab189ffec8cd384(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491aee0f35a8a65fa920535836bbe1c40c0c3e405bd3096975ef630ed0d7c23b(
    value: typing.Optional[CosmosdbAccountConsistencyPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f5e2125a799ef0f9c2f66ccca11d2c4ba1d5737501bfdd19587cad1f2160d2(
    *,
    allowed_headers: typing.Sequence[builtins.str],
    allowed_methods: typing.Sequence[builtins.str],
    allowed_origins: typing.Sequence[builtins.str],
    exposed_headers: typing.Sequence[builtins.str],
    max_age_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ca6c2f6a90ee65d7fcba0c1af5eadb4acb4b6b30b6d9e30502f5812169ac5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186f58758d45666737984dcb8ca1123c4e280cdc12800cb7d6f4bdec42ef8f1c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2de4455ff002a1e90ba90f2ca21f51bded088bc5b93807f3b3210669f572e21(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63c0a6dd8d7bc0c729a5a546183b255af6af8ce992a7e7bed8770cc8627faa5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf87e20d644320421d77260b97acb97906cdcdbed59070dd5072b00f1dcea95(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edcf8013daf653ea18e980b20f43e3de77f9ccebee6c08a2881c8b7e591805c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5cb3bfd9db5b712a2548d4dcba75303dffbd4d136eac1be0d997526fd17bd16(
    value: typing.Optional[CosmosdbAccountCorsRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ea689418f13aff93f1603ae3c1fb19f507d106f95ec6b670c09b88f869663c(
    *,
    failover_priority: jsii.Number,
    location: builtins.str,
    zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4da8f8f4c536f2bb4523616ae7926671d03b571d41ba3ec9375c8e55832e267(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a089b6e49b56ae5e2013e800832ad09beb02adc6a4ad546b9e1da008ff8ec516(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2507a24126f305ddb1e114a3b10db29f9abfd032e2e4b57095e1a8c26d9fb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51825d99d94634606979f5e80810438c2d283db9eb4ea897dcfe35d61e29c4b3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af04077834dc6857e5a64b3b782ae4ee31a811c86031d820347c8c0329f2af8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb52f2053973b7fa638af177e56e888a5f6ce867f81ae3b145383cad74ebc915(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountGeoLocation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a86cf54003312fb4f3f85cfe2438058188f73c21852089b2d53ce707a11ee5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d347fbbb3e589f787c60479e4f585f432e9753b7f1d14d352b424bf5f6b1b95(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb3b6887589a4e65e302ede44de24fd0bd8da037ecbc8594d0b3871a19e8ce7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9bbfd7c754b746622fbd9413261f3433d9dd3163f31ce35d108a314e2f1aadf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18407c5e76d02c53f72b463ea5b7c953ee2fdf807a36bbd26a62dde990d67be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountGeoLocation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf876e71ec99606ccb75f7db07c0f5e6d2c1a81e6133bf6037316974a1ae6af(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c6fe996e258bfb4f202cb0613f018e3150cc87aa19da42fb71f5e4c1a451b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f776742e1e72098cfce830e9a737d2bf4c229a0ce4e5cecddb375f0aa27502(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45e988a44148cdf502c36cd87a78bf26241b3da4ce1e7b4886073ca041e35d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0ff35faa7da77a3f1068a4535cb4bfc45da085edb83e766922223e3b59472f(
    value: typing.Optional[CosmosdbAccountIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b430088fd31eabdc8c3ce9c7d66c4b6c2f2fca2f425d3c55afa5e87f1b7d73fd(
    *,
    restore_timestamp_in_utc: builtins.str,
    source_cosmosdb_account_id: builtins.str,
    database: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountRestoreDatabase, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gremlin_database: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountRestoreGremlinDatabase, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tables_to_restore: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0b056bb95624b65c9178b5a8261ed935fb72349f733d57f8c3a96218298b5f(
    *,
    name: builtins.str,
    collection_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f718e769af6ad6d9dfc1626c6bdd42460f4458b5d72936fec33dce95dbe7b708(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30a5de7db76d7051b44cb377cb9adb967a96d842b728c982ac6be0b00fc7e21(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0746d6a7b8a3e97ed44b0d82c6d0c5992ff9426fc0a59e43ae51557e145a95b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468203520c3ed1f218ce8053710cb941fefe3c647473f5b51a5af214336b2079(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf7210a5e28463c2d13a8c57031d1986b72161bd3597e2d13e751f758586fc9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c768d544121859d71267990aa5f0d6a9b60aa93b46f868fdfbd37be8dc08b0ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreDatabase]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8006fb73c35c5f30c377fb002533d6b395434d00a7714f4b808e3e45b86d84a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233cec59ddc9053880afd66ff3c608e57955bf4438d9b4546278973d9c5c8289(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544d21c1d34bb9935cc14a4e4f1c48be32028900d5616fb874c652445699b517(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004ddf9af022abe4ebff71db084fc8c7724051eecda3ecdd7772f395ba7a3051(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountRestoreDatabase]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4152e99fc5bd13a5b59e26efacd9e1dec68ba96ea3ab02d27e38702c105f2e59(
    *,
    name: builtins.str,
    graph_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5140ad28330516236a9498939a99db8fe9d40b87513b1799a964982a0019de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10fded7afcb61e344297ac34f47eeeac4cda412374249c60ecf4c04b7514ce2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb31139e8bb7a04e78ea90e6e47e83c96d355059fbf6ed6a321fc663fce2d43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb9092b5e9a7e84dde16c0b2a38ac6e21e20f4187fc3198a24e16f4e2256838(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79df9ae03b063831434b8714b3a4b2d5b3717affde133f840ecb58343f9805c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e38ebdea4d7063f5fdc45880873a099fa1b2230cb24828b220ab01c59db1cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountRestoreGremlinDatabase]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9216d89031c53f2cd0b1d0f40ed59e9f365eb65378b3448882888a8639a0378a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a947e33c7c0f696ecd097701227d0053f5e81edebf4c0887f268578b00563da(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6500d222332d1e0198ae77a150e31b1fc0f45be841690f4c1894489d88b19b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fbfc3325b2ccaabfa725a689857598063a31e3998734ca443008817293cae75(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountRestoreGremlinDatabase]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964996d24d1e6fe50eef442c40699f39a01ff405a6c8bd8d836c12ad8cf30f41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90a112688869d389733c102ee6d41a6f1b530dd11b811641abbe019ab1abc43(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountRestoreDatabase, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500b55d0c66b037f28f642746697216726a3c544cf037a7b82762e09a6750cb3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CosmosdbAccountRestoreGremlinDatabase, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deedf3cfdc9bd16dff21f1e4c8eb9a1ca8deb4c4ae8938b9fff630b32131946a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f214cc1f5ed5da7dd57421d52d6bd0619b6a9b014b9c8c702a68fc9908792a1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9df0581415d97e7c42b614360b65e137ae9841786115335e424fe336ad14417(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2e3a1c8b404bd93fc25ae44f936ec822015e0a59bd686d462ef69f797bd1a8(
    value: typing.Optional[CosmosdbAccountRestore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af732f9f83dabda6ad16b995792372f3f79ce7c66eab5259f24f53e8cb1f6953(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d96403fb6211a0227bd721ac8bbcfc94952072809e6f96d77ad833c3bde838(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ee8ed388184c6dc38cd11899286dcc91c5ccb0e0aa4d8fb0cfb030163f8f0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7e1b62d7c3b4184b22e4bcb8817f05b2c02b53d037b42069955a223f96e40f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9731f01e8658ed2e0cb4fb2a251a978ac410aab43b39028910fa1b1004141e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f461ab42ed2060b221cf4bf8f8bce96755f49fdd0d061b3198f55ac503fa2df0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f8e77db2e044111d8bdf263816a86a2963ac53042795b3d4798914a65baea3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4c3562116e2fb4008724dbd0e94d22c2481450fe3c12c4e5214a91c36ba7d6(
    *,
    id: builtins.str,
    ignore_missing_vnet_service_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb9674460756c0d33fb104c1d093a55fca72e4938061735db8f0e06c9b1a74d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241334c0cf6cde8daf4a27c1bff373b9a896004415b99c88a5b6099a693fe103(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de71f9acfb08fb549652c0539942d5b7f9c4de5fee402250a447ee74e3a71d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da2d4d8e5e9173cfda741e39f8114be58f125f98cb895a937ecd69417561518(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198495cff33f5b2a74d2c4d65bbfd95e4f65b2465d1f9b355ae2bc29d9b7d8bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340c6476ed72a40c161ec3e58b745c4e4d740fcfe6a3087f8555a4c44d985e14(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CosmosdbAccountVirtualNetworkRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7523fc8bfd2516fe18abeeeed08e1c0989662e626c13daa39cec92cc946a4fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c43807abe551dbb04d014b6249ff93ea900d68ebd88bbd79e83ad20695e1138(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7236232f2c7056901df79625f04947ac296bb966d0b6880afb56804e41de1593(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb8a813dbaedf494f899cc542680c5280b935f29a0956d995687f16305fe612(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbAccountVirtualNetworkRule]],
) -> None:
    """Type checking stubs"""
    pass
