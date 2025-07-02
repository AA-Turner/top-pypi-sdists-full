r'''
# `azurerm_oracle_cloud_vm_cluster`

Refer to the Terraform Registry for docs: [`azurerm_oracle_cloud_vm_cluster`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster).
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


class OracleCloudVmCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.oracleCloudVmCluster.OracleCloudVmCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster azurerm_oracle_cloud_vm_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cloud_exadata_infrastructure_id: builtins.str,
        cpu_core_count: jsii.Number,
        db_servers: typing.Sequence[builtins.str],
        display_name: builtins.str,
        gi_version: builtins.str,
        hostname: builtins.str,
        license_model: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        ssh_public_keys: typing.Sequence[builtins.str],
        subnet_id: builtins.str,
        virtual_network_id: builtins.str,
        backup_subnet_cidr: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        data_collection_options: typing.Optional[typing.Union["OracleCloudVmClusterDataCollectionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        data_storage_percentage: typing.Optional[jsii.Number] = None,
        data_storage_size_in_tbs: typing.Optional[jsii.Number] = None,
        db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
        domain: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_size_in_gbs: typing.Optional[jsii.Number] = None,
        scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
        scan_listener_port_tcp_ssl: typing.Optional[jsii.Number] = None,
        sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OracleCloudVmClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        zone_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster azurerm_oracle_cloud_vm_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cloud_exadata_infrastructure_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#cloud_exadata_infrastructure_id OracleCloudVmCluster#cloud_exadata_infrastructure_id}.
        :param cpu_core_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#cpu_core_count OracleCloudVmCluster#cpu_core_count}.
        :param db_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#db_servers OracleCloudVmCluster#db_servers}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#display_name OracleCloudVmCluster#display_name}.
        :param gi_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#gi_version OracleCloudVmCluster#gi_version}.
        :param hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#hostname OracleCloudVmCluster#hostname}.
        :param license_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#license_model OracleCloudVmCluster#license_model}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#location OracleCloudVmCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#name OracleCloudVmCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#resource_group_name OracleCloudVmCluster#resource_group_name}.
        :param ssh_public_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#ssh_public_keys OracleCloudVmCluster#ssh_public_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#subnet_id OracleCloudVmCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#virtual_network_id OracleCloudVmCluster#virtual_network_id}.
        :param backup_subnet_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#backup_subnet_cidr OracleCloudVmCluster#backup_subnet_cidr}.
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#cluster_name OracleCloudVmCluster#cluster_name}.
        :param data_collection_options: data_collection_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#data_collection_options OracleCloudVmCluster#data_collection_options}
        :param data_storage_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#data_storage_percentage OracleCloudVmCluster#data_storage_percentage}.
        :param data_storage_size_in_tbs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#data_storage_size_in_tbs OracleCloudVmCluster#data_storage_size_in_tbs}.
        :param db_node_storage_size_in_gbs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#db_node_storage_size_in_gbs OracleCloudVmCluster#db_node_storage_size_in_gbs}.
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#domain OracleCloudVmCluster#domain}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#id OracleCloudVmCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#local_backup_enabled OracleCloudVmCluster#local_backup_enabled}.
        :param memory_size_in_gbs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#memory_size_in_gbs OracleCloudVmCluster#memory_size_in_gbs}.
        :param scan_listener_port_tcp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#scan_listener_port_tcp OracleCloudVmCluster#scan_listener_port_tcp}.
        :param scan_listener_port_tcp_ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#scan_listener_port_tcp_ssl OracleCloudVmCluster#scan_listener_port_tcp_ssl}.
        :param sparse_diskgroup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#sparse_diskgroup_enabled OracleCloudVmCluster#sparse_diskgroup_enabled}.
        :param system_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#system_version OracleCloudVmCluster#system_version}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#tags OracleCloudVmCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#timeouts OracleCloudVmCluster#timeouts}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#time_zone OracleCloudVmCluster#time_zone}.
        :param zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#zone_id OracleCloudVmCluster#zone_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96736d2431d534b764ff103f5db5693b40a88a3d50bca6b7d0ef13b3d0d232db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OracleCloudVmClusterConfig(
            cloud_exadata_infrastructure_id=cloud_exadata_infrastructure_id,
            cpu_core_count=cpu_core_count,
            db_servers=db_servers,
            display_name=display_name,
            gi_version=gi_version,
            hostname=hostname,
            license_model=license_model,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            ssh_public_keys=ssh_public_keys,
            subnet_id=subnet_id,
            virtual_network_id=virtual_network_id,
            backup_subnet_cidr=backup_subnet_cidr,
            cluster_name=cluster_name,
            data_collection_options=data_collection_options,
            data_storage_percentage=data_storage_percentage,
            data_storage_size_in_tbs=data_storage_size_in_tbs,
            db_node_storage_size_in_gbs=db_node_storage_size_in_gbs,
            domain=domain,
            id=id,
            local_backup_enabled=local_backup_enabled,
            memory_size_in_gbs=memory_size_in_gbs,
            scan_listener_port_tcp=scan_listener_port_tcp,
            scan_listener_port_tcp_ssl=scan_listener_port_tcp_ssl,
            sparse_diskgroup_enabled=sparse_diskgroup_enabled,
            system_version=system_version,
            tags=tags,
            timeouts=timeouts,
            time_zone=time_zone,
            zone_id=zone_id,
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
        '''Generates CDKTF code for importing a OracleCloudVmCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OracleCloudVmCluster to import.
        :param import_from_id: The id of the existing OracleCloudVmCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OracleCloudVmCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208d15e90d73ffb3076054c195c346dd1b6ccd7a90cb10e320b795e3084089c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataCollectionOptions")
    def put_data_collection_options(
        self,
        *,
        diagnostics_events_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        health_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        incident_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param diagnostics_events_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#diagnostics_events_enabled OracleCloudVmCluster#diagnostics_events_enabled}.
        :param health_monitoring_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#health_monitoring_enabled OracleCloudVmCluster#health_monitoring_enabled}.
        :param incident_logs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#incident_logs_enabled OracleCloudVmCluster#incident_logs_enabled}.
        '''
        value = OracleCloudVmClusterDataCollectionOptions(
            diagnostics_events_enabled=diagnostics_events_enabled,
            health_monitoring_enabled=health_monitoring_enabled,
            incident_logs_enabled=incident_logs_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putDataCollectionOptions", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#create OracleCloudVmCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#delete OracleCloudVmCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#read OracleCloudVmCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#update OracleCloudVmCluster#update}.
        '''
        value = OracleCloudVmClusterTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBackupSubnetCidr")
    def reset_backup_subnet_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupSubnetCidr", []))

    @jsii.member(jsii_name="resetClusterName")
    def reset_cluster_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterName", []))

    @jsii.member(jsii_name="resetDataCollectionOptions")
    def reset_data_collection_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCollectionOptions", []))

    @jsii.member(jsii_name="resetDataStoragePercentage")
    def reset_data_storage_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStoragePercentage", []))

    @jsii.member(jsii_name="resetDataStorageSizeInTbs")
    def reset_data_storage_size_in_tbs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStorageSizeInTbs", []))

    @jsii.member(jsii_name="resetDbNodeStorageSizeInGbs")
    def reset_db_node_storage_size_in_gbs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbNodeStorageSizeInGbs", []))

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocalBackupEnabled")
    def reset_local_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalBackupEnabled", []))

    @jsii.member(jsii_name="resetMemorySizeInGbs")
    def reset_memory_size_in_gbs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemorySizeInGbs", []))

    @jsii.member(jsii_name="resetScanListenerPortTcp")
    def reset_scan_listener_port_tcp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanListenerPortTcp", []))

    @jsii.member(jsii_name="resetScanListenerPortTcpSsl")
    def reset_scan_listener_port_tcp_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanListenerPortTcpSsl", []))

    @jsii.member(jsii_name="resetSparseDiskgroupEnabled")
    def reset_sparse_diskgroup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparseDiskgroupEnabled", []))

    @jsii.member(jsii_name="resetSystemVersion")
    def reset_system_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemVersion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @jsii.member(jsii_name="resetZoneId")
    def reset_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneId", []))

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
    @jsii.member(jsii_name="dataCollectionOptions")
    def data_collection_options(
        self,
    ) -> "OracleCloudVmClusterDataCollectionOptionsOutputReference":
        return typing.cast("OracleCloudVmClusterDataCollectionOptionsOutputReference", jsii.get(self, "dataCollectionOptions"))

    @builtins.property
    @jsii.member(jsii_name="hostnameActual")
    def hostname_actual(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostnameActual"))

    @builtins.property
    @jsii.member(jsii_name="ocid")
    def ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ocid"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OracleCloudVmClusterTimeoutsOutputReference":
        return typing.cast("OracleCloudVmClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backupSubnetCidrInput")
    def backup_subnet_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupSubnetCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureIdInput")
    def cloud_exadata_infrastructure_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudExadataInfrastructureIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCoreCountInput")
    def cpu_core_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuCoreCountInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCollectionOptionsInput")
    def data_collection_options_input(
        self,
    ) -> typing.Optional["OracleCloudVmClusterDataCollectionOptions"]:
        return typing.cast(typing.Optional["OracleCloudVmClusterDataCollectionOptions"], jsii.get(self, "dataCollectionOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStoragePercentageInput")
    def data_storage_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataStoragePercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeInTbsInput")
    def data_storage_size_in_tbs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataStorageSizeInTbsInput"))

    @builtins.property
    @jsii.member(jsii_name="dbNodeStorageSizeInGbsInput")
    def db_node_storage_size_in_gbs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dbNodeStorageSizeInGbsInput"))

    @builtins.property
    @jsii.member(jsii_name="dbServersInput")
    def db_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dbServersInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="giVersionInput")
    def gi_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "giVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseModelInput")
    def license_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseModelInput"))

    @builtins.property
    @jsii.member(jsii_name="localBackupEnabledInput")
    def local_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeInGbsInput")
    def memory_size_in_gbs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeInGbsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTcpInput")
    def scan_listener_port_tcp_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scanListenerPortTcpInput"))

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTcpSslInput")
    def scan_listener_port_tcp_ssl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scanListenerPortTcpSslInput"))

    @builtins.property
    @jsii.member(jsii_name="sparseDiskgroupEnabledInput")
    def sparse_diskgroup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sparseDiskgroupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeysInput")
    def ssh_public_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshPublicKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="systemVersionInput")
    def system_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OracleCloudVmClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OracleCloudVmClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="backupSubnetCidr")
    def backup_subnet_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupSubnetCidr"))

    @backup_subnet_cidr.setter
    def backup_subnet_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9cc31c2d2b180e50d67b935edb748df463d09703413754501b5b04fb4146a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupSubnetCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureId")
    def cloud_exadata_infrastructure_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudExadataInfrastructureId"))

    @cloud_exadata_infrastructure_id.setter
    def cloud_exadata_infrastructure_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77e80a7db1b505dbee8051d9f71eb87fc0e403af19dac22d9f0fe0e0ce342e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudExadataInfrastructureId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c3df93d92e2a6bcf40db0e23abb989a9b328bc9f189c2716b49b0789817e7ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCoreCount")
    def cpu_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCoreCount"))

    @cpu_core_count.setter
    def cpu_core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432c95f7110cbaa6c79f53010093b7772499796e835e12ed5e6ac8633b35a65b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStoragePercentage")
    def data_storage_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStoragePercentage"))

    @data_storage_percentage.setter
    def data_storage_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dbcf2c7e01594ff3cfc459417fdaaaac0fe949633de2968bf6f80f9c7845aa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoragePercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeInTbs")
    def data_storage_size_in_tbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeInTbs"))

    @data_storage_size_in_tbs.setter
    def data_storage_size_in_tbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39bb248fe34c6f63e55be43fbfdf0ec80ef51aef59c94b3a1e76431e3cb2432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStorageSizeInTbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbNodeStorageSizeInGbs")
    def db_node_storage_size_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dbNodeStorageSizeInGbs"))

    @db_node_storage_size_in_gbs.setter
    def db_node_storage_size_in_gbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d48052babb336291fef3f2aeef5914c5c41ef10b85ad06822879a7580070d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbNodeStorageSizeInGbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbServers")
    def db_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dbServers"))

    @db_servers.setter
    def db_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a90c348755b74223613eacc46c254e05909844b582bfc00b3d9ad5b1c5ed3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a89f285600fa34e281077dea1a4fd4c6e49f001e9e1f9a80fa0b42d269bcf17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe44d564a58c6aa132cd15246593ae520419d42cd57e455d7a73f912a011da13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="giVersion")
    def gi_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "giVersion"))

    @gi_version.setter
    def gi_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e4e811fb85c7727db8366ffaabae345a98c1eaa701de826edb6a0aef58922da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "giVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556d995ecca9181393d4571a398ef851a9ae394c397e648f7b9ae1e4f41cb4ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa16fe9edcf3f319543045c5d713be03af6decb3fab49a20399d23c47507589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseModel")
    def license_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseModel"))

    @license_model.setter
    def license_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__399fa76d2fe8f99feec362a3109f706bba63de8cda32d0415057e66b9ef38e6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localBackupEnabled")
    def local_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "localBackupEnabled"))

    @local_backup_enabled.setter
    def local_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d470fb6469fc58e5afc18e209d6fd9362306fc5ad903f9feac4414676690c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localBackupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23cbc0a1eea2208d2d5d4a70d90b4f9df1d833dec1655dd5a6f31aeef8e4902c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySizeInGbs")
    def memory_size_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeInGbs"))

    @memory_size_in_gbs.setter
    def memory_size_in_gbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83484e56de0e9eda783039e5c33a7d7d9f4035f7e40c6335dff596b24e8bbac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySizeInGbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2690db483264000c8c319da642400548195196cf1313a294777bf802cc53cf97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c898f9f52086a2a96c40de367d735995f1eed36c7a6c9d90aebe0c2c149929b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTcp")
    def scan_listener_port_tcp(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scanListenerPortTcp"))

    @scan_listener_port_tcp.setter
    def scan_listener_port_tcp(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a38540e23c76ff7753b0ce3214557884c7f4903f11d6add534430362ad7a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanListenerPortTcp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTcpSsl")
    def scan_listener_port_tcp_ssl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scanListenerPortTcpSsl"))

    @scan_listener_port_tcp_ssl.setter
    def scan_listener_port_tcp_ssl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62fffb230cedc24d0c1a1a10f967cc2c88adc3accd9c93b5c590bd2041cf5937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanListenerPortTcpSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparseDiskgroupEnabled")
    def sparse_diskgroup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sparseDiskgroupEnabled"))

    @sparse_diskgroup_enabled.setter
    def sparse_diskgroup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d81eaea341136c3956039b816aae9a5149f2387b373e180a5cac7aa07a82516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparseDiskgroupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeys")
    def ssh_public_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshPublicKeys"))

    @ssh_public_keys.setter
    def ssh_public_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52db57997dde6614057f14787ea36e63d5e83f6af656c6a6d8f2b965bd55a181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d571d05c07f324a8e0ebbe759c461af56f5a8a272533ecfca43b9fab13756a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemVersion")
    def system_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemVersion"))

    @system_version.setter
    def system_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b30e8cfe991c56265f40e3ee0e35892b5ab3e30ecc1af178384ac3398bc6dfc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1743f43f1e1118a38364a9e1e18556317f9c458db2094215b36af433f416568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcfe286cbd8ae44d3ff67ed48b90a0e52e648f5d87bb847a51862d6df7d97b7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2821433a7870e8e4d9afed9bff7f7899026f822c01ea5d9f8f2f4390bfcd11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8063dc9002a3368a04ecb48547a3f715e21615d8dbee6198b75752abe61d261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.oracleCloudVmCluster.OracleCloudVmClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cloud_exadata_infrastructure_id": "cloudExadataInfrastructureId",
        "cpu_core_count": "cpuCoreCount",
        "db_servers": "dbServers",
        "display_name": "displayName",
        "gi_version": "giVersion",
        "hostname": "hostname",
        "license_model": "licenseModel",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "ssh_public_keys": "sshPublicKeys",
        "subnet_id": "subnetId",
        "virtual_network_id": "virtualNetworkId",
        "backup_subnet_cidr": "backupSubnetCidr",
        "cluster_name": "clusterName",
        "data_collection_options": "dataCollectionOptions",
        "data_storage_percentage": "dataStoragePercentage",
        "data_storage_size_in_tbs": "dataStorageSizeInTbs",
        "db_node_storage_size_in_gbs": "dbNodeStorageSizeInGbs",
        "domain": "domain",
        "id": "id",
        "local_backup_enabled": "localBackupEnabled",
        "memory_size_in_gbs": "memorySizeInGbs",
        "scan_listener_port_tcp": "scanListenerPortTcp",
        "scan_listener_port_tcp_ssl": "scanListenerPortTcpSsl",
        "sparse_diskgroup_enabled": "sparseDiskgroupEnabled",
        "system_version": "systemVersion",
        "tags": "tags",
        "timeouts": "timeouts",
        "time_zone": "timeZone",
        "zone_id": "zoneId",
    },
)
class OracleCloudVmClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cloud_exadata_infrastructure_id: builtins.str,
        cpu_core_count: jsii.Number,
        db_servers: typing.Sequence[builtins.str],
        display_name: builtins.str,
        gi_version: builtins.str,
        hostname: builtins.str,
        license_model: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        ssh_public_keys: typing.Sequence[builtins.str],
        subnet_id: builtins.str,
        virtual_network_id: builtins.str,
        backup_subnet_cidr: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        data_collection_options: typing.Optional[typing.Union["OracleCloudVmClusterDataCollectionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        data_storage_percentage: typing.Optional[jsii.Number] = None,
        data_storage_size_in_tbs: typing.Optional[jsii.Number] = None,
        db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
        domain: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_size_in_gbs: typing.Optional[jsii.Number] = None,
        scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
        scan_listener_port_tcp_ssl: typing.Optional[jsii.Number] = None,
        sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OracleCloudVmClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cloud_exadata_infrastructure_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#cloud_exadata_infrastructure_id OracleCloudVmCluster#cloud_exadata_infrastructure_id}.
        :param cpu_core_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#cpu_core_count OracleCloudVmCluster#cpu_core_count}.
        :param db_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#db_servers OracleCloudVmCluster#db_servers}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#display_name OracleCloudVmCluster#display_name}.
        :param gi_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#gi_version OracleCloudVmCluster#gi_version}.
        :param hostname: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#hostname OracleCloudVmCluster#hostname}.
        :param license_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#license_model OracleCloudVmCluster#license_model}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#location OracleCloudVmCluster#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#name OracleCloudVmCluster#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#resource_group_name OracleCloudVmCluster#resource_group_name}.
        :param ssh_public_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#ssh_public_keys OracleCloudVmCluster#ssh_public_keys}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#subnet_id OracleCloudVmCluster#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#virtual_network_id OracleCloudVmCluster#virtual_network_id}.
        :param backup_subnet_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#backup_subnet_cidr OracleCloudVmCluster#backup_subnet_cidr}.
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#cluster_name OracleCloudVmCluster#cluster_name}.
        :param data_collection_options: data_collection_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#data_collection_options OracleCloudVmCluster#data_collection_options}
        :param data_storage_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#data_storage_percentage OracleCloudVmCluster#data_storage_percentage}.
        :param data_storage_size_in_tbs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#data_storage_size_in_tbs OracleCloudVmCluster#data_storage_size_in_tbs}.
        :param db_node_storage_size_in_gbs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#db_node_storage_size_in_gbs OracleCloudVmCluster#db_node_storage_size_in_gbs}.
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#domain OracleCloudVmCluster#domain}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#id OracleCloudVmCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#local_backup_enabled OracleCloudVmCluster#local_backup_enabled}.
        :param memory_size_in_gbs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#memory_size_in_gbs OracleCloudVmCluster#memory_size_in_gbs}.
        :param scan_listener_port_tcp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#scan_listener_port_tcp OracleCloudVmCluster#scan_listener_port_tcp}.
        :param scan_listener_port_tcp_ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#scan_listener_port_tcp_ssl OracleCloudVmCluster#scan_listener_port_tcp_ssl}.
        :param sparse_diskgroup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#sparse_diskgroup_enabled OracleCloudVmCluster#sparse_diskgroup_enabled}.
        :param system_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#system_version OracleCloudVmCluster#system_version}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#tags OracleCloudVmCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#timeouts OracleCloudVmCluster#timeouts}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#time_zone OracleCloudVmCluster#time_zone}.
        :param zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#zone_id OracleCloudVmCluster#zone_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_collection_options, dict):
            data_collection_options = OracleCloudVmClusterDataCollectionOptions(**data_collection_options)
        if isinstance(timeouts, dict):
            timeouts = OracleCloudVmClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5afea60291ddfc5ea058db2aded4b91c6722ed43b60f9e074287d0b86986ced0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cloud_exadata_infrastructure_id", value=cloud_exadata_infrastructure_id, expected_type=type_hints["cloud_exadata_infrastructure_id"])
            check_type(argname="argument cpu_core_count", value=cpu_core_count, expected_type=type_hints["cpu_core_count"])
            check_type(argname="argument db_servers", value=db_servers, expected_type=type_hints["db_servers"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gi_version", value=gi_version, expected_type=type_hints["gi_version"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument license_model", value=license_model, expected_type=type_hints["license_model"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument ssh_public_keys", value=ssh_public_keys, expected_type=type_hints["ssh_public_keys"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
            check_type(argname="argument backup_subnet_cidr", value=backup_subnet_cidr, expected_type=type_hints["backup_subnet_cidr"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument data_collection_options", value=data_collection_options, expected_type=type_hints["data_collection_options"])
            check_type(argname="argument data_storage_percentage", value=data_storage_percentage, expected_type=type_hints["data_storage_percentage"])
            check_type(argname="argument data_storage_size_in_tbs", value=data_storage_size_in_tbs, expected_type=type_hints["data_storage_size_in_tbs"])
            check_type(argname="argument db_node_storage_size_in_gbs", value=db_node_storage_size_in_gbs, expected_type=type_hints["db_node_storage_size_in_gbs"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument local_backup_enabled", value=local_backup_enabled, expected_type=type_hints["local_backup_enabled"])
            check_type(argname="argument memory_size_in_gbs", value=memory_size_in_gbs, expected_type=type_hints["memory_size_in_gbs"])
            check_type(argname="argument scan_listener_port_tcp", value=scan_listener_port_tcp, expected_type=type_hints["scan_listener_port_tcp"])
            check_type(argname="argument scan_listener_port_tcp_ssl", value=scan_listener_port_tcp_ssl, expected_type=type_hints["scan_listener_port_tcp_ssl"])
            check_type(argname="argument sparse_diskgroup_enabled", value=sparse_diskgroup_enabled, expected_type=type_hints["sparse_diskgroup_enabled"])
            check_type(argname="argument system_version", value=system_version, expected_type=type_hints["system_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_exadata_infrastructure_id": cloud_exadata_infrastructure_id,
            "cpu_core_count": cpu_core_count,
            "db_servers": db_servers,
            "display_name": display_name,
            "gi_version": gi_version,
            "hostname": hostname,
            "license_model": license_model,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "ssh_public_keys": ssh_public_keys,
            "subnet_id": subnet_id,
            "virtual_network_id": virtual_network_id,
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
        if backup_subnet_cidr is not None:
            self._values["backup_subnet_cidr"] = backup_subnet_cidr
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if data_collection_options is not None:
            self._values["data_collection_options"] = data_collection_options
        if data_storage_percentage is not None:
            self._values["data_storage_percentage"] = data_storage_percentage
        if data_storage_size_in_tbs is not None:
            self._values["data_storage_size_in_tbs"] = data_storage_size_in_tbs
        if db_node_storage_size_in_gbs is not None:
            self._values["db_node_storage_size_in_gbs"] = db_node_storage_size_in_gbs
        if domain is not None:
            self._values["domain"] = domain
        if id is not None:
            self._values["id"] = id
        if local_backup_enabled is not None:
            self._values["local_backup_enabled"] = local_backup_enabled
        if memory_size_in_gbs is not None:
            self._values["memory_size_in_gbs"] = memory_size_in_gbs
        if scan_listener_port_tcp is not None:
            self._values["scan_listener_port_tcp"] = scan_listener_port_tcp
        if scan_listener_port_tcp_ssl is not None:
            self._values["scan_listener_port_tcp_ssl"] = scan_listener_port_tcp_ssl
        if sparse_diskgroup_enabled is not None:
            self._values["sparse_diskgroup_enabled"] = sparse_diskgroup_enabled
        if system_version is not None:
            self._values["system_version"] = system_version
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if time_zone is not None:
            self._values["time_zone"] = time_zone
        if zone_id is not None:
            self._values["zone_id"] = zone_id

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
    def cloud_exadata_infrastructure_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#cloud_exadata_infrastructure_id OracleCloudVmCluster#cloud_exadata_infrastructure_id}.'''
        result = self._values.get("cloud_exadata_infrastructure_id")
        assert result is not None, "Required property 'cloud_exadata_infrastructure_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cpu_core_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#cpu_core_count OracleCloudVmCluster#cpu_core_count}.'''
        result = self._values.get("cpu_core_count")
        assert result is not None, "Required property 'cpu_core_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def db_servers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#db_servers OracleCloudVmCluster#db_servers}.'''
        result = self._values.get("db_servers")
        assert result is not None, "Required property 'db_servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#display_name OracleCloudVmCluster#display_name}.'''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gi_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#gi_version OracleCloudVmCluster#gi_version}.'''
        result = self._values.get("gi_version")
        assert result is not None, "Required property 'gi_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#hostname OracleCloudVmCluster#hostname}.'''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def license_model(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#license_model OracleCloudVmCluster#license_model}.'''
        result = self._values.get("license_model")
        assert result is not None, "Required property 'license_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#location OracleCloudVmCluster#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#name OracleCloudVmCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#resource_group_name OracleCloudVmCluster#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_public_keys(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#ssh_public_keys OracleCloudVmCluster#ssh_public_keys}.'''
        result = self._values.get("ssh_public_keys")
        assert result is not None, "Required property 'ssh_public_keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#subnet_id OracleCloudVmCluster#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#virtual_network_id OracleCloudVmCluster#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        assert result is not None, "Required property 'virtual_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_subnet_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#backup_subnet_cidr OracleCloudVmCluster#backup_subnet_cidr}.'''
        result = self._values.get("backup_subnet_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#cluster_name OracleCloudVmCluster#cluster_name}.'''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_collection_options(
        self,
    ) -> typing.Optional["OracleCloudVmClusterDataCollectionOptions"]:
        '''data_collection_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#data_collection_options OracleCloudVmCluster#data_collection_options}
        '''
        result = self._values.get("data_collection_options")
        return typing.cast(typing.Optional["OracleCloudVmClusterDataCollectionOptions"], result)

    @builtins.property
    def data_storage_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#data_storage_percentage OracleCloudVmCluster#data_storage_percentage}.'''
        result = self._values.get("data_storage_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_storage_size_in_tbs(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#data_storage_size_in_tbs OracleCloudVmCluster#data_storage_size_in_tbs}.'''
        result = self._values.get("data_storage_size_in_tbs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_node_storage_size_in_gbs(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#db_node_storage_size_in_gbs OracleCloudVmCluster#db_node_storage_size_in_gbs}.'''
        result = self._values.get("db_node_storage_size_in_gbs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#domain OracleCloudVmCluster#domain}.'''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#id OracleCloudVmCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#local_backup_enabled OracleCloudVmCluster#local_backup_enabled}.'''
        result = self._values.get("local_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def memory_size_in_gbs(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#memory_size_in_gbs OracleCloudVmCluster#memory_size_in_gbs}.'''
        result = self._values.get("memory_size_in_gbs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scan_listener_port_tcp(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#scan_listener_port_tcp OracleCloudVmCluster#scan_listener_port_tcp}.'''
        result = self._values.get("scan_listener_port_tcp")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scan_listener_port_tcp_ssl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#scan_listener_port_tcp_ssl OracleCloudVmCluster#scan_listener_port_tcp_ssl}.'''
        result = self._values.get("scan_listener_port_tcp_ssl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sparse_diskgroup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#sparse_diskgroup_enabled OracleCloudVmCluster#sparse_diskgroup_enabled}.'''
        result = self._values.get("sparse_diskgroup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def system_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#system_version OracleCloudVmCluster#system_version}.'''
        result = self._values.get("system_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#tags OracleCloudVmCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OracleCloudVmClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#timeouts OracleCloudVmCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OracleCloudVmClusterTimeouts"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#time_zone OracleCloudVmCluster#time_zone}.'''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#zone_id OracleCloudVmCluster#zone_id}.'''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleCloudVmClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.oracleCloudVmCluster.OracleCloudVmClusterDataCollectionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "diagnostics_events_enabled": "diagnosticsEventsEnabled",
        "health_monitoring_enabled": "healthMonitoringEnabled",
        "incident_logs_enabled": "incidentLogsEnabled",
    },
)
class OracleCloudVmClusterDataCollectionOptions:
    def __init__(
        self,
        *,
        diagnostics_events_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        health_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        incident_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param diagnostics_events_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#diagnostics_events_enabled OracleCloudVmCluster#diagnostics_events_enabled}.
        :param health_monitoring_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#health_monitoring_enabled OracleCloudVmCluster#health_monitoring_enabled}.
        :param incident_logs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#incident_logs_enabled OracleCloudVmCluster#incident_logs_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7000adb97f2e762e8465d24a3dfa9a17facf7eafdc785b5afb92310ed7962b9e)
            check_type(argname="argument diagnostics_events_enabled", value=diagnostics_events_enabled, expected_type=type_hints["diagnostics_events_enabled"])
            check_type(argname="argument health_monitoring_enabled", value=health_monitoring_enabled, expected_type=type_hints["health_monitoring_enabled"])
            check_type(argname="argument incident_logs_enabled", value=incident_logs_enabled, expected_type=type_hints["incident_logs_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if diagnostics_events_enabled is not None:
            self._values["diagnostics_events_enabled"] = diagnostics_events_enabled
        if health_monitoring_enabled is not None:
            self._values["health_monitoring_enabled"] = health_monitoring_enabled
        if incident_logs_enabled is not None:
            self._values["incident_logs_enabled"] = incident_logs_enabled

    @builtins.property
    def diagnostics_events_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#diagnostics_events_enabled OracleCloudVmCluster#diagnostics_events_enabled}.'''
        result = self._values.get("diagnostics_events_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def health_monitoring_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#health_monitoring_enabled OracleCloudVmCluster#health_monitoring_enabled}.'''
        result = self._values.get("health_monitoring_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def incident_logs_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#incident_logs_enabled OracleCloudVmCluster#incident_logs_enabled}.'''
        result = self._values.get("incident_logs_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleCloudVmClusterDataCollectionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleCloudVmClusterDataCollectionOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.oracleCloudVmCluster.OracleCloudVmClusterDataCollectionOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__211a98138f1977cc4b890f42af349ce143b0807cd462ea5192d32f159014ac65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiagnosticsEventsEnabled")
    def reset_diagnostics_events_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiagnosticsEventsEnabled", []))

    @jsii.member(jsii_name="resetHealthMonitoringEnabled")
    def reset_health_monitoring_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthMonitoringEnabled", []))

    @jsii.member(jsii_name="resetIncidentLogsEnabled")
    def reset_incident_logs_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncidentLogsEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="diagnosticsEventsEnabledInput")
    def diagnostics_events_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "diagnosticsEventsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="healthMonitoringEnabledInput")
    def health_monitoring_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "healthMonitoringEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="incidentLogsEnabledInput")
    def incident_logs_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "incidentLogsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="diagnosticsEventsEnabled")
    def diagnostics_events_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "diagnosticsEventsEnabled"))

    @diagnostics_events_enabled.setter
    def diagnostics_events_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6e176fa6641d8e7116c3fe1afc64c9ea7fda4caedd1ffa076d09079dfbdc21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diagnosticsEventsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthMonitoringEnabled")
    def health_monitoring_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "healthMonitoringEnabled"))

    @health_monitoring_enabled.setter
    def health_monitoring_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487ea83e43f1c4765a1922f3aa5c7078e733fe3bd6cb0961149f1c1ef75a2c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthMonitoringEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="incidentLogsEnabled")
    def incident_logs_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "incidentLogsEnabled"))

    @incident_logs_enabled.setter
    def incident_logs_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26769ad54ad2403126b87f41081e8cd7548237318bb7c354ad8d9a9f7ab08803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "incidentLogsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OracleCloudVmClusterDataCollectionOptions]:
        return typing.cast(typing.Optional[OracleCloudVmClusterDataCollectionOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleCloudVmClusterDataCollectionOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b39b12b33044a97db2b8ae2814767180a21d5aa1c04146be84085da37faf01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.oracleCloudVmCluster.OracleCloudVmClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class OracleCloudVmClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#create OracleCloudVmCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#delete OracleCloudVmCluster#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#read OracleCloudVmCluster#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#update OracleCloudVmCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225b13697d7570bdbd9d4e6a781a55d2f54bf57336eb53b384e965aef7a7acb1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#create OracleCloudVmCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#delete OracleCloudVmCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#read OracleCloudVmCluster#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_cloud_vm_cluster#update OracleCloudVmCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleCloudVmClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleCloudVmClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.oracleCloudVmCluster.OracleCloudVmClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2a2b6dd0316eb1c21efd2087ca655739ece092e1c58010d2cc8e41cc60cddf8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__057277786e58a2c9c3a702ea3f29a5e49e9203dddc0fc6ede934c2ce2a334d9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b76cd25dac17e3584e2d024beb0e5686126e00016f040837894f3ed4bcbe6474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7405d6cd662cb25d990f2b9247b69f093f4676a350edf8a0f47ce6b39c0d4573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c871d140bb47d45599409376b47d25a1ca03a55f9df1580adb889fe0e98bcce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleCloudVmClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleCloudVmClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleCloudVmClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b30309e31830170953133698aa84ea3a7b37fc6ce2949401b0e09d1a5149254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OracleCloudVmCluster",
    "OracleCloudVmClusterConfig",
    "OracleCloudVmClusterDataCollectionOptions",
    "OracleCloudVmClusterDataCollectionOptionsOutputReference",
    "OracleCloudVmClusterTimeouts",
    "OracleCloudVmClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__96736d2431d534b764ff103f5db5693b40a88a3d50bca6b7d0ef13b3d0d232db(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cloud_exadata_infrastructure_id: builtins.str,
    cpu_core_count: jsii.Number,
    db_servers: typing.Sequence[builtins.str],
    display_name: builtins.str,
    gi_version: builtins.str,
    hostname: builtins.str,
    license_model: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    ssh_public_keys: typing.Sequence[builtins.str],
    subnet_id: builtins.str,
    virtual_network_id: builtins.str,
    backup_subnet_cidr: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    data_collection_options: typing.Optional[typing.Union[OracleCloudVmClusterDataCollectionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    data_storage_percentage: typing.Optional[jsii.Number] = None,
    data_storage_size_in_tbs: typing.Optional[jsii.Number] = None,
    db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
    domain: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    memory_size_in_gbs: typing.Optional[jsii.Number] = None,
    scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
    scan_listener_port_tcp_ssl: typing.Optional[jsii.Number] = None,
    sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    system_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OracleCloudVmClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    zone_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__208d15e90d73ffb3076054c195c346dd1b6ccd7a90cb10e320b795e3084089c6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9cc31c2d2b180e50d67b935edb748df463d09703413754501b5b04fb4146a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77e80a7db1b505dbee8051d9f71eb87fc0e403af19dac22d9f0fe0e0ce342e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3df93d92e2a6bcf40db0e23abb989a9b328bc9f189c2716b49b0789817e7ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432c95f7110cbaa6c79f53010093b7772499796e835e12ed5e6ac8633b35a65b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dbcf2c7e01594ff3cfc459417fdaaaac0fe949633de2968bf6f80f9c7845aa5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39bb248fe34c6f63e55be43fbfdf0ec80ef51aef59c94b3a1e76431e3cb2432(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d48052babb336291fef3f2aeef5914c5c41ef10b85ad06822879a7580070d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a90c348755b74223613eacc46c254e05909844b582bfc00b3d9ad5b1c5ed3c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a89f285600fa34e281077dea1a4fd4c6e49f001e9e1f9a80fa0b42d269bcf17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe44d564a58c6aa132cd15246593ae520419d42cd57e455d7a73f912a011da13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4e811fb85c7727db8366ffaabae345a98c1eaa701de826edb6a0aef58922da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556d995ecca9181393d4571a398ef851a9ae394c397e648f7b9ae1e4f41cb4ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa16fe9edcf3f319543045c5d713be03af6decb3fab49a20399d23c47507589(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399fa76d2fe8f99feec362a3109f706bba63de8cda32d0415057e66b9ef38e6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d470fb6469fc58e5afc18e209d6fd9362306fc5ad903f9feac4414676690c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23cbc0a1eea2208d2d5d4a70d90b4f9df1d833dec1655dd5a6f31aeef8e4902c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83484e56de0e9eda783039e5c33a7d7d9f4035f7e40c6335dff596b24e8bbac9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2690db483264000c8c319da642400548195196cf1313a294777bf802cc53cf97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c898f9f52086a2a96c40de367d735995f1eed36c7a6c9d90aebe0c2c149929b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a38540e23c76ff7753b0ce3214557884c7f4903f11d6add534430362ad7a69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62fffb230cedc24d0c1a1a10f967cc2c88adc3accd9c93b5c590bd2041cf5937(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d81eaea341136c3956039b816aae9a5149f2387b373e180a5cac7aa07a82516(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52db57997dde6614057f14787ea36e63d5e83f6af656c6a6d8f2b965bd55a181(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d571d05c07f324a8e0ebbe759c461af56f5a8a272533ecfca43b9fab13756a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30e8cfe991c56265f40e3ee0e35892b5ab3e30ecc1af178384ac3398bc6dfc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1743f43f1e1118a38364a9e1e18556317f9c458db2094215b36af433f416568(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcfe286cbd8ae44d3ff67ed48b90a0e52e648f5d87bb847a51862d6df7d97b7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2821433a7870e8e4d9afed9bff7f7899026f822c01ea5d9f8f2f4390bfcd11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8063dc9002a3368a04ecb48547a3f715e21615d8dbee6198b75752abe61d261(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afea60291ddfc5ea058db2aded4b91c6722ed43b60f9e074287d0b86986ced0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloud_exadata_infrastructure_id: builtins.str,
    cpu_core_count: jsii.Number,
    db_servers: typing.Sequence[builtins.str],
    display_name: builtins.str,
    gi_version: builtins.str,
    hostname: builtins.str,
    license_model: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    ssh_public_keys: typing.Sequence[builtins.str],
    subnet_id: builtins.str,
    virtual_network_id: builtins.str,
    backup_subnet_cidr: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    data_collection_options: typing.Optional[typing.Union[OracleCloudVmClusterDataCollectionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    data_storage_percentage: typing.Optional[jsii.Number] = None,
    data_storage_size_in_tbs: typing.Optional[jsii.Number] = None,
    db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
    domain: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    memory_size_in_gbs: typing.Optional[jsii.Number] = None,
    scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
    scan_listener_port_tcp_ssl: typing.Optional[jsii.Number] = None,
    sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    system_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OracleCloudVmClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7000adb97f2e762e8465d24a3dfa9a17facf7eafdc785b5afb92310ed7962b9e(
    *,
    diagnostics_events_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    health_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    incident_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211a98138f1977cc4b890f42af349ce143b0807cd462ea5192d32f159014ac65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6e176fa6641d8e7116c3fe1afc64c9ea7fda4caedd1ffa076d09079dfbdc21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487ea83e43f1c4765a1922f3aa5c7078e733fe3bd6cb0961149f1c1ef75a2c22(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26769ad54ad2403126b87f41081e8cd7548237318bb7c354ad8d9a9f7ab08803(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b39b12b33044a97db2b8ae2814767180a21d5aa1c04146be84085da37faf01(
    value: typing.Optional[OracleCloudVmClusterDataCollectionOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225b13697d7570bdbd9d4e6a781a55d2f54bf57336eb53b384e965aef7a7acb1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a2b6dd0316eb1c21efd2087ca655739ece092e1c58010d2cc8e41cc60cddf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057277786e58a2c9c3a702ea3f29a5e49e9203dddc0fc6ede934c2ce2a334d9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76cd25dac17e3584e2d024beb0e5686126e00016f040837894f3ed4bcbe6474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7405d6cd662cb25d990f2b9247b69f093f4676a350edf8a0f47ce6b39c0d4573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c871d140bb47d45599409376b47d25a1ca03a55f9df1580adb889fe0e98bcce6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b30309e31830170953133698aa84ea3a7b37fc6ce2949401b0e09d1a5149254(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleCloudVmClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
