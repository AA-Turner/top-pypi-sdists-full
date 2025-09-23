r'''
# `aws_odb_cloud_vm_cluster`

Refer to the Terraform Registry for docs: [`aws_odb_cloud_vm_cluster`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster).
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


class OdbCloudVmCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster aws_odb_cloud_vm_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cloud_exadata_infrastructure_id: builtins.str,
        cpu_core_count: jsii.Number,
        db_servers: typing.Sequence[builtins.str],
        display_name: builtins.str,
        gi_version: builtins.str,
        hostname_prefix: builtins.str,
        odb_network_id: builtins.str,
        ssh_public_keys: typing.Sequence[builtins.str],
        cluster_name: typing.Optional[builtins.str] = None,
        data_collection_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OdbCloudVmClusterDataCollectionOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_storage_size_in_tbs: typing.Optional[jsii.Number] = None,
        db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
        is_local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        license_model: typing.Optional[builtins.str] = None,
        memory_size_in_gbs: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OdbCloudVmClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timezone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster aws_odb_cloud_vm_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cloud_exadata_infrastructure_id: The unique identifier of the Exadata infrastructure for this VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#cloud_exadata_infrastructure_id OdbCloudVmCluster#cloud_exadata_infrastructure_id}
        :param cpu_core_count: The number of CPU cores to enable on the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#cpu_core_count OdbCloudVmCluster#cpu_core_count}
        :param db_servers: The list of database servers for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#db_servers OdbCloudVmCluster#db_servers}
        :param display_name: A user-friendly name for the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#display_name OdbCloudVmCluster#display_name}
        :param gi_version: A valid software version of Oracle Grid Infrastructure (GI). To get the list of valid values, use the ListGiVersions operation and specify the shape of the Exadata infrastructure. Example: 19.0.0.0 This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#gi_version OdbCloudVmCluster#gi_version}
        :param hostname_prefix: The host name prefix for the VM cluster. Constraints: - Can't be "localhost" or "hostname". - Can't contain "-version". - The maximum length of the combined hostname and domain is 63 characters. - The hostname must be unique within the subnet. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#hostname_prefix OdbCloudVmCluster#hostname_prefix}
        :param odb_network_id: The unique identifier of the ODB network for the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#odb_network_id OdbCloudVmCluster#odb_network_id}
        :param ssh_public_keys: The public key portion of one or more key pairs used for SSH access to the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#ssh_public_keys OdbCloudVmCluster#ssh_public_keys}
        :param cluster_name: The name of the Grid Infrastructure (GI) cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#cluster_name OdbCloudVmCluster#cluster_name}
        :param data_collection_options: data_collection_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#data_collection_options OdbCloudVmCluster#data_collection_options}
        :param data_storage_size_in_tbs: The size of the data disk group, in terabytes (TBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#data_storage_size_in_tbs OdbCloudVmCluster#data_storage_size_in_tbs}
        :param db_node_storage_size_in_gbs: The amount of local node storage, in gigabytes (GBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#db_node_storage_size_in_gbs OdbCloudVmCluster#db_node_storage_size_in_gbs}
        :param is_local_backup_enabled: Specifies whether to enable database backups to local Exadata storage for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_local_backup_enabled OdbCloudVmCluster#is_local_backup_enabled}
        :param is_sparse_diskgroup_enabled: Specifies whether to create a sparse disk group for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_sparse_diskgroup_enabled OdbCloudVmCluster#is_sparse_diskgroup_enabled}
        :param license_model: The Oracle license model to apply to the VM cluster. Default: LICENSE_INCLUDED. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#license_model OdbCloudVmCluster#license_model}
        :param memory_size_in_gbs: The amount of memory, in gigabytes (GBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#memory_size_in_gbs OdbCloudVmCluster#memory_size_in_gbs}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#region OdbCloudVmCluster#region}
        :param scan_listener_port_tcp: The port number for TCP connections to the single client access name (SCAN) listener. Valid values: 1024–8999 with the following exceptions: 2484 , 6100 , 6200 , 7060, 7070 , 7085 , and 7879Default: 1521. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#scan_listener_port_tcp OdbCloudVmCluster#scan_listener_port_tcp}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#tags OdbCloudVmCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#timeouts OdbCloudVmCluster#timeouts}
        :param timezone: The configured time zone of the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#timezone OdbCloudVmCluster#timezone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3156d1e4c43f388bd424347deed81dcca3cb8d60639def831efc4045b6aca277)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = OdbCloudVmClusterConfig(
            cloud_exadata_infrastructure_id=cloud_exadata_infrastructure_id,
            cpu_core_count=cpu_core_count,
            db_servers=db_servers,
            display_name=display_name,
            gi_version=gi_version,
            hostname_prefix=hostname_prefix,
            odb_network_id=odb_network_id,
            ssh_public_keys=ssh_public_keys,
            cluster_name=cluster_name,
            data_collection_options=data_collection_options,
            data_storage_size_in_tbs=data_storage_size_in_tbs,
            db_node_storage_size_in_gbs=db_node_storage_size_in_gbs,
            is_local_backup_enabled=is_local_backup_enabled,
            is_sparse_diskgroup_enabled=is_sparse_diskgroup_enabled,
            license_model=license_model,
            memory_size_in_gbs=memory_size_in_gbs,
            region=region,
            scan_listener_port_tcp=scan_listener_port_tcp,
            tags=tags,
            timeouts=timeouts,
            timezone=timezone,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a OdbCloudVmCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OdbCloudVmCluster to import.
        :param import_from_id: The id of the existing OdbCloudVmCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OdbCloudVmCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3969eebc3486e30d57be28df60b81c0659306facd9507d2ed34eee65bc7672)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataCollectionOptions")
    def put_data_collection_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OdbCloudVmClusterDataCollectionOptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bacc3febd98b0c59606f4e69a551ebc77587987e0e47b013f1539094a2c21e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataCollectionOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#create OdbCloudVmCluster#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#delete OdbCloudVmCluster#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#update OdbCloudVmCluster#update}
        '''
        value = OdbCloudVmClusterTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetClusterName")
    def reset_cluster_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterName", []))

    @jsii.member(jsii_name="resetDataCollectionOptions")
    def reset_data_collection_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCollectionOptions", []))

    @jsii.member(jsii_name="resetDataStorageSizeInTbs")
    def reset_data_storage_size_in_tbs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStorageSizeInTbs", []))

    @jsii.member(jsii_name="resetDbNodeStorageSizeInGbs")
    def reset_db_node_storage_size_in_gbs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbNodeStorageSizeInGbs", []))

    @jsii.member(jsii_name="resetIsLocalBackupEnabled")
    def reset_is_local_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsLocalBackupEnabled", []))

    @jsii.member(jsii_name="resetIsSparseDiskgroupEnabled")
    def reset_is_sparse_diskgroup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSparseDiskgroupEnabled", []))

    @jsii.member(jsii_name="resetLicenseModel")
    def reset_license_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseModel", []))

    @jsii.member(jsii_name="resetMemorySizeInGbs")
    def reset_memory_size_in_gbs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemorySizeInGbs", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScanListenerPortTcp")
    def reset_scan_listener_port_tcp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanListenerPortTcp", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="computeModel")
    def compute_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeModel"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="dataCollectionOptions")
    def data_collection_options(self) -> "OdbCloudVmClusterDataCollectionOptionsList":
        return typing.cast("OdbCloudVmClusterDataCollectionOptionsList", jsii.get(self, "dataCollectionOptions"))

    @builtins.property
    @jsii.member(jsii_name="diskRedundancy")
    def disk_redundancy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskRedundancy"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="hostnamePrefixComputed")
    def hostname_prefix_computed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostnamePrefixComputed"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="iormConfigCache")
    def iorm_config_cache(self) -> "OdbCloudVmClusterIormConfigCacheList":
        return typing.cast("OdbCloudVmClusterIormConfigCacheList", jsii.get(self, "iormConfigCache"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdateHistoryEntryId")
    def last_update_history_entry_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdateHistoryEntryId"))

    @builtins.property
    @jsii.member(jsii_name="listenerPort")
    def listener_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "listenerPort"))

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @builtins.property
    @jsii.member(jsii_name="ocid")
    def ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ocid"))

    @builtins.property
    @jsii.member(jsii_name="ociResourceAnchorName")
    def oci_resource_anchor_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociResourceAnchorName"))

    @builtins.property
    @jsii.member(jsii_name="ociUrl")
    def oci_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociUrl"))

    @builtins.property
    @jsii.member(jsii_name="percentProgress")
    def percent_progress(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentProgress"))

    @builtins.property
    @jsii.member(jsii_name="scanDnsName")
    def scan_dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scanDnsName"))

    @builtins.property
    @jsii.member(jsii_name="scanDnsRecordId")
    def scan_dns_record_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scanDnsRecordId"))

    @builtins.property
    @jsii.member(jsii_name="scanIpIds")
    def scan_ip_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scanIpIds"))

    @builtins.property
    @jsii.member(jsii_name="shape")
    def shape(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shape"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="statusReason")
    def status_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusReason"))

    @builtins.property
    @jsii.member(jsii_name="storageSizeInGbs")
    def storage_size_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageSizeInGbs"))

    @builtins.property
    @jsii.member(jsii_name="systemVersion")
    def system_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemVersion"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OdbCloudVmClusterTimeoutsOutputReference":
        return typing.cast("OdbCloudVmClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vipIds")
    def vip_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vipIds"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudVmClusterDataCollectionOptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudVmClusterDataCollectionOptions"]]], jsii.get(self, "dataCollectionOptionsInput"))

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
    @jsii.member(jsii_name="giVersionInput")
    def gi_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "giVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnamePrefixInput")
    def hostname_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="isLocalBackupEnabledInput")
    def is_local_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isLocalBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isSparseDiskgroupEnabledInput")
    def is_sparse_diskgroup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSparseDiskgroupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseModelInput")
    def license_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseModelInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeInGbsInput")
    def memory_size_in_gbs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeInGbsInput"))

    @builtins.property
    @jsii.member(jsii_name="odbNetworkIdInput")
    def odb_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "odbNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTcpInput")
    def scan_listener_port_tcp_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scanListenerPortTcpInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeysInput")
    def ssh_public_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshPublicKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OdbCloudVmClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OdbCloudVmClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureId")
    def cloud_exadata_infrastructure_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudExadataInfrastructureId"))

    @cloud_exadata_infrastructure_id.setter
    def cloud_exadata_infrastructure_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253fd06e06f5e28be7ef7af1365b308cf3467a6a935a2b27d02c53d6df278a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudExadataInfrastructureId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a59d10809c3b8f0588f012f5812437fcc277c43abb0d2338e492eacf5151d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCoreCount")
    def cpu_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCoreCount"))

    @cpu_core_count.setter
    def cpu_core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1529a4625063e97ae38954934ecc56dd93ff92e36201ddaf3f929c251aeac4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeInTbs")
    def data_storage_size_in_tbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeInTbs"))

    @data_storage_size_in_tbs.setter
    def data_storage_size_in_tbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0eb3b3dd5000bff6dabcd088dab560fafbfa424c2c88f5baee2abe3b7d76e53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStorageSizeInTbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbNodeStorageSizeInGbs")
    def db_node_storage_size_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dbNodeStorageSizeInGbs"))

    @db_node_storage_size_in_gbs.setter
    def db_node_storage_size_in_gbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d629faa0102bd37dde97228f234ee3804554528e87742427ec5241b9b782a5c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbNodeStorageSizeInGbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbServers")
    def db_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dbServers"))

    @db_servers.setter
    def db_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa6bbe892741331de56b988436aede0451fc8f4a60821b4b9ff4f44468d6ad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f917d93a2399a6235306319d1c964019b76bfced25bfb703d24ed01336c1b0e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="giVersion")
    def gi_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "giVersion"))

    @gi_version.setter
    def gi_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a10cd06fafe79714d30b8c30f03022c62c450015d04184d47d7ece799121b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "giVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostnamePrefix")
    def hostname_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostnamePrefix"))

    @hostname_prefix.setter
    def hostname_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f214a2eb5ec9c335ef8fbbd1998be9fc649785241aa19617e2add4c5530048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostnamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isLocalBackupEnabled")
    def is_local_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isLocalBackupEnabled"))

    @is_local_backup_enabled.setter
    def is_local_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744002c74526aa046724f4f85618f5270897867a78b1428fc197aa3d372138cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isLocalBackupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSparseDiskgroupEnabled")
    def is_sparse_diskgroup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSparseDiskgroupEnabled"))

    @is_sparse_diskgroup_enabled.setter
    def is_sparse_diskgroup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b67b4a4954be02a42e2a2a372685189256ced6bb87dfe49d05e463469c30434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSparseDiskgroupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseModel")
    def license_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseModel"))

    @license_model.setter
    def license_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c58f8aef9f53001de3d4c1b63e480b6657cf7a0ff8bdc923fa855613127e051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySizeInGbs")
    def memory_size_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeInGbs"))

    @memory_size_in_gbs.setter
    def memory_size_in_gbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a82812d39c59ddcf8b91812c9a40a0e02add53d66c99d849789a58408c24b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySizeInGbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="odbNetworkId")
    def odb_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "odbNetworkId"))

    @odb_network_id.setter
    def odb_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b63f6cb9d225d739cd9f5da619bb46af7b6d4dd9c13dc5fa3e84a3c3fd3a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "odbNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a2f3ea7444e60d49a3875e4e31f6623202f2c5cfdc7d1d7ca4f240511bbfd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTcp")
    def scan_listener_port_tcp(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scanListenerPortTcp"))

    @scan_listener_port_tcp.setter
    def scan_listener_port_tcp(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11f1d371ee5d9651845d83496667c670fc980ccc19b0b31432402e787d28a94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanListenerPortTcp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeys")
    def ssh_public_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshPublicKeys"))

    @ssh_public_keys.setter
    def ssh_public_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe60c5a7fc05b3576d0abd218c25106864fcb554f8a2fd8e5154cc42eddedc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9dfeee2965c1305f327d0287bf9f648cadf7388546038ee035c1cb4a1957a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0cfbc775a62fa3c478138f7a9ce2274ab6be2821a448bbdc29fae5e28f1e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterConfig",
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
        "hostname_prefix": "hostnamePrefix",
        "odb_network_id": "odbNetworkId",
        "ssh_public_keys": "sshPublicKeys",
        "cluster_name": "clusterName",
        "data_collection_options": "dataCollectionOptions",
        "data_storage_size_in_tbs": "dataStorageSizeInTbs",
        "db_node_storage_size_in_gbs": "dbNodeStorageSizeInGbs",
        "is_local_backup_enabled": "isLocalBackupEnabled",
        "is_sparse_diskgroup_enabled": "isSparseDiskgroupEnabled",
        "license_model": "licenseModel",
        "memory_size_in_gbs": "memorySizeInGbs",
        "region": "region",
        "scan_listener_port_tcp": "scanListenerPortTcp",
        "tags": "tags",
        "timeouts": "timeouts",
        "timezone": "timezone",
    },
)
class OdbCloudVmClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        hostname_prefix: builtins.str,
        odb_network_id: builtins.str,
        ssh_public_keys: typing.Sequence[builtins.str],
        cluster_name: typing.Optional[builtins.str] = None,
        data_collection_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OdbCloudVmClusterDataCollectionOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_storage_size_in_tbs: typing.Optional[jsii.Number] = None,
        db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
        is_local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        license_model: typing.Optional[builtins.str] = None,
        memory_size_in_gbs: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OdbCloudVmClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cloud_exadata_infrastructure_id: The unique identifier of the Exadata infrastructure for this VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#cloud_exadata_infrastructure_id OdbCloudVmCluster#cloud_exadata_infrastructure_id}
        :param cpu_core_count: The number of CPU cores to enable on the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#cpu_core_count OdbCloudVmCluster#cpu_core_count}
        :param db_servers: The list of database servers for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#db_servers OdbCloudVmCluster#db_servers}
        :param display_name: A user-friendly name for the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#display_name OdbCloudVmCluster#display_name}
        :param gi_version: A valid software version of Oracle Grid Infrastructure (GI). To get the list of valid values, use the ListGiVersions operation and specify the shape of the Exadata infrastructure. Example: 19.0.0.0 This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#gi_version OdbCloudVmCluster#gi_version}
        :param hostname_prefix: The host name prefix for the VM cluster. Constraints: - Can't be "localhost" or "hostname". - Can't contain "-version". - The maximum length of the combined hostname and domain is 63 characters. - The hostname must be unique within the subnet. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#hostname_prefix OdbCloudVmCluster#hostname_prefix}
        :param odb_network_id: The unique identifier of the ODB network for the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#odb_network_id OdbCloudVmCluster#odb_network_id}
        :param ssh_public_keys: The public key portion of one or more key pairs used for SSH access to the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#ssh_public_keys OdbCloudVmCluster#ssh_public_keys}
        :param cluster_name: The name of the Grid Infrastructure (GI) cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#cluster_name OdbCloudVmCluster#cluster_name}
        :param data_collection_options: data_collection_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#data_collection_options OdbCloudVmCluster#data_collection_options}
        :param data_storage_size_in_tbs: The size of the data disk group, in terabytes (TBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#data_storage_size_in_tbs OdbCloudVmCluster#data_storage_size_in_tbs}
        :param db_node_storage_size_in_gbs: The amount of local node storage, in gigabytes (GBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#db_node_storage_size_in_gbs OdbCloudVmCluster#db_node_storage_size_in_gbs}
        :param is_local_backup_enabled: Specifies whether to enable database backups to local Exadata storage for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_local_backup_enabled OdbCloudVmCluster#is_local_backup_enabled}
        :param is_sparse_diskgroup_enabled: Specifies whether to create a sparse disk group for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_sparse_diskgroup_enabled OdbCloudVmCluster#is_sparse_diskgroup_enabled}
        :param license_model: The Oracle license model to apply to the VM cluster. Default: LICENSE_INCLUDED. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#license_model OdbCloudVmCluster#license_model}
        :param memory_size_in_gbs: The amount of memory, in gigabytes (GBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#memory_size_in_gbs OdbCloudVmCluster#memory_size_in_gbs}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#region OdbCloudVmCluster#region}
        :param scan_listener_port_tcp: The port number for TCP connections to the single client access name (SCAN) listener. Valid values: 1024–8999 with the following exceptions: 2484 , 6100 , 6200 , 7060, 7070 , 7085 , and 7879Default: 1521. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#scan_listener_port_tcp OdbCloudVmCluster#scan_listener_port_tcp}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#tags OdbCloudVmCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#timeouts OdbCloudVmCluster#timeouts}
        :param timezone: The configured time zone of the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#timezone OdbCloudVmCluster#timezone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = OdbCloudVmClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab17da6d474070d35fc69a34e5dd94aea8c804696de6b1c55c7890be5565d1aa)
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
            check_type(argname="argument hostname_prefix", value=hostname_prefix, expected_type=type_hints["hostname_prefix"])
            check_type(argname="argument odb_network_id", value=odb_network_id, expected_type=type_hints["odb_network_id"])
            check_type(argname="argument ssh_public_keys", value=ssh_public_keys, expected_type=type_hints["ssh_public_keys"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument data_collection_options", value=data_collection_options, expected_type=type_hints["data_collection_options"])
            check_type(argname="argument data_storage_size_in_tbs", value=data_storage_size_in_tbs, expected_type=type_hints["data_storage_size_in_tbs"])
            check_type(argname="argument db_node_storage_size_in_gbs", value=db_node_storage_size_in_gbs, expected_type=type_hints["db_node_storage_size_in_gbs"])
            check_type(argname="argument is_local_backup_enabled", value=is_local_backup_enabled, expected_type=type_hints["is_local_backup_enabled"])
            check_type(argname="argument is_sparse_diskgroup_enabled", value=is_sparse_diskgroup_enabled, expected_type=type_hints["is_sparse_diskgroup_enabled"])
            check_type(argname="argument license_model", value=license_model, expected_type=type_hints["license_model"])
            check_type(argname="argument memory_size_in_gbs", value=memory_size_in_gbs, expected_type=type_hints["memory_size_in_gbs"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scan_listener_port_tcp", value=scan_listener_port_tcp, expected_type=type_hints["scan_listener_port_tcp"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_exadata_infrastructure_id": cloud_exadata_infrastructure_id,
            "cpu_core_count": cpu_core_count,
            "db_servers": db_servers,
            "display_name": display_name,
            "gi_version": gi_version,
            "hostname_prefix": hostname_prefix,
            "odb_network_id": odb_network_id,
            "ssh_public_keys": ssh_public_keys,
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
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if data_collection_options is not None:
            self._values["data_collection_options"] = data_collection_options
        if data_storage_size_in_tbs is not None:
            self._values["data_storage_size_in_tbs"] = data_storage_size_in_tbs
        if db_node_storage_size_in_gbs is not None:
            self._values["db_node_storage_size_in_gbs"] = db_node_storage_size_in_gbs
        if is_local_backup_enabled is not None:
            self._values["is_local_backup_enabled"] = is_local_backup_enabled
        if is_sparse_diskgroup_enabled is not None:
            self._values["is_sparse_diskgroup_enabled"] = is_sparse_diskgroup_enabled
        if license_model is not None:
            self._values["license_model"] = license_model
        if memory_size_in_gbs is not None:
            self._values["memory_size_in_gbs"] = memory_size_in_gbs
        if region is not None:
            self._values["region"] = region
        if scan_listener_port_tcp is not None:
            self._values["scan_listener_port_tcp"] = scan_listener_port_tcp
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if timezone is not None:
            self._values["timezone"] = timezone

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
        '''The unique identifier of the Exadata infrastructure for this VM cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#cloud_exadata_infrastructure_id OdbCloudVmCluster#cloud_exadata_infrastructure_id}
        '''
        result = self._values.get("cloud_exadata_infrastructure_id")
        assert result is not None, "Required property 'cloud_exadata_infrastructure_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cpu_core_count(self) -> jsii.Number:
        '''The number of CPU cores to enable on the VM cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#cpu_core_count OdbCloudVmCluster#cpu_core_count}
        '''
        result = self._values.get("cpu_core_count")
        assert result is not None, "Required property 'cpu_core_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def db_servers(self) -> typing.List[builtins.str]:
        '''The list of database servers for the VM cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#db_servers OdbCloudVmCluster#db_servers}
        '''
        result = self._values.get("db_servers")
        assert result is not None, "Required property 'db_servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''A user-friendly name for the VM cluster. This member is required. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#display_name OdbCloudVmCluster#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gi_version(self) -> builtins.str:
        '''A valid software version of Oracle Grid Infrastructure (GI).

        To get the list of valid values, use the ListGiVersions operation and specify the shape of the Exadata infrastructure. Example: 19.0.0.0 This member is required. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#gi_version OdbCloudVmCluster#gi_version}
        '''
        result = self._values.get("gi_version")
        assert result is not None, "Required property 'gi_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname_prefix(self) -> builtins.str:
        '''The host name prefix for the VM cluster.

        Constraints: - Can't be "localhost" or "hostname". - Can't contain "-version". - The maximum length of the combined hostname and domain is 63 characters. - The hostname must be unique within the subnet. This member is required. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#hostname_prefix OdbCloudVmCluster#hostname_prefix}
        '''
        result = self._values.get("hostname_prefix")
        assert result is not None, "Required property 'hostname_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def odb_network_id(self) -> builtins.str:
        '''The unique identifier of the ODB network for the VM cluster.

        This member is required. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#odb_network_id OdbCloudVmCluster#odb_network_id}
        '''
        result = self._values.get("odb_network_id")
        assert result is not None, "Required property 'odb_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_public_keys(self) -> typing.List[builtins.str]:
        '''The public key portion of one or more key pairs used for SSH access to the VM cluster.

        This member is required. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#ssh_public_keys OdbCloudVmCluster#ssh_public_keys}
        '''
        result = self._values.get("ssh_public_keys")
        assert result is not None, "Required property 'ssh_public_keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Grid Infrastructure (GI) cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#cluster_name OdbCloudVmCluster#cluster_name}
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_collection_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudVmClusterDataCollectionOptions"]]]:
        '''data_collection_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#data_collection_options OdbCloudVmCluster#data_collection_options}
        '''
        result = self._values.get("data_collection_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudVmClusterDataCollectionOptions"]]], result)

    @builtins.property
    def data_storage_size_in_tbs(self) -> typing.Optional[jsii.Number]:
        '''The size of the data disk group, in terabytes (TBs), to allocate for the VM cluster.

        Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#data_storage_size_in_tbs OdbCloudVmCluster#data_storage_size_in_tbs}
        '''
        result = self._values.get("data_storage_size_in_tbs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_node_storage_size_in_gbs(self) -> typing.Optional[jsii.Number]:
        '''The amount of local node storage, in gigabytes (GBs), to allocate for the VM cluster.

        Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#db_node_storage_size_in_gbs OdbCloudVmCluster#db_node_storage_size_in_gbs}
        '''
        result = self._values.get("db_node_storage_size_in_gbs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def is_local_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to enable database backups to local Exadata storage for the VM cluster.

        Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_local_backup_enabled OdbCloudVmCluster#is_local_backup_enabled}
        '''
        result = self._values.get("is_local_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_sparse_diskgroup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to create a sparse disk group for the VM cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_sparse_diskgroup_enabled OdbCloudVmCluster#is_sparse_diskgroup_enabled}
        '''
        result = self._values.get("is_sparse_diskgroup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def license_model(self) -> typing.Optional[builtins.str]:
        '''The Oracle license model to apply to the VM cluster. Default: LICENSE_INCLUDED. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#license_model OdbCloudVmCluster#license_model}
        '''
        result = self._values.get("license_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_size_in_gbs(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory, in gigabytes (GBs), to allocate for the VM cluster.

        Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#memory_size_in_gbs OdbCloudVmCluster#memory_size_in_gbs}
        '''
        result = self._values.get("memory_size_in_gbs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#region OdbCloudVmCluster#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scan_listener_port_tcp(self) -> typing.Optional[jsii.Number]:
        '''The port number for TCP connections to the single client access name (SCAN) listener.

        Valid values: 1024–8999 with the following exceptions: 2484 , 6100 , 6200 , 7060, 7070 , 7085 , and 7879Default: 1521. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#scan_listener_port_tcp OdbCloudVmCluster#scan_listener_port_tcp}
        '''
        result = self._values.get("scan_listener_port_tcp")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#tags OdbCloudVmCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OdbCloudVmClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#timeouts OdbCloudVmCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OdbCloudVmClusterTimeouts"], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''The configured time zone of the VM cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#timezone OdbCloudVmCluster#timezone}
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudVmClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterDataCollectionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "is_diagnostics_events_enabled": "isDiagnosticsEventsEnabled",
        "is_health_monitoring_enabled": "isHealthMonitoringEnabled",
        "is_incident_logs_enabled": "isIncidentLogsEnabled",
    },
)
class OdbCloudVmClusterDataCollectionOptions:
    def __init__(
        self,
        *,
        is_diagnostics_events_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        is_health_monitoring_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        is_incident_logs_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param is_diagnostics_events_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_diagnostics_events_enabled OdbCloudVmCluster#is_diagnostics_events_enabled}.
        :param is_health_monitoring_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_health_monitoring_enabled OdbCloudVmCluster#is_health_monitoring_enabled}.
        :param is_incident_logs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_incident_logs_enabled OdbCloudVmCluster#is_incident_logs_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491e2c38885410b0d6c03cf3c3d91b934d7f38aa7839db610f13aa9a20049260)
            check_type(argname="argument is_diagnostics_events_enabled", value=is_diagnostics_events_enabled, expected_type=type_hints["is_diagnostics_events_enabled"])
            check_type(argname="argument is_health_monitoring_enabled", value=is_health_monitoring_enabled, expected_type=type_hints["is_health_monitoring_enabled"])
            check_type(argname="argument is_incident_logs_enabled", value=is_incident_logs_enabled, expected_type=type_hints["is_incident_logs_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_diagnostics_events_enabled": is_diagnostics_events_enabled,
            "is_health_monitoring_enabled": is_health_monitoring_enabled,
            "is_incident_logs_enabled": is_incident_logs_enabled,
        }

    @builtins.property
    def is_diagnostics_events_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_diagnostics_events_enabled OdbCloudVmCluster#is_diagnostics_events_enabled}.'''
        result = self._values.get("is_diagnostics_events_enabled")
        assert result is not None, "Required property 'is_diagnostics_events_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def is_health_monitoring_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_health_monitoring_enabled OdbCloudVmCluster#is_health_monitoring_enabled}.'''
        result = self._values.get("is_health_monitoring_enabled")
        assert result is not None, "Required property 'is_health_monitoring_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def is_incident_logs_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#is_incident_logs_enabled OdbCloudVmCluster#is_incident_logs_enabled}.'''
        result = self._values.get("is_incident_logs_enabled")
        assert result is not None, "Required property 'is_incident_logs_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudVmClusterDataCollectionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbCloudVmClusterDataCollectionOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterDataCollectionOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f870a6698d22972462155bcb76e0143521c32d5317b8c6c70664f93ee3c87ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbCloudVmClusterDataCollectionOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f08f4921dd9b337c47c9b7a98d14acf4d3539df815561b58c10f6f776773d0e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbCloudVmClusterDataCollectionOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1597c738493003e16d81889fc234b59db519ccfc8c75a107fb63c62b3e9c44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9e6413c92a9f5d06e17a162ec03d1e919fa3247a4ecd084ab9463eb94a52c6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e78df1c3909a5e49e35cf7a087aa103cb7da0e4f83c1f8d2c98feb90c3d9118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudVmClusterDataCollectionOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudVmClusterDataCollectionOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudVmClusterDataCollectionOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e730a591aa1cf740891011b2302f855c478c2bcbb820c344c18f1173abda63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OdbCloudVmClusterDataCollectionOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterDataCollectionOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d823c161f9d1328f7b06eb7697426c702373cadee89b4800c81c113902d8f22c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="isDiagnosticsEventsEnabledInput")
    def is_diagnostics_events_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isDiagnosticsEventsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isHealthMonitoringEnabledInput")
    def is_health_monitoring_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isHealthMonitoringEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isIncidentLogsEnabledInput")
    def is_incident_logs_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isIncidentLogsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isDiagnosticsEventsEnabled")
    def is_diagnostics_events_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isDiagnosticsEventsEnabled"))

    @is_diagnostics_events_enabled.setter
    def is_diagnostics_events_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85296f238810dd873f34e6f6eae4481e2b4afe174938c4d7d5d025c835bbfc5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDiagnosticsEventsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isHealthMonitoringEnabled")
    def is_health_monitoring_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isHealthMonitoringEnabled"))

    @is_health_monitoring_enabled.setter
    def is_health_monitoring_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b78d26817c4494b2aa48428859b8ed3b14112e92ba1dfd7de063d6d8cf22c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isHealthMonitoringEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isIncidentLogsEnabled")
    def is_incident_logs_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isIncidentLogsEnabled"))

    @is_incident_logs_enabled.setter
    def is_incident_logs_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643bd0fe15ae0735278a6eefa1fbc4d420983e004f8976b50f248350c1da9b70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isIncidentLogsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterDataCollectionOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterDataCollectionOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterDataCollectionOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3caa16e2aa8671c3da141e6b11c52ce4a683507b781aa23891294525939deda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCache",
    jsii_struct_bases=[],
    name_mapping={},
)
class OdbCloudVmClusterIormConfigCache:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudVmClusterIormConfigCache(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCacheDbPlans",
    jsii_struct_bases=[],
    name_mapping={},
)
class OdbCloudVmClusterIormConfigCacheDbPlans:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudVmClusterIormConfigCacheDbPlans(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbCloudVmClusterIormConfigCacheDbPlansList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCacheDbPlansList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84a58bf25e6679e793dbafa24ee575ce2ff1c0c8639beb8c7bb002d6a5e3d28d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbCloudVmClusterIormConfigCacheDbPlansOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a213233fe3263e4aaad7a4c5e70f50c4a86c9e478d95918a846398713f7d6e1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbCloudVmClusterIormConfigCacheDbPlansOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f421c8c6adf898e38e03e646bda5a72766f08515858d1bab6861742cfa2aa2dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a4173d3d0466819f733fca6b84e939ff3f82a1d1bbdd8abea02074676b29138)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20dfeec2e10ff74552dac4d043cb784f2e764b4905f99c80ef7844e7a55b4943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OdbCloudVmClusterIormConfigCacheDbPlansOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCacheDbPlansOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__583ff52f573212f40d5b1d388941d9da085fd6b4f11f152a441e58c1ff02ee0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dbName")
    def db_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbName"))

    @builtins.property
    @jsii.member(jsii_name="flashCacheLimit")
    def flash_cache_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flashCacheLimit"))

    @builtins.property
    @jsii.member(jsii_name="share")
    def share(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "share"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OdbCloudVmClusterIormConfigCacheDbPlans]:
        return typing.cast(typing.Optional[OdbCloudVmClusterIormConfigCacheDbPlans], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OdbCloudVmClusterIormConfigCacheDbPlans],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749985a7fdd95464cbafd421df7b81fcda4fe693531a9fd1e9cd96fbe7055c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OdbCloudVmClusterIormConfigCacheList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCacheList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d79366ecdee96617af0c4d1791f24fc12fda45fba27886633368a35e10c1d778)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbCloudVmClusterIormConfigCacheOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68488f54f99cfadb14f0b9096bdbad14699e74d050514f187d8cd5f0b77a5cdd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbCloudVmClusterIormConfigCacheOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65fa3219e9295be8172a91d52a837e20e4c36ef084c5b29f83d71e8d5d4c47b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b3a359b6d34b2ad449f7336bc39c145900f78fe6570a987bb16a8f2b0ede4bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5de3d07009d0e75cecca1bc0bdd6cfd58d9db132050d52f424be9fcd5f546e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OdbCloudVmClusterIormConfigCacheOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCacheOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b85cfb68840be638f464923725c41e10a560ec89a4bfb1bc98941d6d03d39ce2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dbPlans")
    def db_plans(self) -> OdbCloudVmClusterIormConfigCacheDbPlansList:
        return typing.cast(OdbCloudVmClusterIormConfigCacheDbPlansList, jsii.get(self, "dbPlans"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleDetails")
    def lifecycle_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleDetails"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleState")
    def lifecycle_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleState"))

    @builtins.property
    @jsii.member(jsii_name="objective")
    def objective(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objective"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OdbCloudVmClusterIormConfigCache]:
        return typing.cast(typing.Optional[OdbCloudVmClusterIormConfigCache], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OdbCloudVmClusterIormConfigCache],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59806fd574db5315d88ce77b6546616049e497db32f381adafa30ea1b149532f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class OdbCloudVmClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#create OdbCloudVmCluster#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#delete OdbCloudVmCluster#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#update OdbCloudVmCluster#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97857521a26f62f808276e54536457a44f53333d1d987b54fa24f694e74ad555)
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
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#create OdbCloudVmCluster#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#delete OdbCloudVmCluster#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_vm_cluster#update OdbCloudVmCluster#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudVmClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbCloudVmClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudVmCluster.OdbCloudVmClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__943d56c79572189c6835345da3e6b80185b13d3be0ecbcdf8d10ba49864b5a33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce762212c7175b906285176e3f1aacbe38178bdb3f181c5ea97e8458e39a6734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304d9b1881a9bc144b8d818b78b2b3cdb86c9244d4a56b96da82a953fe36b6ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e24c4fe62d5fae0466ca46c1b24f8abb5d6d6d2f9589209b4b10448fc608f800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773fd2bedc1b06c588d31493126b1a725ae955ddc48956b9bfea0941313e9a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OdbCloudVmCluster",
    "OdbCloudVmClusterConfig",
    "OdbCloudVmClusterDataCollectionOptions",
    "OdbCloudVmClusterDataCollectionOptionsList",
    "OdbCloudVmClusterDataCollectionOptionsOutputReference",
    "OdbCloudVmClusterIormConfigCache",
    "OdbCloudVmClusterIormConfigCacheDbPlans",
    "OdbCloudVmClusterIormConfigCacheDbPlansList",
    "OdbCloudVmClusterIormConfigCacheDbPlansOutputReference",
    "OdbCloudVmClusterIormConfigCacheList",
    "OdbCloudVmClusterIormConfigCacheOutputReference",
    "OdbCloudVmClusterTimeouts",
    "OdbCloudVmClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3156d1e4c43f388bd424347deed81dcca3cb8d60639def831efc4045b6aca277(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cloud_exadata_infrastructure_id: builtins.str,
    cpu_core_count: jsii.Number,
    db_servers: typing.Sequence[builtins.str],
    display_name: builtins.str,
    gi_version: builtins.str,
    hostname_prefix: builtins.str,
    odb_network_id: builtins.str,
    ssh_public_keys: typing.Sequence[builtins.str],
    cluster_name: typing.Optional[builtins.str] = None,
    data_collection_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudVmClusterDataCollectionOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_storage_size_in_tbs: typing.Optional[jsii.Number] = None,
    db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
    is_local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    license_model: typing.Optional[builtins.str] = None,
    memory_size_in_gbs: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OdbCloudVmClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timezone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__2e3969eebc3486e30d57be28df60b81c0659306facd9507d2ed34eee65bc7672(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bacc3febd98b0c59606f4e69a551ebc77587987e0e47b013f1539094a2c21e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudVmClusterDataCollectionOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253fd06e06f5e28be7ef7af1365b308cf3467a6a935a2b27d02c53d6df278a6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a59d10809c3b8f0588f012f5812437fcc277c43abb0d2338e492eacf5151d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1529a4625063e97ae38954934ecc56dd93ff92e36201ddaf3f929c251aeac4e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0eb3b3dd5000bff6dabcd088dab560fafbfa424c2c88f5baee2abe3b7d76e53(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d629faa0102bd37dde97228f234ee3804554528e87742427ec5241b9b782a5c3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa6bbe892741331de56b988436aede0451fc8f4a60821b4b9ff4f44468d6ad1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f917d93a2399a6235306319d1c964019b76bfced25bfb703d24ed01336c1b0e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a10cd06fafe79714d30b8c30f03022c62c450015d04184d47d7ece799121b2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f214a2eb5ec9c335ef8fbbd1998be9fc649785241aa19617e2add4c5530048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744002c74526aa046724f4f85618f5270897867a78b1428fc197aa3d372138cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b67b4a4954be02a42e2a2a372685189256ced6bb87dfe49d05e463469c30434(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c58f8aef9f53001de3d4c1b63e480b6657cf7a0ff8bdc923fa855613127e051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a82812d39c59ddcf8b91812c9a40a0e02add53d66c99d849789a58408c24b46(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b63f6cb9d225d739cd9f5da619bb46af7b6d4dd9c13dc5fa3e84a3c3fd3a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a2f3ea7444e60d49a3875e4e31f6623202f2c5cfdc7d1d7ca4f240511bbfd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11f1d371ee5d9651845d83496667c670fc980ccc19b0b31432402e787d28a94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe60c5a7fc05b3576d0abd218c25106864fcb554f8a2fd8e5154cc42eddedc0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9dfeee2965c1305f327d0287bf9f648cadf7388546038ee035c1cb4a1957a4a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0cfbc775a62fa3c478138f7a9ce2274ab6be2821a448bbdc29fae5e28f1e8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab17da6d474070d35fc69a34e5dd94aea8c804696de6b1c55c7890be5565d1aa(
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
    hostname_prefix: builtins.str,
    odb_network_id: builtins.str,
    ssh_public_keys: typing.Sequence[builtins.str],
    cluster_name: typing.Optional[builtins.str] = None,
    data_collection_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudVmClusterDataCollectionOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_storage_size_in_tbs: typing.Optional[jsii.Number] = None,
    db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
    is_local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    license_model: typing.Optional[builtins.str] = None,
    memory_size_in_gbs: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OdbCloudVmClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491e2c38885410b0d6c03cf3c3d91b934d7f38aa7839db610f13aa9a20049260(
    *,
    is_diagnostics_events_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    is_health_monitoring_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    is_incident_logs_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f870a6698d22972462155bcb76e0143521c32d5317b8c6c70664f93ee3c87ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f08f4921dd9b337c47c9b7a98d14acf4d3539df815561b58c10f6f776773d0e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1597c738493003e16d81889fc234b59db519ccfc8c75a107fb63c62b3e9c44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e6413c92a9f5d06e17a162ec03d1e919fa3247a4ecd084ab9463eb94a52c6e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e78df1c3909a5e49e35cf7a087aa103cb7da0e4f83c1f8d2c98feb90c3d9118(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e730a591aa1cf740891011b2302f855c478c2bcbb820c344c18f1173abda63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudVmClusterDataCollectionOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d823c161f9d1328f7b06eb7697426c702373cadee89b4800c81c113902d8f22c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85296f238810dd873f34e6f6eae4481e2b4afe174938c4d7d5d025c835bbfc5f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b78d26817c4494b2aa48428859b8ed3b14112e92ba1dfd7de063d6d8cf22c83(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643bd0fe15ae0735278a6eefa1fbc4d420983e004f8976b50f248350c1da9b70(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3caa16e2aa8671c3da141e6b11c52ce4a683507b781aa23891294525939deda(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterDataCollectionOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a58bf25e6679e793dbafa24ee575ce2ff1c0c8639beb8c7bb002d6a5e3d28d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a213233fe3263e4aaad7a4c5e70f50c4a86c9e478d95918a846398713f7d6e1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f421c8c6adf898e38e03e646bda5a72766f08515858d1bab6861742cfa2aa2dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4173d3d0466819f733fca6b84e939ff3f82a1d1bbdd8abea02074676b29138(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20dfeec2e10ff74552dac4d043cb784f2e764b4905f99c80ef7844e7a55b4943(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583ff52f573212f40d5b1d388941d9da085fd6b4f11f152a441e58c1ff02ee0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749985a7fdd95464cbafd421df7b81fcda4fe693531a9fd1e9cd96fbe7055c39(
    value: typing.Optional[OdbCloudVmClusterIormConfigCacheDbPlans],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79366ecdee96617af0c4d1791f24fc12fda45fba27886633368a35e10c1d778(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68488f54f99cfadb14f0b9096bdbad14699e74d050514f187d8cd5f0b77a5cdd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fa3219e9295be8172a91d52a837e20e4c36ef084c5b29f83d71e8d5d4c47b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3a359b6d34b2ad449f7336bc39c145900f78fe6570a987bb16a8f2b0ede4bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de3d07009d0e75cecca1bc0bdd6cfd58d9db132050d52f424be9fcd5f546e2d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85cfb68840be638f464923725c41e10a560ec89a4bfb1bc98941d6d03d39ce2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59806fd574db5315d88ce77b6546616049e497db32f381adafa30ea1b149532f(
    value: typing.Optional[OdbCloudVmClusterIormConfigCache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97857521a26f62f808276e54536457a44f53333d1d987b54fa24f694e74ad555(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943d56c79572189c6835345da3e6b80185b13d3be0ecbcdf8d10ba49864b5a33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce762212c7175b906285176e3f1aacbe38178bdb3f181c5ea97e8458e39a6734(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304d9b1881a9bc144b8d818b78b2b3cdb86c9244d4a56b96da82a953fe36b6ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24c4fe62d5fae0466ca46c1b24f8abb5d6d6d2f9589209b4b10448fc608f800(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773fd2bedc1b06c588d31493126b1a725ae955ddc48956b9bfea0941313e9a45(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
