r'''
# `aws_odb_cloud_autonomous_vm_cluster`

Refer to the Terraform Registry for docs: [`aws_odb_cloud_autonomous_vm_cluster`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster).
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


class OdbCloudAutonomousVmCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster aws_odb_cloud_autonomous_vm_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        autonomous_data_storage_size_in_tbs: jsii.Number,
        cloud_exadata_infrastructure_id: builtins.str,
        cpu_core_count_per_node: jsii.Number,
        db_servers: typing.Sequence[builtins.str],
        display_name: builtins.str,
        memory_per_oracle_compute_unit_in_gbs: jsii.Number,
        odb_network_id: builtins.str,
        scan_listener_port_non_tls: jsii.Number,
        scan_listener_port_tls: jsii.Number,
        total_container_databases: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        is_mtls_enabled_vm_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        license_model: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OdbCloudAutonomousVmClusterMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OdbCloudAutonomousVmClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster aws_odb_cloud_autonomous_vm_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param autonomous_data_storage_size_in_tbs: The data storage size allocated for Autonomous Databases in the Autonomous VM cluster, in TB. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#autonomous_data_storage_size_in_tbs OdbCloudAutonomousVmCluster#autonomous_data_storage_size_in_tbs}
        :param cloud_exadata_infrastructure_id: Exadata infrastructure id. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#cloud_exadata_infrastructure_id OdbCloudAutonomousVmCluster#cloud_exadata_infrastructure_id}
        :param cpu_core_count_per_node: The number of CPU cores enabled per node in the Autonomous VM cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#cpu_core_count_per_node OdbCloudAutonomousVmCluster#cpu_core_count_per_node}
        :param db_servers: The database servers in the Autonomous VM cluster. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#db_servers OdbCloudAutonomousVmCluster#db_servers}
        :param display_name: The display name of the Autonomous VM cluster. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#display_name OdbCloudAutonomousVmCluster#display_name}
        :param memory_per_oracle_compute_unit_in_gbs: The amount of memory allocated per Oracle Compute Unit, in GB. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#memory_per_oracle_compute_unit_in_gbs OdbCloudAutonomousVmCluster#memory_per_oracle_compute_unit_in_gbs}
        :param odb_network_id: The unique identifier of the ODB network associated with this Autonomous VM Cluster. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#odb_network_id OdbCloudAutonomousVmCluster#odb_network_id}
        :param scan_listener_port_non_tls: The SCAN listener port for non-TLS (TCP) protocol. The default is 1521. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#scan_listener_port_non_tls OdbCloudAutonomousVmCluster#scan_listener_port_non_tls}
        :param scan_listener_port_tls: The SCAN listener port for TLS (TCP) protocol. The default is 2484. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#scan_listener_port_tls OdbCloudAutonomousVmCluster#scan_listener_port_tls}
        :param total_container_databases: The total number of Autonomous Container Databases that can be created with the allocated local storage. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#total_container_databases OdbCloudAutonomousVmCluster#total_container_databases}
        :param description: The description of the Autonomous VM cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#description OdbCloudAutonomousVmCluster#description}
        :param is_mtls_enabled_vm_cluster: Indicates whether mutual TLS (mTLS) authentication is enabled for the Autonomous VM cluster. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#is_mtls_enabled_vm_cluster OdbCloudAutonomousVmCluster#is_mtls_enabled_vm_cluster}
        :param license_model: The license model for the Autonomous VM cluster. Valid values are LICENSE_INCLUDED or BRING_YOUR_OWN_LICENSE . Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#license_model OdbCloudAutonomousVmCluster#license_model}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#maintenance_window OdbCloudAutonomousVmCluster#maintenance_window}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#region OdbCloudAutonomousVmCluster#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#tags OdbCloudAutonomousVmCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#timeouts OdbCloudAutonomousVmCluster#timeouts}
        :param time_zone: The time zone of the Autonomous VM cluster. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#time_zone OdbCloudAutonomousVmCluster#time_zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3edcfd2f8f68e05db4de02d71429dab609537c00639af333eb80745a834bf9e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = OdbCloudAutonomousVmClusterConfig(
            autonomous_data_storage_size_in_tbs=autonomous_data_storage_size_in_tbs,
            cloud_exadata_infrastructure_id=cloud_exadata_infrastructure_id,
            cpu_core_count_per_node=cpu_core_count_per_node,
            db_servers=db_servers,
            display_name=display_name,
            memory_per_oracle_compute_unit_in_gbs=memory_per_oracle_compute_unit_in_gbs,
            odb_network_id=odb_network_id,
            scan_listener_port_non_tls=scan_listener_port_non_tls,
            scan_listener_port_tls=scan_listener_port_tls,
            total_container_databases=total_container_databases,
            description=description,
            is_mtls_enabled_vm_cluster=is_mtls_enabled_vm_cluster,
            license_model=license_model,
            maintenance_window=maintenance_window,
            region=region,
            tags=tags,
            timeouts=timeouts,
            time_zone=time_zone,
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
        '''Generates CDKTF code for importing a OdbCloudAutonomousVmCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OdbCloudAutonomousVmCluster to import.
        :param import_from_id: The id of the existing OdbCloudAutonomousVmCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OdbCloudAutonomousVmCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eed355ef42cbfc5efc3a1df929397a55fb55e6aae2e913858a875f7f0cb8b49)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OdbCloudAutonomousVmClusterMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c51bc5d563da3b2b0d0ab3a55f710091a0492724f9e5681c134fd9fcbeb754c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#create OdbCloudAutonomousVmCluster#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#delete OdbCloudAutonomousVmCluster#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#update OdbCloudAutonomousVmCluster#update}
        '''
        value = OdbCloudAutonomousVmClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetIsMtlsEnabledVmCluster")
    def reset_is_mtls_enabled_vm_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsMtlsEnabledVmCluster", []))

    @jsii.member(jsii_name="resetLicenseModel")
    def reset_license_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseModel", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

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
    @jsii.member(jsii_name="autonomousDataStoragePercentage")
    def autonomous_data_storage_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autonomousDataStoragePercentage"))

    @builtins.property
    @jsii.member(jsii_name="availableAutonomousDataStorageSizeInTbs")
    def available_autonomous_data_storage_size_in_tbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availableAutonomousDataStorageSizeInTbs"))

    @builtins.property
    @jsii.member(jsii_name="availableContainerDatabases")
    def available_container_databases(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availableContainerDatabases"))

    @builtins.property
    @jsii.member(jsii_name="availableCpus")
    def available_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availableCpus"))

    @builtins.property
    @jsii.member(jsii_name="computeModel")
    def compute_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeModel"))

    @builtins.property
    @jsii.member(jsii_name="cpuCoreCount")
    def cpu_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCoreCount"))

    @builtins.property
    @jsii.member(jsii_name="cpuPercentage")
    def cpu_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuPercentage"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeInGbs")
    def data_storage_size_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeInGbs"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeInTbs")
    def data_storage_size_in_tbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeInTbs"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="exadataStorageInTbsLowestScaledValue")
    def exadata_storage_in_tbs_lowest_scaled_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "exadataStorageInTbsLowestScaledValue"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(self) -> "OdbCloudAutonomousVmClusterMaintenanceWindowList":
        return typing.cast("OdbCloudAutonomousVmClusterMaintenanceWindowList", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="maxAcdsLowestScaledValue")
    def max_acds_lowest_scaled_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAcdsLowestScaledValue"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeInGbs")
    def memory_size_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeInGbs"))

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @builtins.property
    @jsii.member(jsii_name="nonProvisionableAutonomousContainerDatabases")
    def non_provisionable_autonomous_container_databases(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nonProvisionableAutonomousContainerDatabases"))

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
    @jsii.member(jsii_name="odbNodeStorageSizeInGbs")
    def odb_node_storage_size_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "odbNodeStorageSizeInGbs"))

    @builtins.property
    @jsii.member(jsii_name="percentProgress")
    def percent_progress(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentProgress"))

    @builtins.property
    @jsii.member(jsii_name="provisionableAutonomousContainerDatabases")
    def provisionable_autonomous_container_databases(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionableAutonomousContainerDatabases"))

    @builtins.property
    @jsii.member(jsii_name="provisionedAutonomousContainerDatabases")
    def provisioned_autonomous_container_databases(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedAutonomousContainerDatabases"))

    @builtins.property
    @jsii.member(jsii_name="provisionedCpus")
    def provisioned_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedCpus"))

    @builtins.property
    @jsii.member(jsii_name="reclaimableCpus")
    def reclaimable_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reclaimableCpus"))

    @builtins.property
    @jsii.member(jsii_name="reservedCpus")
    def reserved_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reservedCpus"))

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
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="timeDatabaseSslCertificateExpires")
    def time_database_ssl_certificate_expires(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeDatabaseSslCertificateExpires"))

    @builtins.property
    @jsii.member(jsii_name="timeOrdsCertificateExpires")
    def time_ords_certificate_expires(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeOrdsCertificateExpires"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OdbCloudAutonomousVmClusterTimeoutsOutputReference":
        return typing.cast("OdbCloudAutonomousVmClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autonomousDataStorageSizeInTbsInput")
    def autonomous_data_storage_size_in_tbs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autonomousDataStorageSizeInTbsInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureIdInput")
    def cloud_exadata_infrastructure_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudExadataInfrastructureIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCoreCountPerNodeInput")
    def cpu_core_count_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuCoreCountPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="dbServersInput")
    def db_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dbServersInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="isMtlsEnabledVmClusterInput")
    def is_mtls_enabled_vm_cluster_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isMtlsEnabledVmClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseModelInput")
    def license_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseModelInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudAutonomousVmClusterMaintenanceWindow"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudAutonomousVmClusterMaintenanceWindow"]]], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryPerOracleComputeUnitInGbsInput")
    def memory_per_oracle_compute_unit_in_gbs_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryPerOracleComputeUnitInGbsInput"))

    @builtins.property
    @jsii.member(jsii_name="odbNetworkIdInput")
    def odb_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "odbNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortNonTlsInput")
    def scan_listener_port_non_tls_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scanListenerPortNonTlsInput"))

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTlsInput")
    def scan_listener_port_tls_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scanListenerPortTlsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OdbCloudAutonomousVmClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OdbCloudAutonomousVmClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="totalContainerDatabasesInput")
    def total_container_databases_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "totalContainerDatabasesInput"))

    @builtins.property
    @jsii.member(jsii_name="autonomousDataStorageSizeInTbs")
    def autonomous_data_storage_size_in_tbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autonomousDataStorageSizeInTbs"))

    @autonomous_data_storage_size_in_tbs.setter
    def autonomous_data_storage_size_in_tbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a2cbacc20a9e4316801c2e2db84cce4374fd7e7fa4a4098a81a502d6ead1521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autonomousDataStorageSizeInTbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureId")
    def cloud_exadata_infrastructure_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudExadataInfrastructureId"))

    @cloud_exadata_infrastructure_id.setter
    def cloud_exadata_infrastructure_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7809c4a80ab9b887f934731c9e46fa1c30ac96fc250fba6403b4755075aca6ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudExadataInfrastructureId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCoreCountPerNode")
    def cpu_core_count_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCoreCountPerNode"))

    @cpu_core_count_per_node.setter
    def cpu_core_count_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7320edf3f64a35268cf4a0d10fa421afb47664b935b765df41bb2d0a2dbf83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCoreCountPerNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbServers")
    def db_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dbServers"))

    @db_servers.setter
    def db_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f065b4961e78f9b8f8f45dc222dfbe847064e5ac9811e2975e6ddfd048776aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade2d6f438bbdfc61379eeb13a20cee461b3e1b1f739a1cfd1676eefa6c7379d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a55e038df465fb2fb59c3bd083d95830569a40bacf5e1be6bef6c7bada62100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isMtlsEnabledVmCluster")
    def is_mtls_enabled_vm_cluster(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isMtlsEnabledVmCluster"))

    @is_mtls_enabled_vm_cluster.setter
    def is_mtls_enabled_vm_cluster(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2887d37a7bd0cae1664832729eb610f6a98facf2d6f144c6ed59eea63eb443f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isMtlsEnabledVmCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseModel")
    def license_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseModel"))

    @license_model.setter
    def license_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9281cd9f10c9f40f160e179d517973ca683a18513fa87c4ea57e5a8bd016c2b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memoryPerOracleComputeUnitInGbs")
    def memory_per_oracle_compute_unit_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryPerOracleComputeUnitInGbs"))

    @memory_per_oracle_compute_unit_in_gbs.setter
    def memory_per_oracle_compute_unit_in_gbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed04c9e56e16f70877541774d974f0702846bdf4c71238ca016e9ba9361cec4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryPerOracleComputeUnitInGbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="odbNetworkId")
    def odb_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "odbNetworkId"))

    @odb_network_id.setter
    def odb_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320ab22eeb8816694140f210d881682d1b8fa0194c3bb6b9dc8c64559297fd04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "odbNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0483853b0fd0e53ff53b4fbe8debb8442f22dd5277d479c82d23b173630571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortNonTls")
    def scan_listener_port_non_tls(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scanListenerPortNonTls"))

    @scan_listener_port_non_tls.setter
    def scan_listener_port_non_tls(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325b46414bd2ed5d78fd8aaed9a932c8cc1a96e9ca12028436ccc58288473788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanListenerPortNonTls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTls")
    def scan_listener_port_tls(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scanListenerPortTls"))

    @scan_listener_port_tls.setter
    def scan_listener_port_tls(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5907373ff87b2872238f99c87c8802c6966338fb38fbad795ab3f9fec48acac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanListenerPortTls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4042d4fd37f6f59c206f8e5ba17010fb4d822f0861e7748bc4e88a5c4492fcc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee56d992c4e565e9e7eb937e299cc12561b5d4bf84c1fdcc5783c959cb0f4ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalContainerDatabases")
    def total_container_databases(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalContainerDatabases"))

    @total_container_databases.setter
    def total_container_databases(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13bbcb5ebb1149176c3fcca55ebc551aad0a82e2fd35405049df156a7d706f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalContainerDatabases", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "autonomous_data_storage_size_in_tbs": "autonomousDataStorageSizeInTbs",
        "cloud_exadata_infrastructure_id": "cloudExadataInfrastructureId",
        "cpu_core_count_per_node": "cpuCoreCountPerNode",
        "db_servers": "dbServers",
        "display_name": "displayName",
        "memory_per_oracle_compute_unit_in_gbs": "memoryPerOracleComputeUnitInGbs",
        "odb_network_id": "odbNetworkId",
        "scan_listener_port_non_tls": "scanListenerPortNonTls",
        "scan_listener_port_tls": "scanListenerPortTls",
        "total_container_databases": "totalContainerDatabases",
        "description": "description",
        "is_mtls_enabled_vm_cluster": "isMtlsEnabledVmCluster",
        "license_model": "licenseModel",
        "maintenance_window": "maintenanceWindow",
        "region": "region",
        "tags": "tags",
        "timeouts": "timeouts",
        "time_zone": "timeZone",
    },
)
class OdbCloudAutonomousVmClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        autonomous_data_storage_size_in_tbs: jsii.Number,
        cloud_exadata_infrastructure_id: builtins.str,
        cpu_core_count_per_node: jsii.Number,
        db_servers: typing.Sequence[builtins.str],
        display_name: builtins.str,
        memory_per_oracle_compute_unit_in_gbs: jsii.Number,
        odb_network_id: builtins.str,
        scan_listener_port_non_tls: jsii.Number,
        scan_listener_port_tls: jsii.Number,
        total_container_databases: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        is_mtls_enabled_vm_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        license_model: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OdbCloudAutonomousVmClusterMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OdbCloudAutonomousVmClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param autonomous_data_storage_size_in_tbs: The data storage size allocated for Autonomous Databases in the Autonomous VM cluster, in TB. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#autonomous_data_storage_size_in_tbs OdbCloudAutonomousVmCluster#autonomous_data_storage_size_in_tbs}
        :param cloud_exadata_infrastructure_id: Exadata infrastructure id. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#cloud_exadata_infrastructure_id OdbCloudAutonomousVmCluster#cloud_exadata_infrastructure_id}
        :param cpu_core_count_per_node: The number of CPU cores enabled per node in the Autonomous VM cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#cpu_core_count_per_node OdbCloudAutonomousVmCluster#cpu_core_count_per_node}
        :param db_servers: The database servers in the Autonomous VM cluster. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#db_servers OdbCloudAutonomousVmCluster#db_servers}
        :param display_name: The display name of the Autonomous VM cluster. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#display_name OdbCloudAutonomousVmCluster#display_name}
        :param memory_per_oracle_compute_unit_in_gbs: The amount of memory allocated per Oracle Compute Unit, in GB. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#memory_per_oracle_compute_unit_in_gbs OdbCloudAutonomousVmCluster#memory_per_oracle_compute_unit_in_gbs}
        :param odb_network_id: The unique identifier of the ODB network associated with this Autonomous VM Cluster. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#odb_network_id OdbCloudAutonomousVmCluster#odb_network_id}
        :param scan_listener_port_non_tls: The SCAN listener port for non-TLS (TCP) protocol. The default is 1521. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#scan_listener_port_non_tls OdbCloudAutonomousVmCluster#scan_listener_port_non_tls}
        :param scan_listener_port_tls: The SCAN listener port for TLS (TCP) protocol. The default is 2484. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#scan_listener_port_tls OdbCloudAutonomousVmCluster#scan_listener_port_tls}
        :param total_container_databases: The total number of Autonomous Container Databases that can be created with the allocated local storage. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#total_container_databases OdbCloudAutonomousVmCluster#total_container_databases}
        :param description: The description of the Autonomous VM cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#description OdbCloudAutonomousVmCluster#description}
        :param is_mtls_enabled_vm_cluster: Indicates whether mutual TLS (mTLS) authentication is enabled for the Autonomous VM cluster. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#is_mtls_enabled_vm_cluster OdbCloudAutonomousVmCluster#is_mtls_enabled_vm_cluster}
        :param license_model: The license model for the Autonomous VM cluster. Valid values are LICENSE_INCLUDED or BRING_YOUR_OWN_LICENSE . Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#license_model OdbCloudAutonomousVmCluster#license_model}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#maintenance_window OdbCloudAutonomousVmCluster#maintenance_window}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#region OdbCloudAutonomousVmCluster#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#tags OdbCloudAutonomousVmCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#timeouts OdbCloudAutonomousVmCluster#timeouts}
        :param time_zone: The time zone of the Autonomous VM cluster. Changing this will force terraform to create new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#time_zone OdbCloudAutonomousVmCluster#time_zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = OdbCloudAutonomousVmClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede7b42370598dc58181aab088bd44521646ae35bce10adef214a6dcba47e738)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument autonomous_data_storage_size_in_tbs", value=autonomous_data_storage_size_in_tbs, expected_type=type_hints["autonomous_data_storage_size_in_tbs"])
            check_type(argname="argument cloud_exadata_infrastructure_id", value=cloud_exadata_infrastructure_id, expected_type=type_hints["cloud_exadata_infrastructure_id"])
            check_type(argname="argument cpu_core_count_per_node", value=cpu_core_count_per_node, expected_type=type_hints["cpu_core_count_per_node"])
            check_type(argname="argument db_servers", value=db_servers, expected_type=type_hints["db_servers"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument memory_per_oracle_compute_unit_in_gbs", value=memory_per_oracle_compute_unit_in_gbs, expected_type=type_hints["memory_per_oracle_compute_unit_in_gbs"])
            check_type(argname="argument odb_network_id", value=odb_network_id, expected_type=type_hints["odb_network_id"])
            check_type(argname="argument scan_listener_port_non_tls", value=scan_listener_port_non_tls, expected_type=type_hints["scan_listener_port_non_tls"])
            check_type(argname="argument scan_listener_port_tls", value=scan_listener_port_tls, expected_type=type_hints["scan_listener_port_tls"])
            check_type(argname="argument total_container_databases", value=total_container_databases, expected_type=type_hints["total_container_databases"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument is_mtls_enabled_vm_cluster", value=is_mtls_enabled_vm_cluster, expected_type=type_hints["is_mtls_enabled_vm_cluster"])
            check_type(argname="argument license_model", value=license_model, expected_type=type_hints["license_model"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autonomous_data_storage_size_in_tbs": autonomous_data_storage_size_in_tbs,
            "cloud_exadata_infrastructure_id": cloud_exadata_infrastructure_id,
            "cpu_core_count_per_node": cpu_core_count_per_node,
            "db_servers": db_servers,
            "display_name": display_name,
            "memory_per_oracle_compute_unit_in_gbs": memory_per_oracle_compute_unit_in_gbs,
            "odb_network_id": odb_network_id,
            "scan_listener_port_non_tls": scan_listener_port_non_tls,
            "scan_listener_port_tls": scan_listener_port_tls,
            "total_container_databases": total_container_databases,
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
        if description is not None:
            self._values["description"] = description
        if is_mtls_enabled_vm_cluster is not None:
            self._values["is_mtls_enabled_vm_cluster"] = is_mtls_enabled_vm_cluster
        if license_model is not None:
            self._values["license_model"] = license_model
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if time_zone is not None:
            self._values["time_zone"] = time_zone

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
    def autonomous_data_storage_size_in_tbs(self) -> jsii.Number:
        '''The data storage size allocated for Autonomous Databases in the Autonomous VM cluster, in TB.

        Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#autonomous_data_storage_size_in_tbs OdbCloudAutonomousVmCluster#autonomous_data_storage_size_in_tbs}
        '''
        result = self._values.get("autonomous_data_storage_size_in_tbs")
        assert result is not None, "Required property 'autonomous_data_storage_size_in_tbs' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cloud_exadata_infrastructure_id(self) -> builtins.str:
        '''Exadata infrastructure id. Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#cloud_exadata_infrastructure_id OdbCloudAutonomousVmCluster#cloud_exadata_infrastructure_id}
        '''
        result = self._values.get("cloud_exadata_infrastructure_id")
        assert result is not None, "Required property 'cloud_exadata_infrastructure_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cpu_core_count_per_node(self) -> jsii.Number:
        '''The number of CPU cores enabled per node in the Autonomous VM cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#cpu_core_count_per_node OdbCloudAutonomousVmCluster#cpu_core_count_per_node}
        '''
        result = self._values.get("cpu_core_count_per_node")
        assert result is not None, "Required property 'cpu_core_count_per_node' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def db_servers(self) -> typing.List[builtins.str]:
        '''The database servers in the Autonomous VM cluster. Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#db_servers OdbCloudAutonomousVmCluster#db_servers}
        '''
        result = self._values.get("db_servers")
        assert result is not None, "Required property 'db_servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name of the Autonomous VM cluster. Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#display_name OdbCloudAutonomousVmCluster#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def memory_per_oracle_compute_unit_in_gbs(self) -> jsii.Number:
        '''The amount of memory allocated per Oracle Compute Unit, in GB.

        Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#memory_per_oracle_compute_unit_in_gbs OdbCloudAutonomousVmCluster#memory_per_oracle_compute_unit_in_gbs}
        '''
        result = self._values.get("memory_per_oracle_compute_unit_in_gbs")
        assert result is not None, "Required property 'memory_per_oracle_compute_unit_in_gbs' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def odb_network_id(self) -> builtins.str:
        '''The unique identifier of the ODB network associated with this Autonomous VM Cluster.

        Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#odb_network_id OdbCloudAutonomousVmCluster#odb_network_id}
        '''
        result = self._values.get("odb_network_id")
        assert result is not None, "Required property 'odb_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scan_listener_port_non_tls(self) -> jsii.Number:
        '''The SCAN listener port for non-TLS (TCP) protocol.

        The default is 1521. Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#scan_listener_port_non_tls OdbCloudAutonomousVmCluster#scan_listener_port_non_tls}
        '''
        result = self._values.get("scan_listener_port_non_tls")
        assert result is not None, "Required property 'scan_listener_port_non_tls' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scan_listener_port_tls(self) -> jsii.Number:
        '''The SCAN listener port for TLS (TCP) protocol.

        The default is 2484. Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#scan_listener_port_tls OdbCloudAutonomousVmCluster#scan_listener_port_tls}
        '''
        result = self._values.get("scan_listener_port_tls")
        assert result is not None, "Required property 'scan_listener_port_tls' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def total_container_databases(self) -> jsii.Number:
        '''The total number of Autonomous Container Databases that can be created with the allocated local storage.

        Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#total_container_databases OdbCloudAutonomousVmCluster#total_container_databases}
        '''
        result = self._values.get("total_container_databases")
        assert result is not None, "Required property 'total_container_databases' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Autonomous VM cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#description OdbCloudAutonomousVmCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_mtls_enabled_vm_cluster(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether mutual TLS (mTLS) authentication is enabled for the Autonomous VM cluster.

        Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#is_mtls_enabled_vm_cluster OdbCloudAutonomousVmCluster#is_mtls_enabled_vm_cluster}
        '''
        result = self._values.get("is_mtls_enabled_vm_cluster")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def license_model(self) -> typing.Optional[builtins.str]:
        '''The license model for the Autonomous VM cluster.

        Valid values are LICENSE_INCLUDED or BRING_YOUR_OWN_LICENSE . Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#license_model OdbCloudAutonomousVmCluster#license_model}
        '''
        result = self._values.get("license_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudAutonomousVmClusterMaintenanceWindow"]]]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#maintenance_window OdbCloudAutonomousVmCluster#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudAutonomousVmClusterMaintenanceWindow"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#region OdbCloudAutonomousVmCluster#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#tags OdbCloudAutonomousVmCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OdbCloudAutonomousVmClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#timeouts OdbCloudAutonomousVmCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OdbCloudAutonomousVmClusterTimeouts"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone of the Autonomous VM cluster. Changing this will force terraform to create new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#time_zone OdbCloudAutonomousVmCluster#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudAutonomousVmClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={
        "preference": "preference",
        "days_of_week": "daysOfWeek",
        "hours_of_day": "hoursOfDay",
        "lead_time_in_weeks": "leadTimeInWeeks",
        "months": "months",
        "weeks_of_month": "weeksOfMonth",
    },
)
class OdbCloudAutonomousVmClusterMaintenanceWindow:
    def __init__(
        self,
        *,
        preference: builtins.str,
        days_of_week: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hours_of_day: typing.Optional[typing.Sequence[jsii.Number]] = None,
        lead_time_in_weeks: typing.Optional[jsii.Number] = None,
        months: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OdbCloudAutonomousVmClusterMaintenanceWindowMonths", typing.Dict[builtins.str, typing.Any]]]]] = None,
        weeks_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param preference: The preference for the maintenance window scheduling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#preference OdbCloudAutonomousVmCluster#preference}
        :param days_of_week: The days of the week when maintenance can be performed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#days_of_week OdbCloudAutonomousVmCluster#days_of_week}
        :param hours_of_day: The hours of the day when maintenance can be performed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#hours_of_day OdbCloudAutonomousVmCluster#hours_of_day}
        :param lead_time_in_weeks: The lead time in weeks before the maintenance window. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#lead_time_in_weeks OdbCloudAutonomousVmCluster#lead_time_in_weeks}
        :param months: The months when maintenance can be performed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#months OdbCloudAutonomousVmCluster#months}
        :param weeks_of_month: Indicates whether to skip release updates during maintenance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#weeks_of_month OdbCloudAutonomousVmCluster#weeks_of_month}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df1f2fd6b96a8077f231e74a5a73a865a75e91899951119ce8bc3d3a1c0e5ed0)
            check_type(argname="argument preference", value=preference, expected_type=type_hints["preference"])
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
            check_type(argname="argument hours_of_day", value=hours_of_day, expected_type=type_hints["hours_of_day"])
            check_type(argname="argument lead_time_in_weeks", value=lead_time_in_weeks, expected_type=type_hints["lead_time_in_weeks"])
            check_type(argname="argument months", value=months, expected_type=type_hints["months"])
            check_type(argname="argument weeks_of_month", value=weeks_of_month, expected_type=type_hints["weeks_of_month"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "preference": preference,
        }
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week
        if hours_of_day is not None:
            self._values["hours_of_day"] = hours_of_day
        if lead_time_in_weeks is not None:
            self._values["lead_time_in_weeks"] = lead_time_in_weeks
        if months is not None:
            self._values["months"] = months
        if weeks_of_month is not None:
            self._values["weeks_of_month"] = weeks_of_month

    @builtins.property
    def preference(self) -> builtins.str:
        '''The preference for the maintenance window scheduling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#preference OdbCloudAutonomousVmCluster#preference}
        '''
        result = self._values.get("preference")
        assert result is not None, "Required property 'preference' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def days_of_week(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek"]]]:
        '''The days of the week when maintenance can be performed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#days_of_week OdbCloudAutonomousVmCluster#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek"]]], result)

    @builtins.property
    def hours_of_day(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The hours of the day when maintenance can be performed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#hours_of_day OdbCloudAutonomousVmCluster#hours_of_day}
        '''
        result = self._values.get("hours_of_day")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def lead_time_in_weeks(self) -> typing.Optional[jsii.Number]:
        '''The lead time in weeks before the maintenance window.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#lead_time_in_weeks OdbCloudAutonomousVmCluster#lead_time_in_weeks}
        '''
        result = self._values.get("lead_time_in_weeks")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def months(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudAutonomousVmClusterMaintenanceWindowMonths"]]]:
        '''The months when maintenance can be performed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#months OdbCloudAutonomousVmCluster#months}
        '''
        result = self._values.get("months")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudAutonomousVmClusterMaintenanceWindowMonths"]]], result)

    @builtins.property
    def weeks_of_month(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Indicates whether to skip release updates during maintenance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#weeks_of_month OdbCloudAutonomousVmCluster#weeks_of_month}
        '''
        result = self._values.get("weeks_of_month")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudAutonomousVmClusterMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#name OdbCloudAutonomousVmCluster#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be09dd48730cebc3b668c29caca06c0412169dbbd9da722438843bf58f8fdf19)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#name OdbCloudAutonomousVmCluster#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeekList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeekList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58f06547e98987972ecae16533b7c29bef2c339b65cc494b7751fc9430c304b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeekOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__936349f60df7ec517dae837e773777faafa6bc05bb5cfcb270abd2fe0a7f46d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeekOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93467d29372d7ee092abb21dd69b014f53bfd14ca8bc473b98ce59f1f9aca89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6301946fc75932f06969d39b46039b128faf5af1d852340cf0b4be91877dcb3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db60b7161ccc8287a4f05118d33836144f61b0643c1abb3e9963933c04482849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1144e2234ae6b3b3a537da86663432c3363e3d75877d53cc3aa1b31c920d21d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeekOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeekOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__014f45e43bb35c3258daa808747e622fadbe3933c9d2ec8da2808316c4eb3664)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d50653c25eb3a24b130ac010e48577fc65c34b437c1c24ff587e798ad66f18f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc339204d309075fbc9eb0c14452bf17f36b51a5d07736ff7363fb417e5a48ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OdbCloudAutonomousVmClusterMaintenanceWindowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterMaintenanceWindowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b165bea5b09f812ac2c1ef72b38fdb66ba47cba1fa23fa999b6ed6c32c6b663)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbCloudAutonomousVmClusterMaintenanceWindowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44759dffa9ca75a77c51506b14b870f8fe49eb43a1ef62e73682161a14916845)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbCloudAutonomousVmClusterMaintenanceWindowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f910599354184c9f21bec029b7e7b8662a3b5751c974d3a35090fbffa62e17e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__876c672165051a3e974bfc1e122525a99cfef39a66239ba5b61c0e57d22ce713)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bf1fa01cd0549d45d20bdf18b7dd10721ccc6969de26b4354dd02270d8c60e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__586fead486824d3a02bce555e84f0db38aa6662112164577dcc9c1877753cc80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterMaintenanceWindowMonths",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OdbCloudAutonomousVmClusterMaintenanceWindowMonths:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#name OdbCloudAutonomousVmCluster#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df2ab83ff876f7414dddccdecba6d3cf6e14ca41b41c0ca58d8ce50d4e274c9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#name OdbCloudAutonomousVmCluster#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudAutonomousVmClusterMaintenanceWindowMonths(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbCloudAutonomousVmClusterMaintenanceWindowMonthsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterMaintenanceWindowMonthsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20b27a29cdffe09b9379ca912c0459a2e95dfe8d0f5cd6a1277b2e0eaa2b5bdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbCloudAutonomousVmClusterMaintenanceWindowMonthsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d80c2b6755abcc2b055218aa4d890eac42cbaaaf85291566b8bd86cf9a4a67)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbCloudAutonomousVmClusterMaintenanceWindowMonthsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14e1f87550242cd87cc477a48469c0dbd1264c2c7a5f83035f4ac88d2adb5a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce624baa196a5e5690c52928e32986c87fa89002d85a7f17683f879351c2b8e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abd3cf44c8dca92d5408fcd66bf989ba27b7545235a7b16948a03378f63514fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowMonths]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowMonths]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowMonths]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab8652fd5fcfbdeef232612edc968e0575053be4dcab543b923dd782747279c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OdbCloudAutonomousVmClusterMaintenanceWindowMonthsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterMaintenanceWindowMonthsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09d36366d706031d3b8473f995da5cca824ad7ece70b1020b4ee7fd35e99c318)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7700ac93f0632d92bdf3489e37f3906a330dcde15a054c1b3d8fb453a24b60c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindowMonths]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindowMonths]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindowMonths]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047af7d3b53735f077392768068cef6cfb61ffdaa7c6885947ea36aba8b25145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OdbCloudAutonomousVmClusterMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ef9089ec4f9fcc557a7ab1ef43da2825b7b0fdac800fd5e60102c75ce760d97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDaysOfWeek")
    def put_days_of_week(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980a6b458db45b686a4ce10d04e7d226ab6993b6db7e651b408d3498127146f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDaysOfWeek", [value]))

    @jsii.member(jsii_name="putMonths")
    def put_months(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudAutonomousVmClusterMaintenanceWindowMonths, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918a918b4d876eb7a9a5dfc03653006217b97260d211b437118990cc7c23529a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMonths", [value]))

    @jsii.member(jsii_name="resetDaysOfWeek")
    def reset_days_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfWeek", []))

    @jsii.member(jsii_name="resetHoursOfDay")
    def reset_hours_of_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHoursOfDay", []))

    @jsii.member(jsii_name="resetLeadTimeInWeeks")
    def reset_lead_time_in_weeks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLeadTimeInWeeks", []))

    @jsii.member(jsii_name="resetMonths")
    def reset_months(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonths", []))

    @jsii.member(jsii_name="resetWeeksOfMonth")
    def reset_weeks_of_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeksOfMonth", []))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(
        self,
    ) -> OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeekList:
        return typing.cast(OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeekList, jsii.get(self, "daysOfWeek"))

    @builtins.property
    @jsii.member(jsii_name="months")
    def months(self) -> OdbCloudAutonomousVmClusterMaintenanceWindowMonthsList:
        return typing.cast(OdbCloudAutonomousVmClusterMaintenanceWindowMonthsList, jsii.get(self, "months"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek]]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="hoursOfDayInput")
    def hours_of_day_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "hoursOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="leadTimeInWeeksInput")
    def lead_time_in_weeks_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "leadTimeInWeeksInput"))

    @builtins.property
    @jsii.member(jsii_name="monthsInput")
    def months_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowMonths]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowMonths]]], jsii.get(self, "monthsInput"))

    @builtins.property
    @jsii.member(jsii_name="preferenceInput")
    def preference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="weeksOfMonthInput")
    def weeks_of_month_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "weeksOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="hoursOfDay")
    def hours_of_day(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "hoursOfDay"))

    @hours_of_day.setter
    def hours_of_day(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c59fef510fe41cfd2a70756788100bc03f6544a7d601d44859fc4539de25b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hoursOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="leadTimeInWeeks")
    def lead_time_in_weeks(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "leadTimeInWeeks"))

    @lead_time_in_weeks.setter
    def lead_time_in_weeks(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e8b2a0be3622c7fa8dffe12e9846f6490a4ee33df5edce4803f9aca502969e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "leadTimeInWeeks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preference")
    def preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preference"))

    @preference.setter
    def preference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2eae54590ab15cb0a81efc8e7e914ed8340325d7a4c563dcfbf633642a25a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeksOfMonth")
    def weeks_of_month(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "weeksOfMonth"))

    @weeks_of_month.setter
    def weeks_of_month(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47fd755cdd00fb2190567a227543fa6c5813379960876cc14e08bafa56fa2a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeksOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindow]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindow]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindow]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1349107599ea1860b076c623db9be0c3b7f07794ca3c4571dde4eb413495501c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class OdbCloudAutonomousVmClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#create OdbCloudAutonomousVmCluster#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#delete OdbCloudAutonomousVmCluster#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#update OdbCloudAutonomousVmCluster#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d282d2da974443263f0ba5e103db18e7624bb855d231767ad3272b4098b5941c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#create OdbCloudAutonomousVmCluster#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#delete OdbCloudAutonomousVmCluster#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/odb_cloud_autonomous_vm_cluster#update OdbCloudAutonomousVmCluster#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudAutonomousVmClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbCloudAutonomousVmClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.odbCloudAutonomousVmCluster.OdbCloudAutonomousVmClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__348f5e1a6c2a273f40e4b6968a013b528237ac3c0058b3f4e170db8d5a83406c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9e879196fea51aea2cb645f5c2194410cefb1b14eaf2b20c32bfe446e988705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1862b6098c0dfb133789b46b398ebf3433da74bb0046ae1cba005b46acebab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605e075218fc5edd98067cbf0ade18f3f04e95869e74abf6052855751ba4bfbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c8a9af1262d3a4ef799c68661eb32ca521ebd4359fa4826b3e4c67e82d6ffb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OdbCloudAutonomousVmCluster",
    "OdbCloudAutonomousVmClusterConfig",
    "OdbCloudAutonomousVmClusterMaintenanceWindow",
    "OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek",
    "OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeekList",
    "OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeekOutputReference",
    "OdbCloudAutonomousVmClusterMaintenanceWindowList",
    "OdbCloudAutonomousVmClusterMaintenanceWindowMonths",
    "OdbCloudAutonomousVmClusterMaintenanceWindowMonthsList",
    "OdbCloudAutonomousVmClusterMaintenanceWindowMonthsOutputReference",
    "OdbCloudAutonomousVmClusterMaintenanceWindowOutputReference",
    "OdbCloudAutonomousVmClusterTimeouts",
    "OdbCloudAutonomousVmClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c3edcfd2f8f68e05db4de02d71429dab609537c00639af333eb80745a834bf9e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    autonomous_data_storage_size_in_tbs: jsii.Number,
    cloud_exadata_infrastructure_id: builtins.str,
    cpu_core_count_per_node: jsii.Number,
    db_servers: typing.Sequence[builtins.str],
    display_name: builtins.str,
    memory_per_oracle_compute_unit_in_gbs: jsii.Number,
    odb_network_id: builtins.str,
    scan_listener_port_non_tls: jsii.Number,
    scan_listener_port_tls: jsii.Number,
    total_container_databases: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    is_mtls_enabled_vm_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    license_model: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudAutonomousVmClusterMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OdbCloudAutonomousVmClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__2eed355ef42cbfc5efc3a1df929397a55fb55e6aae2e913858a875f7f0cb8b49(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c51bc5d563da3b2b0d0ab3a55f710091a0492724f9e5681c134fd9fcbeb754c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudAutonomousVmClusterMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2cbacc20a9e4316801c2e2db84cce4374fd7e7fa4a4098a81a502d6ead1521(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7809c4a80ab9b887f934731c9e46fa1c30ac96fc250fba6403b4755075aca6ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7320edf3f64a35268cf4a0d10fa421afb47664b935b765df41bb2d0a2dbf83(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f065b4961e78f9b8f8f45dc222dfbe847064e5ac9811e2975e6ddfd048776aac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade2d6f438bbdfc61379eeb13a20cee461b3e1b1f739a1cfd1676eefa6c7379d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a55e038df465fb2fb59c3bd083d95830569a40bacf5e1be6bef6c7bada62100(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2887d37a7bd0cae1664832729eb610f6a98facf2d6f144c6ed59eea63eb443f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9281cd9f10c9f40f160e179d517973ca683a18513fa87c4ea57e5a8bd016c2b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed04c9e56e16f70877541774d974f0702846bdf4c71238ca016e9ba9361cec4e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320ab22eeb8816694140f210d881682d1b8fa0194c3bb6b9dc8c64559297fd04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0483853b0fd0e53ff53b4fbe8debb8442f22dd5277d479c82d23b173630571(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325b46414bd2ed5d78fd8aaed9a932c8cc1a96e9ca12028436ccc58288473788(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5907373ff87b2872238f99c87c8802c6966338fb38fbad795ab3f9fec48acac2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4042d4fd37f6f59c206f8e5ba17010fb4d822f0861e7748bc4e88a5c4492fcc5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee56d992c4e565e9e7eb937e299cc12561b5d4bf84c1fdcc5783c959cb0f4ec2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13bbcb5ebb1149176c3fcca55ebc551aad0a82e2fd35405049df156a7d706f20(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede7b42370598dc58181aab088bd44521646ae35bce10adef214a6dcba47e738(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autonomous_data_storage_size_in_tbs: jsii.Number,
    cloud_exadata_infrastructure_id: builtins.str,
    cpu_core_count_per_node: jsii.Number,
    db_servers: typing.Sequence[builtins.str],
    display_name: builtins.str,
    memory_per_oracle_compute_unit_in_gbs: jsii.Number,
    odb_network_id: builtins.str,
    scan_listener_port_non_tls: jsii.Number,
    scan_listener_port_tls: jsii.Number,
    total_container_databases: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    is_mtls_enabled_vm_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    license_model: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudAutonomousVmClusterMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OdbCloudAutonomousVmClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1f2fd6b96a8077f231e74a5a73a865a75e91899951119ce8bc3d3a1c0e5ed0(
    *,
    preference: builtins.str,
    days_of_week: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hours_of_day: typing.Optional[typing.Sequence[jsii.Number]] = None,
    lead_time_in_weeks: typing.Optional[jsii.Number] = None,
    months: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudAutonomousVmClusterMaintenanceWindowMonths, typing.Dict[builtins.str, typing.Any]]]]] = None,
    weeks_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be09dd48730cebc3b668c29caca06c0412169dbbd9da722438843bf58f8fdf19(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f06547e98987972ecae16533b7c29bef2c339b65cc494b7751fc9430c304b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936349f60df7ec517dae837e773777faafa6bc05bb5cfcb270abd2fe0a7f46d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93467d29372d7ee092abb21dd69b014f53bfd14ca8bc473b98ce59f1f9aca89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6301946fc75932f06969d39b46039b128faf5af1d852340cf0b4be91877dcb3c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db60b7161ccc8287a4f05118d33836144f61b0643c1abb3e9963933c04482849(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1144e2234ae6b3b3a537da86663432c3363e3d75877d53cc3aa1b31c920d21d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014f45e43bb35c3258daa808747e622fadbe3933c9d2ec8da2808316c4eb3664(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50653c25eb3a24b130ac010e48577fc65c34b437c1c24ff587e798ad66f18f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc339204d309075fbc9eb0c14452bf17f36b51a5d07736ff7363fb417e5a48ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b165bea5b09f812ac2c1ef72b38fdb66ba47cba1fa23fa999b6ed6c32c6b663(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44759dffa9ca75a77c51506b14b870f8fe49eb43a1ef62e73682161a14916845(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f910599354184c9f21bec029b7e7b8662a3b5751c974d3a35090fbffa62e17e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876c672165051a3e974bfc1e122525a99cfef39a66239ba5b61c0e57d22ce713(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf1fa01cd0549d45d20bdf18b7dd10721ccc6969de26b4354dd02270d8c60e2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586fead486824d3a02bce555e84f0db38aa6662112164577dcc9c1877753cc80(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df2ab83ff876f7414dddccdecba6d3cf6e14ca41b41c0ca58d8ce50d4e274c9(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b27a29cdffe09b9379ca912c0459a2e95dfe8d0f5cd6a1277b2e0eaa2b5bdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d80c2b6755abcc2b055218aa4d890eac42cbaaaf85291566b8bd86cf9a4a67(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14e1f87550242cd87cc477a48469c0dbd1264c2c7a5f83035f4ac88d2adb5a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce624baa196a5e5690c52928e32986c87fa89002d85a7f17683f879351c2b8e4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd3cf44c8dca92d5408fcd66bf989ba27b7545235a7b16948a03378f63514fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab8652fd5fcfbdeef232612edc968e0575053be4dcab543b923dd782747279c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudAutonomousVmClusterMaintenanceWindowMonths]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d36366d706031d3b8473f995da5cca824ad7ece70b1020b4ee7fd35e99c318(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7700ac93f0632d92bdf3489e37f3906a330dcde15a054c1b3d8fb453a24b60c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047af7d3b53735f077392768068cef6cfb61ffdaa7c6885947ea36aba8b25145(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindowMonths]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef9089ec4f9fcc557a7ab1ef43da2825b7b0fdac800fd5e60102c75ce760d97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980a6b458db45b686a4ce10d04e7d226ab6993b6db7e651b408d3498127146f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudAutonomousVmClusterMaintenanceWindowDaysOfWeek, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918a918b4d876eb7a9a5dfc03653006217b97260d211b437118990cc7c23529a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudAutonomousVmClusterMaintenanceWindowMonths, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c59fef510fe41cfd2a70756788100bc03f6544a7d601d44859fc4539de25b1a(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e8b2a0be3622c7fa8dffe12e9846f6490a4ee33df5edce4803f9aca502969e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2eae54590ab15cb0a81efc8e7e914ed8340325d7a4c563dcfbf633642a25a4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fd755cdd00fb2190567a227543fa6c5813379960876cc14e08bafa56fa2a1c(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1349107599ea1860b076c623db9be0c3b7f07794ca3c4571dde4eb413495501c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterMaintenanceWindow]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d282d2da974443263f0ba5e103db18e7624bb855d231767ad3272b4098b5941c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348f5e1a6c2a273f40e4b6968a013b528237ac3c0058b3f4e170db8d5a83406c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e879196fea51aea2cb645f5c2194410cefb1b14eaf2b20c32bfe446e988705(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1862b6098c0dfb133789b46b398ebf3433da74bb0046ae1cba005b46acebab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605e075218fc5edd98067cbf0ade18f3f04e95869e74abf6052855751ba4bfbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8a9af1262d3a4ef799c68661eb32ca521ebd4359fa4826b3e4c67e82d6ffb1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudAutonomousVmClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
