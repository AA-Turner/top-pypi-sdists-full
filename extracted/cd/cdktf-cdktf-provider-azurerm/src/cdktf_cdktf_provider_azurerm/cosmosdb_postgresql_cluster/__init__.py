r'''
# `azurerm_cosmosdb_postgresql_cluster`

Refer to the Terraform Registry for docs: [`azurerm_cosmosdb_postgresql_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster).
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


class CosmosdbPostgresqlCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbPostgresqlCluster.CosmosdbPostgresqlCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster azurerm_cosmosdb_postgresql_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        node_count: jsii.Number,
        resource_group_name: builtins.str,
        administrator_login_password: typing.Optional[builtins.str] = None,
        citus_version: typing.Optional[builtins.str] = None,
        coordinator_public_ip_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        coordinator_server_edition: typing.Optional[builtins.str] = None,
        coordinator_storage_quota_in_mb: typing.Optional[jsii.Number] = None,
        coordinator_vcore_count: typing.Optional[jsii.Number] = None,
        ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["CosmosdbPostgresqlClusterMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        node_public_ip_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        node_server_edition: typing.Optional[builtins.str] = None,
        node_storage_quota_in_mb: typing.Optional[jsii.Number] = None,
        node_vcores: typing.Optional[jsii.Number] = None,
        point_in_time_in_utc: typing.Optional[builtins.str] = None,
        preferred_primary_zone: typing.Optional[builtins.str] = None,
        shards_on_coordinator_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_location: typing.Optional[builtins.str] = None,
        source_resource_id: typing.Optional[builtins.str] = None,
        sql_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CosmosdbPostgresqlClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster azurerm_cosmosdb_postgresql_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#location CosmosdbPostgresqlCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#name CosmosdbPostgresqlCluster#name}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_count CosmosdbPostgresqlCluster#node_count}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#resource_group_name CosmosdbPostgresqlCluster#resource_group_name}.
        :param administrator_login_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#administrator_login_password CosmosdbPostgresqlCluster#administrator_login_password}.
        :param citus_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#citus_version CosmosdbPostgresqlCluster#citus_version}.
        :param coordinator_public_ip_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_public_ip_access_enabled CosmosdbPostgresqlCluster#coordinator_public_ip_access_enabled}.
        :param coordinator_server_edition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_server_edition CosmosdbPostgresqlCluster#coordinator_server_edition}.
        :param coordinator_storage_quota_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_storage_quota_in_mb CosmosdbPostgresqlCluster#coordinator_storage_quota_in_mb}.
        :param coordinator_vcore_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_vcore_count CosmosdbPostgresqlCluster#coordinator_vcore_count}.
        :param ha_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#ha_enabled CosmosdbPostgresqlCluster#ha_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#id CosmosdbPostgresqlCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#maintenance_window CosmosdbPostgresqlCluster#maintenance_window}
        :param node_public_ip_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_public_ip_access_enabled CosmosdbPostgresqlCluster#node_public_ip_access_enabled}.
        :param node_server_edition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_server_edition CosmosdbPostgresqlCluster#node_server_edition}.
        :param node_storage_quota_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_storage_quota_in_mb CosmosdbPostgresqlCluster#node_storage_quota_in_mb}.
        :param node_vcores: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_vcores CosmosdbPostgresqlCluster#node_vcores}.
        :param point_in_time_in_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#point_in_time_in_utc CosmosdbPostgresqlCluster#point_in_time_in_utc}.
        :param preferred_primary_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#preferred_primary_zone CosmosdbPostgresqlCluster#preferred_primary_zone}.
        :param shards_on_coordinator_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#shards_on_coordinator_enabled CosmosdbPostgresqlCluster#shards_on_coordinator_enabled}.
        :param source_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#source_location CosmosdbPostgresqlCluster#source_location}.
        :param source_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#source_resource_id CosmosdbPostgresqlCluster#source_resource_id}.
        :param sql_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#sql_version CosmosdbPostgresqlCluster#sql_version}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#tags CosmosdbPostgresqlCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#timeouts CosmosdbPostgresqlCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07654fa020f828013cebfcc72e58c7ecd13436c503c1c7e0855e06ae2ba0ee8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CosmosdbPostgresqlClusterConfig(
            location=location,
            name=name,
            node_count=node_count,
            resource_group_name=resource_group_name,
            administrator_login_password=administrator_login_password,
            citus_version=citus_version,
            coordinator_public_ip_access_enabled=coordinator_public_ip_access_enabled,
            coordinator_server_edition=coordinator_server_edition,
            coordinator_storage_quota_in_mb=coordinator_storage_quota_in_mb,
            coordinator_vcore_count=coordinator_vcore_count,
            ha_enabled=ha_enabled,
            id=id,
            maintenance_window=maintenance_window,
            node_public_ip_access_enabled=node_public_ip_access_enabled,
            node_server_edition=node_server_edition,
            node_storage_quota_in_mb=node_storage_quota_in_mb,
            node_vcores=node_vcores,
            point_in_time_in_utc=point_in_time_in_utc,
            preferred_primary_zone=preferred_primary_zone,
            shards_on_coordinator_enabled=shards_on_coordinator_enabled,
            source_location=source_location,
            source_resource_id=source_resource_id,
            sql_version=sql_version,
            tags=tags,
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
        '''Generates CDKTF code for importing a CosmosdbPostgresqlCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CosmosdbPostgresqlCluster to import.
        :param import_from_id: The id of the existing CosmosdbPostgresqlCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CosmosdbPostgresqlCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf31f40411ae37858d28f8ab8264ec1e3f8e6f94301ce12b31fc78c3d04088ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(
        self,
        *,
        day_of_week: typing.Optional[jsii.Number] = None,
        start_hour: typing.Optional[jsii.Number] = None,
        start_minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#day_of_week CosmosdbPostgresqlCluster#day_of_week}.
        :param start_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#start_hour CosmosdbPostgresqlCluster#start_hour}.
        :param start_minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#start_minute CosmosdbPostgresqlCluster#start_minute}.
        '''
        value = CosmosdbPostgresqlClusterMaintenanceWindow(
            day_of_week=day_of_week, start_hour=start_hour, start_minute=start_minute
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#create CosmosdbPostgresqlCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#delete CosmosdbPostgresqlCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#read CosmosdbPostgresqlCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#update CosmosdbPostgresqlCluster#update}.
        '''
        value = CosmosdbPostgresqlClusterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdministratorLoginPassword")
    def reset_administrator_login_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorLoginPassword", []))

    @jsii.member(jsii_name="resetCitusVersion")
    def reset_citus_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCitusVersion", []))

    @jsii.member(jsii_name="resetCoordinatorPublicIpAccessEnabled")
    def reset_coordinator_public_ip_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoordinatorPublicIpAccessEnabled", []))

    @jsii.member(jsii_name="resetCoordinatorServerEdition")
    def reset_coordinator_server_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoordinatorServerEdition", []))

    @jsii.member(jsii_name="resetCoordinatorStorageQuotaInMb")
    def reset_coordinator_storage_quota_in_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoordinatorStorageQuotaInMb", []))

    @jsii.member(jsii_name="resetCoordinatorVcoreCount")
    def reset_coordinator_vcore_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoordinatorVcoreCount", []))

    @jsii.member(jsii_name="resetHaEnabled")
    def reset_ha_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetNodePublicIpAccessEnabled")
    def reset_node_public_ip_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodePublicIpAccessEnabled", []))

    @jsii.member(jsii_name="resetNodeServerEdition")
    def reset_node_server_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeServerEdition", []))

    @jsii.member(jsii_name="resetNodeStorageQuotaInMb")
    def reset_node_storage_quota_in_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeStorageQuotaInMb", []))

    @jsii.member(jsii_name="resetNodeVcores")
    def reset_node_vcores(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeVcores", []))

    @jsii.member(jsii_name="resetPointInTimeInUtc")
    def reset_point_in_time_in_utc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPointInTimeInUtc", []))

    @jsii.member(jsii_name="resetPreferredPrimaryZone")
    def reset_preferred_primary_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredPrimaryZone", []))

    @jsii.member(jsii_name="resetShardsOnCoordinatorEnabled")
    def reset_shards_on_coordinator_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShardsOnCoordinatorEnabled", []))

    @jsii.member(jsii_name="resetSourceLocation")
    def reset_source_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceLocation", []))

    @jsii.member(jsii_name="resetSourceResourceId")
    def reset_source_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceResourceId", []))

    @jsii.member(jsii_name="resetSqlVersion")
    def reset_sql_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlVersion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="earliestRestoreTime")
    def earliest_restore_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "earliestRestoreTime"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> "CosmosdbPostgresqlClusterMaintenanceWindowOutputReference":
        return typing.cast("CosmosdbPostgresqlClusterMaintenanceWindowOutputReference", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="servers")
    def servers(self) -> "CosmosdbPostgresqlClusterServersList":
        return typing.cast("CosmosdbPostgresqlClusterServersList", jsii.get(self, "servers"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CosmosdbPostgresqlClusterTimeoutsOutputReference":
        return typing.cast("CosmosdbPostgresqlClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginPasswordInput")
    def administrator_login_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorLoginPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="citusVersionInput")
    def citus_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "citusVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="coordinatorPublicIpAccessEnabledInput")
    def coordinator_public_ip_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "coordinatorPublicIpAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="coordinatorServerEditionInput")
    def coordinator_server_edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coordinatorServerEditionInput"))

    @builtins.property
    @jsii.member(jsii_name="coordinatorStorageQuotaInMbInput")
    def coordinator_storage_quota_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coordinatorStorageQuotaInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="coordinatorVcoreCountInput")
    def coordinator_vcore_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coordinatorVcoreCountInput"))

    @builtins.property
    @jsii.member(jsii_name="haEnabledInput")
    def ha_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "haEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional["CosmosdbPostgresqlClusterMaintenanceWindow"]:
        return typing.cast(typing.Optional["CosmosdbPostgresqlClusterMaintenanceWindow"], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpAccessEnabledInput")
    def node_public_ip_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nodePublicIpAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeServerEditionInput")
    def node_server_edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeServerEditionInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeStorageQuotaInMbInput")
    def node_storage_quota_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeStorageQuotaInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeVcoresInput")
    def node_vcores_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeVcoresInput"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeInUtcInput")
    def point_in_time_in_utc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pointInTimeInUtcInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredPrimaryZoneInput")
    def preferred_primary_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredPrimaryZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="shardsOnCoordinatorEnabledInput")
    def shards_on_coordinator_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "shardsOnCoordinatorEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceLocationInput")
    def source_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceResourceIdInput")
    def source_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlVersionInput")
    def sql_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CosmosdbPostgresqlClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CosmosdbPostgresqlClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginPassword")
    def administrator_login_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorLoginPassword"))

    @administrator_login_password.setter
    def administrator_login_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4fc3f5f85ccd5384dbc12c3aab37e645dba66c6139f87ac89716c6d5ccc90b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorLoginPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="citusVersion")
    def citus_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "citusVersion"))

    @citus_version.setter
    def citus_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec4aff7fcf994b7ecbb229685b25f9b375015f3a26b15c6f382b72a7fe26db9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "citusVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coordinatorPublicIpAccessEnabled")
    def coordinator_public_ip_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "coordinatorPublicIpAccessEnabled"))

    @coordinator_public_ip_access_enabled.setter
    def coordinator_public_ip_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7af85a236d429d6a8aff8307c6de2fffeaca22e90a7ac5ac2df6355587569d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coordinatorPublicIpAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coordinatorServerEdition")
    def coordinator_server_edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coordinatorServerEdition"))

    @coordinator_server_edition.setter
    def coordinator_server_edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d079e2746c408ca1d961dab02e612f25ccf907a07b8ce267ca046ea3d0f3cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coordinatorServerEdition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coordinatorStorageQuotaInMb")
    def coordinator_storage_quota_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coordinatorStorageQuotaInMb"))

    @coordinator_storage_quota_in_mb.setter
    def coordinator_storage_quota_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1512f4e3aee5ab9fa39ff1531066a25e43eea74308e1e57ac0c28940eee6ec53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coordinatorStorageQuotaInMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coordinatorVcoreCount")
    def coordinator_vcore_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coordinatorVcoreCount"))

    @coordinator_vcore_count.setter
    def coordinator_vcore_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf897d7d2a4a8af93f4b94a9a3ba794e7741225fecf8bddc6de9687cf8a27a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coordinatorVcoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="haEnabled")
    def ha_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "haEnabled"))

    @ha_enabled.setter
    def ha_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f2feff7157bb268d8205e0cb7b61eb17c5a6139cfcda850fc7aa4496226cc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f74a7a67cf6155e3563cad9e381e82607b226a06267ed0606307003f2a611172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4790b718b116b8d85e23e4fff3f208250fa29551470f5c290ba5374a21e154f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881775aa48e9117ae98b32a91f279a859198329916beef6ebd68f440d5deb8eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ec86877a26890c599e8ada3ae60226fcac09b6751371aa4ed6dde2c9ade643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodePublicIpAccessEnabled")
    def node_public_ip_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nodePublicIpAccessEnabled"))

    @node_public_ip_access_enabled.setter
    def node_public_ip_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a46dbc1051d514a827b0235759009b0c7dad3130e0135c01a52c35f5e542771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePublicIpAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeServerEdition")
    def node_server_edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeServerEdition"))

    @node_server_edition.setter
    def node_server_edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d5e382c757b28c336e6c597f4692027c132c52826ff134dc7306bef4a6a616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeServerEdition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeStorageQuotaInMb")
    def node_storage_quota_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeStorageQuotaInMb"))

    @node_storage_quota_in_mb.setter
    def node_storage_quota_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4436e222d0f7777aba9b8b492800fb5314b6f659365739a12977274b994c2f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeStorageQuotaInMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeVcores")
    def node_vcores(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeVcores"))

    @node_vcores.setter
    def node_vcores(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046fbbd395d03f6f8ef0b820021f1574450ed92fdca99e127ade832c490e9368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeVcores", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pointInTimeInUtc")
    def point_in_time_in_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pointInTimeInUtc"))

    @point_in_time_in_utc.setter
    def point_in_time_in_utc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4444ec45b4dfec6cb027e4e6afc942e273b5a7aece50e07beee22d7bc43123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTimeInUtc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredPrimaryZone")
    def preferred_primary_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredPrimaryZone"))

    @preferred_primary_zone.setter
    def preferred_primary_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b63cb221d909578658d8f2d557a58a8e0fcf355012c42593f0f468f07441f70f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredPrimaryZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25efed6aa5570d9a1d2c8940a7899135606ac5790d863e93c638dc39403601c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shardsOnCoordinatorEnabled")
    def shards_on_coordinator_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "shardsOnCoordinatorEnabled"))

    @shards_on_coordinator_enabled.setter
    def shards_on_coordinator_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf906b656f1863ca2ae6802d2a61332c6e5bce5507bebad11cc43354c2710ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shardsOnCoordinatorEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceLocation")
    def source_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceLocation"))

    @source_location.setter
    def source_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52673c42ec554c1967197fc8ab012cba845113a9497e2b0ae8527ae64dc5bda2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceResourceId")
    def source_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceResourceId"))

    @source_resource_id.setter
    def source_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__977f15343ca062e364802493cfb46506d5ef8f1c296e90353abd366e4842a1d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlVersion")
    def sql_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlVersion"))

    @sql_version.setter
    def sql_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fba989de9334acb39abd94924d48f548bf798801e2464516bbef744d2408d2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0302e61470581179177631c9297ce63b7e55d0e6894b4417f3e7c11fe9a6a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbPostgresqlCluster.CosmosdbPostgresqlClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "node_count": "nodeCount",
        "resource_group_name": "resourceGroupName",
        "administrator_login_password": "administratorLoginPassword",
        "citus_version": "citusVersion",
        "coordinator_public_ip_access_enabled": "coordinatorPublicIpAccessEnabled",
        "coordinator_server_edition": "coordinatorServerEdition",
        "coordinator_storage_quota_in_mb": "coordinatorStorageQuotaInMb",
        "coordinator_vcore_count": "coordinatorVcoreCount",
        "ha_enabled": "haEnabled",
        "id": "id",
        "maintenance_window": "maintenanceWindow",
        "node_public_ip_access_enabled": "nodePublicIpAccessEnabled",
        "node_server_edition": "nodeServerEdition",
        "node_storage_quota_in_mb": "nodeStorageQuotaInMb",
        "node_vcores": "nodeVcores",
        "point_in_time_in_utc": "pointInTimeInUtc",
        "preferred_primary_zone": "preferredPrimaryZone",
        "shards_on_coordinator_enabled": "shardsOnCoordinatorEnabled",
        "source_location": "sourceLocation",
        "source_resource_id": "sourceResourceId",
        "sql_version": "sqlVersion",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class CosmosdbPostgresqlClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        node_count: jsii.Number,
        resource_group_name: builtins.str,
        administrator_login_password: typing.Optional[builtins.str] = None,
        citus_version: typing.Optional[builtins.str] = None,
        coordinator_public_ip_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        coordinator_server_edition: typing.Optional[builtins.str] = None,
        coordinator_storage_quota_in_mb: typing.Optional[jsii.Number] = None,
        coordinator_vcore_count: typing.Optional[jsii.Number] = None,
        ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["CosmosdbPostgresqlClusterMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        node_public_ip_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        node_server_edition: typing.Optional[builtins.str] = None,
        node_storage_quota_in_mb: typing.Optional[jsii.Number] = None,
        node_vcores: typing.Optional[jsii.Number] = None,
        point_in_time_in_utc: typing.Optional[builtins.str] = None,
        preferred_primary_zone: typing.Optional[builtins.str] = None,
        shards_on_coordinator_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_location: typing.Optional[builtins.str] = None,
        source_resource_id: typing.Optional[builtins.str] = None,
        sql_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CosmosdbPostgresqlClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#location CosmosdbPostgresqlCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#name CosmosdbPostgresqlCluster#name}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_count CosmosdbPostgresqlCluster#node_count}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#resource_group_name CosmosdbPostgresqlCluster#resource_group_name}.
        :param administrator_login_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#administrator_login_password CosmosdbPostgresqlCluster#administrator_login_password}.
        :param citus_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#citus_version CosmosdbPostgresqlCluster#citus_version}.
        :param coordinator_public_ip_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_public_ip_access_enabled CosmosdbPostgresqlCluster#coordinator_public_ip_access_enabled}.
        :param coordinator_server_edition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_server_edition CosmosdbPostgresqlCluster#coordinator_server_edition}.
        :param coordinator_storage_quota_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_storage_quota_in_mb CosmosdbPostgresqlCluster#coordinator_storage_quota_in_mb}.
        :param coordinator_vcore_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_vcore_count CosmosdbPostgresqlCluster#coordinator_vcore_count}.
        :param ha_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#ha_enabled CosmosdbPostgresqlCluster#ha_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#id CosmosdbPostgresqlCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#maintenance_window CosmosdbPostgresqlCluster#maintenance_window}
        :param node_public_ip_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_public_ip_access_enabled CosmosdbPostgresqlCluster#node_public_ip_access_enabled}.
        :param node_server_edition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_server_edition CosmosdbPostgresqlCluster#node_server_edition}.
        :param node_storage_quota_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_storage_quota_in_mb CosmosdbPostgresqlCluster#node_storage_quota_in_mb}.
        :param node_vcores: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_vcores CosmosdbPostgresqlCluster#node_vcores}.
        :param point_in_time_in_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#point_in_time_in_utc CosmosdbPostgresqlCluster#point_in_time_in_utc}.
        :param preferred_primary_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#preferred_primary_zone CosmosdbPostgresqlCluster#preferred_primary_zone}.
        :param shards_on_coordinator_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#shards_on_coordinator_enabled CosmosdbPostgresqlCluster#shards_on_coordinator_enabled}.
        :param source_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#source_location CosmosdbPostgresqlCluster#source_location}.
        :param source_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#source_resource_id CosmosdbPostgresqlCluster#source_resource_id}.
        :param sql_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#sql_version CosmosdbPostgresqlCluster#sql_version}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#tags CosmosdbPostgresqlCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#timeouts CosmosdbPostgresqlCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(maintenance_window, dict):
            maintenance_window = CosmosdbPostgresqlClusterMaintenanceWindow(**maintenance_window)
        if isinstance(timeouts, dict):
            timeouts = CosmosdbPostgresqlClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa7b79ad540917118d6fd390aa727844354cff8ab6cbaf9ed7d9e89d3f906da)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument administrator_login_password", value=administrator_login_password, expected_type=type_hints["administrator_login_password"])
            check_type(argname="argument citus_version", value=citus_version, expected_type=type_hints["citus_version"])
            check_type(argname="argument coordinator_public_ip_access_enabled", value=coordinator_public_ip_access_enabled, expected_type=type_hints["coordinator_public_ip_access_enabled"])
            check_type(argname="argument coordinator_server_edition", value=coordinator_server_edition, expected_type=type_hints["coordinator_server_edition"])
            check_type(argname="argument coordinator_storage_quota_in_mb", value=coordinator_storage_quota_in_mb, expected_type=type_hints["coordinator_storage_quota_in_mb"])
            check_type(argname="argument coordinator_vcore_count", value=coordinator_vcore_count, expected_type=type_hints["coordinator_vcore_count"])
            check_type(argname="argument ha_enabled", value=ha_enabled, expected_type=type_hints["ha_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument node_public_ip_access_enabled", value=node_public_ip_access_enabled, expected_type=type_hints["node_public_ip_access_enabled"])
            check_type(argname="argument node_server_edition", value=node_server_edition, expected_type=type_hints["node_server_edition"])
            check_type(argname="argument node_storage_quota_in_mb", value=node_storage_quota_in_mb, expected_type=type_hints["node_storage_quota_in_mb"])
            check_type(argname="argument node_vcores", value=node_vcores, expected_type=type_hints["node_vcores"])
            check_type(argname="argument point_in_time_in_utc", value=point_in_time_in_utc, expected_type=type_hints["point_in_time_in_utc"])
            check_type(argname="argument preferred_primary_zone", value=preferred_primary_zone, expected_type=type_hints["preferred_primary_zone"])
            check_type(argname="argument shards_on_coordinator_enabled", value=shards_on_coordinator_enabled, expected_type=type_hints["shards_on_coordinator_enabled"])
            check_type(argname="argument source_location", value=source_location, expected_type=type_hints["source_location"])
            check_type(argname="argument source_resource_id", value=source_resource_id, expected_type=type_hints["source_resource_id"])
            check_type(argname="argument sql_version", value=sql_version, expected_type=type_hints["sql_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "node_count": node_count,
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
        if administrator_login_password is not None:
            self._values["administrator_login_password"] = administrator_login_password
        if citus_version is not None:
            self._values["citus_version"] = citus_version
        if coordinator_public_ip_access_enabled is not None:
            self._values["coordinator_public_ip_access_enabled"] = coordinator_public_ip_access_enabled
        if coordinator_server_edition is not None:
            self._values["coordinator_server_edition"] = coordinator_server_edition
        if coordinator_storage_quota_in_mb is not None:
            self._values["coordinator_storage_quota_in_mb"] = coordinator_storage_quota_in_mb
        if coordinator_vcore_count is not None:
            self._values["coordinator_vcore_count"] = coordinator_vcore_count
        if ha_enabled is not None:
            self._values["ha_enabled"] = ha_enabled
        if id is not None:
            self._values["id"] = id
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if node_public_ip_access_enabled is not None:
            self._values["node_public_ip_access_enabled"] = node_public_ip_access_enabled
        if node_server_edition is not None:
            self._values["node_server_edition"] = node_server_edition
        if node_storage_quota_in_mb is not None:
            self._values["node_storage_quota_in_mb"] = node_storage_quota_in_mb
        if node_vcores is not None:
            self._values["node_vcores"] = node_vcores
        if point_in_time_in_utc is not None:
            self._values["point_in_time_in_utc"] = point_in_time_in_utc
        if preferred_primary_zone is not None:
            self._values["preferred_primary_zone"] = preferred_primary_zone
        if shards_on_coordinator_enabled is not None:
            self._values["shards_on_coordinator_enabled"] = shards_on_coordinator_enabled
        if source_location is not None:
            self._values["source_location"] = source_location
        if source_resource_id is not None:
            self._values["source_resource_id"] = source_resource_id
        if sql_version is not None:
            self._values["sql_version"] = sql_version
        if tags is not None:
            self._values["tags"] = tags
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#location CosmosdbPostgresqlCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#name CosmosdbPostgresqlCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_count CosmosdbPostgresqlCluster#node_count}.'''
        result = self._values.get("node_count")
        assert result is not None, "Required property 'node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#resource_group_name CosmosdbPostgresqlCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administrator_login_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#administrator_login_password CosmosdbPostgresqlCluster#administrator_login_password}.'''
        result = self._values.get("administrator_login_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def citus_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#citus_version CosmosdbPostgresqlCluster#citus_version}.'''
        result = self._values.get("citus_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def coordinator_public_ip_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_public_ip_access_enabled CosmosdbPostgresqlCluster#coordinator_public_ip_access_enabled}.'''
        result = self._values.get("coordinator_public_ip_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def coordinator_server_edition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_server_edition CosmosdbPostgresqlCluster#coordinator_server_edition}.'''
        result = self._values.get("coordinator_server_edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def coordinator_storage_quota_in_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_storage_quota_in_mb CosmosdbPostgresqlCluster#coordinator_storage_quota_in_mb}.'''
        result = self._values.get("coordinator_storage_quota_in_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def coordinator_vcore_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#coordinator_vcore_count CosmosdbPostgresqlCluster#coordinator_vcore_count}.'''
        result = self._values.get("coordinator_vcore_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#ha_enabled CosmosdbPostgresqlCluster#ha_enabled}.'''
        result = self._values.get("ha_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#id CosmosdbPostgresqlCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["CosmosdbPostgresqlClusterMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#maintenance_window CosmosdbPostgresqlCluster#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["CosmosdbPostgresqlClusterMaintenanceWindow"], result)

    @builtins.property
    def node_public_ip_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_public_ip_access_enabled CosmosdbPostgresqlCluster#node_public_ip_access_enabled}.'''
        result = self._values.get("node_public_ip_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def node_server_edition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_server_edition CosmosdbPostgresqlCluster#node_server_edition}.'''
        result = self._values.get("node_server_edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_storage_quota_in_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_storage_quota_in_mb CosmosdbPostgresqlCluster#node_storage_quota_in_mb}.'''
        result = self._values.get("node_storage_quota_in_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_vcores(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#node_vcores CosmosdbPostgresqlCluster#node_vcores}.'''
        result = self._values.get("node_vcores")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def point_in_time_in_utc(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#point_in_time_in_utc CosmosdbPostgresqlCluster#point_in_time_in_utc}.'''
        result = self._values.get("point_in_time_in_utc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_primary_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#preferred_primary_zone CosmosdbPostgresqlCluster#preferred_primary_zone}.'''
        result = self._values.get("preferred_primary_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shards_on_coordinator_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#shards_on_coordinator_enabled CosmosdbPostgresqlCluster#shards_on_coordinator_enabled}.'''
        result = self._values.get("shards_on_coordinator_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#source_location CosmosdbPostgresqlCluster#source_location}.'''
        result = self._values.get("source_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#source_resource_id CosmosdbPostgresqlCluster#source_resource_id}.'''
        result = self._values.get("source_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#sql_version CosmosdbPostgresqlCluster#sql_version}.'''
        result = self._values.get("sql_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#tags CosmosdbPostgresqlCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CosmosdbPostgresqlClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#timeouts CosmosdbPostgresqlCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CosmosdbPostgresqlClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbPostgresqlClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbPostgresqlCluster.CosmosdbPostgresqlClusterMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={
        "day_of_week": "dayOfWeek",
        "start_hour": "startHour",
        "start_minute": "startMinute",
    },
)
class CosmosdbPostgresqlClusterMaintenanceWindow:
    def __init__(
        self,
        *,
        day_of_week: typing.Optional[jsii.Number] = None,
        start_hour: typing.Optional[jsii.Number] = None,
        start_minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#day_of_week CosmosdbPostgresqlCluster#day_of_week}.
        :param start_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#start_hour CosmosdbPostgresqlCluster#start_hour}.
        :param start_minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#start_minute CosmosdbPostgresqlCluster#start_minute}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbf14edd5da43b6d567f067bda3b481af55e6c95c7b9bb46fdcb7ab5dd23468)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument start_hour", value=start_hour, expected_type=type_hints["start_hour"])
            check_type(argname="argument start_minute", value=start_minute, expected_type=type_hints["start_minute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day_of_week is not None:
            self._values["day_of_week"] = day_of_week
        if start_hour is not None:
            self._values["start_hour"] = start_hour
        if start_minute is not None:
            self._values["start_minute"] = start_minute

    @builtins.property
    def day_of_week(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#day_of_week CosmosdbPostgresqlCluster#day_of_week}.'''
        result = self._values.get("day_of_week")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_hour(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#start_hour CosmosdbPostgresqlCluster#start_hour}.'''
        result = self._values.get("start_hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_minute(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#start_minute CosmosdbPostgresqlCluster#start_minute}.'''
        result = self._values.get("start_minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbPostgresqlClusterMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbPostgresqlClusterMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbPostgresqlCluster.CosmosdbPostgresqlClusterMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd80c0ec105b46e8b7c833aa6bc659e1977f0da9a632aaf000975e7a92d1d7b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDayOfWeek")
    def reset_day_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDayOfWeek", []))

    @jsii.member(jsii_name="resetStartHour")
    def reset_start_hour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartHour", []))

    @jsii.member(jsii_name="resetStartMinute")
    def reset_start_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartMinute", []))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="startHourInput")
    def start_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startHourInput"))

    @builtins.property
    @jsii.member(jsii_name="startMinuteInput")
    def start_minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startMinuteInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5af05ce32ad0c927da2fccab5d81da30b4500bfe6afc2f4fcc77a4e789a59a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startHour")
    def start_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startHour"))

    @start_hour.setter
    def start_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f0fc77cbacf0515c7706b4e272c74b5898e7aeece3f795a02f79e738781f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startMinute")
    def start_minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startMinute"))

    @start_minute.setter
    def start_minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2624126adce8b5cc1952e93eb15bb2b0f55b0f06a4f209934f81d5e33f6757c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startMinute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CosmosdbPostgresqlClusterMaintenanceWindow]:
        return typing.cast(typing.Optional[CosmosdbPostgresqlClusterMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CosmosdbPostgresqlClusterMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b89fc4ba36b5d117d26973c56ffe9d7b6e29d261ba07581abaed0637e6920f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbPostgresqlCluster.CosmosdbPostgresqlClusterServers",
    jsii_struct_bases=[],
    name_mapping={},
)
class CosmosdbPostgresqlClusterServers:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbPostgresqlClusterServers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbPostgresqlClusterServersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbPostgresqlCluster.CosmosdbPostgresqlClusterServersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd2eb956994a83a1b999d77d66bde985c1187c16d419ad8cd0d26c86e1d76eac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CosmosdbPostgresqlClusterServersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa1f09b015ea58d0f688c6eb37ca1271ec202946ef31dedc62a95eb4df9803b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CosmosdbPostgresqlClusterServersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36182bc215956421bce562d208528cf3282b3f0f81bc3b221cf1d2bbbbd6369)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b76167c2f0c054ec3a2ee9eeef1105bdc4b45a6102526d121a3bc0c2324d666e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bdc9166f316b9a2a03d23203281a780fa5bd966c0f3e63ccaf44a6da6d5d8bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CosmosdbPostgresqlClusterServersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbPostgresqlCluster.CosmosdbPostgresqlClusterServersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca49d8c00bdce25d62c4bc86429f10ca1fe82151f37ef9c5c75fa725d1ea685c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CosmosdbPostgresqlClusterServers]:
        return typing.cast(typing.Optional[CosmosdbPostgresqlClusterServers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CosmosdbPostgresqlClusterServers],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a6f9f9ae804bb66f2c7b621374243627a612599471799814dcfed7030148100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cosmosdbPostgresqlCluster.CosmosdbPostgresqlClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class CosmosdbPostgresqlClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#create CosmosdbPostgresqlCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#delete CosmosdbPostgresqlCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#read CosmosdbPostgresqlCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#update CosmosdbPostgresqlCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb8062335a55129407eb884e1b69b8868193a430120d245bd2aab1115b49f8d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#create CosmosdbPostgresqlCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#delete CosmosdbPostgresqlCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#read CosmosdbPostgresqlCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cosmosdb_postgresql_cluster#update CosmosdbPostgresqlCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosmosdbPostgresqlClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CosmosdbPostgresqlClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cosmosdbPostgresqlCluster.CosmosdbPostgresqlClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbdc66d93a9264af9016007cfba104496ff9d59faa3b7d862125b30b4d0b1431)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37874b0bcccca92f1b14744d8ab60f84da1b802e62258f2b229e8c8c443a5e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9e1d12572ded4e5e70a691f3c9b7d6d6964cf6040f96856e9e7b9d975644bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f6d77316cbe7ac6ffc99267861b1f805a4cb79d6312aa564c5ce4ada9f7ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eae7b6e71241097fe45c882f12a8f74c38ae933c68ed109a71405f6b54a57ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbPostgresqlClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbPostgresqlClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbPostgresqlClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3bb9d838ecd69959af0a62e4c347cca0b33925fa8f1fdc3d5d299e25431a16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CosmosdbPostgresqlCluster",
    "CosmosdbPostgresqlClusterConfig",
    "CosmosdbPostgresqlClusterMaintenanceWindow",
    "CosmosdbPostgresqlClusterMaintenanceWindowOutputReference",
    "CosmosdbPostgresqlClusterServers",
    "CosmosdbPostgresqlClusterServersList",
    "CosmosdbPostgresqlClusterServersOutputReference",
    "CosmosdbPostgresqlClusterTimeouts",
    "CosmosdbPostgresqlClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b07654fa020f828013cebfcc72e58c7ecd13436c503c1c7e0855e06ae2ba0ee8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    node_count: jsii.Number,
    resource_group_name: builtins.str,
    administrator_login_password: typing.Optional[builtins.str] = None,
    citus_version: typing.Optional[builtins.str] = None,
    coordinator_public_ip_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    coordinator_server_edition: typing.Optional[builtins.str] = None,
    coordinator_storage_quota_in_mb: typing.Optional[jsii.Number] = None,
    coordinator_vcore_count: typing.Optional[jsii.Number] = None,
    ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[CosmosdbPostgresqlClusterMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    node_public_ip_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    node_server_edition: typing.Optional[builtins.str] = None,
    node_storage_quota_in_mb: typing.Optional[jsii.Number] = None,
    node_vcores: typing.Optional[jsii.Number] = None,
    point_in_time_in_utc: typing.Optional[builtins.str] = None,
    preferred_primary_zone: typing.Optional[builtins.str] = None,
    shards_on_coordinator_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_location: typing.Optional[builtins.str] = None,
    source_resource_id: typing.Optional[builtins.str] = None,
    sql_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CosmosdbPostgresqlClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__cf31f40411ae37858d28f8ab8264ec1e3f8e6f94301ce12b31fc78c3d04088ae(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4fc3f5f85ccd5384dbc12c3aab37e645dba66c6139f87ac89716c6d5ccc90b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec4aff7fcf994b7ecbb229685b25f9b375015f3a26b15c6f382b72a7fe26db9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7af85a236d429d6a8aff8307c6de2fffeaca22e90a7ac5ac2df6355587569d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d079e2746c408ca1d961dab02e612f25ccf907a07b8ce267ca046ea3d0f3cdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1512f4e3aee5ab9fa39ff1531066a25e43eea74308e1e57ac0c28940eee6ec53(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf897d7d2a4a8af93f4b94a9a3ba794e7741225fecf8bddc6de9687cf8a27a5c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f2feff7157bb268d8205e0cb7b61eb17c5a6139cfcda850fc7aa4496226cc4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74a7a67cf6155e3563cad9e381e82607b226a06267ed0606307003f2a611172(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4790b718b116b8d85e23e4fff3f208250fa29551470f5c290ba5374a21e154f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881775aa48e9117ae98b32a91f279a859198329916beef6ebd68f440d5deb8eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ec86877a26890c599e8ada3ae60226fcac09b6751371aa4ed6dde2c9ade643(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a46dbc1051d514a827b0235759009b0c7dad3130e0135c01a52c35f5e542771(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d5e382c757b28c336e6c597f4692027c132c52826ff134dc7306bef4a6a616(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4436e222d0f7777aba9b8b492800fb5314b6f659365739a12977274b994c2f75(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046fbbd395d03f6f8ef0b820021f1574450ed92fdca99e127ade832c490e9368(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4444ec45b4dfec6cb027e4e6afc942e273b5a7aece50e07beee22d7bc43123(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63cb221d909578658d8f2d557a58a8e0fcf355012c42593f0f468f07441f70f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25efed6aa5570d9a1d2c8940a7899135606ac5790d863e93c638dc39403601c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf906b656f1863ca2ae6802d2a61332c6e5bce5507bebad11cc43354c2710ad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52673c42ec554c1967197fc8ab012cba845113a9497e2b0ae8527ae64dc5bda2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977f15343ca062e364802493cfb46506d5ef8f1c296e90353abd366e4842a1d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fba989de9334acb39abd94924d48f548bf798801e2464516bbef744d2408d2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0302e61470581179177631c9297ce63b7e55d0e6894b4417f3e7c11fe9a6a3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa7b79ad540917118d6fd390aa727844354cff8ab6cbaf9ed7d9e89d3f906da(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    node_count: jsii.Number,
    resource_group_name: builtins.str,
    administrator_login_password: typing.Optional[builtins.str] = None,
    citus_version: typing.Optional[builtins.str] = None,
    coordinator_public_ip_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    coordinator_server_edition: typing.Optional[builtins.str] = None,
    coordinator_storage_quota_in_mb: typing.Optional[jsii.Number] = None,
    coordinator_vcore_count: typing.Optional[jsii.Number] = None,
    ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[CosmosdbPostgresqlClusterMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    node_public_ip_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    node_server_edition: typing.Optional[builtins.str] = None,
    node_storage_quota_in_mb: typing.Optional[jsii.Number] = None,
    node_vcores: typing.Optional[jsii.Number] = None,
    point_in_time_in_utc: typing.Optional[builtins.str] = None,
    preferred_primary_zone: typing.Optional[builtins.str] = None,
    shards_on_coordinator_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_location: typing.Optional[builtins.str] = None,
    source_resource_id: typing.Optional[builtins.str] = None,
    sql_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CosmosdbPostgresqlClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbf14edd5da43b6d567f067bda3b481af55e6c95c7b9bb46fdcb7ab5dd23468(
    *,
    day_of_week: typing.Optional[jsii.Number] = None,
    start_hour: typing.Optional[jsii.Number] = None,
    start_minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd80c0ec105b46e8b7c833aa6bc659e1977f0da9a632aaf000975e7a92d1d7b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5af05ce32ad0c927da2fccab5d81da30b4500bfe6afc2f4fcc77a4e789a59a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f0fc77cbacf0515c7706b4e272c74b5898e7aeece3f795a02f79e738781f8c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2624126adce8b5cc1952e93eb15bb2b0f55b0f06a4f209934f81d5e33f6757c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b89fc4ba36b5d117d26973c56ffe9d7b6e29d261ba07581abaed0637e6920f(
    value: typing.Optional[CosmosdbPostgresqlClusterMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2eb956994a83a1b999d77d66bde985c1187c16d419ad8cd0d26c86e1d76eac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa1f09b015ea58d0f688c6eb37ca1271ec202946ef31dedc62a95eb4df9803b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36182bc215956421bce562d208528cf3282b3f0f81bc3b221cf1d2bbbbd6369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76167c2f0c054ec3a2ee9eeef1105bdc4b45a6102526d121a3bc0c2324d666e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdc9166f316b9a2a03d23203281a780fa5bd966c0f3e63ccaf44a6da6d5d8bf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca49d8c00bdce25d62c4bc86429f10ca1fe82151f37ef9c5c75fa725d1ea685c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6f9f9ae804bb66f2c7b621374243627a612599471799814dcfed7030148100(
    value: typing.Optional[CosmosdbPostgresqlClusterServers],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb8062335a55129407eb884e1b69b8868193a430120d245bd2aab1115b49f8d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdc66d93a9264af9016007cfba104496ff9d59faa3b7d862125b30b4d0b1431(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37874b0bcccca92f1b14744d8ab60f84da1b802e62258f2b229e8c8c443a5e0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9e1d12572ded4e5e70a691f3c9b7d6d6964cf6040f96856e9e7b9d975644bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f6d77316cbe7ac6ffc99267861b1f805a4cb79d6312aa564c5ce4ada9f7ac7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eae7b6e71241097fe45c882f12a8f74c38ae933c68ed109a71405f6b54a57ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3bb9d838ecd69959af0a62e4c347cca0b33925fa8f1fdc3d5d299e25431a16(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CosmosdbPostgresqlClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
