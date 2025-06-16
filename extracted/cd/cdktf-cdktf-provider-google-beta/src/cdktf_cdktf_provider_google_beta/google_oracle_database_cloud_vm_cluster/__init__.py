r'''
# `google_oracle_database_cloud_vm_cluster`

Refer to the Terraform Registry for docs: [`google_oracle_database_cloud_vm_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster).
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


class GoogleOracleDatabaseCloudVmCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudVmCluster.GoogleOracleDatabaseCloudVmCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster google_oracle_database_cloud_vm_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backup_subnet_cidr: builtins.str,
        cidr: builtins.str,
        cloud_vm_cluster_id: builtins.str,
        exadata_infrastructure: builtins.str,
        location: builtins.str,
        network: builtins.str,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union["GoogleOracleDatabaseCloudVmClusterProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleOracleDatabaseCloudVmClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster google_oracle_database_cloud_vm_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backup_subnet_cidr: CIDR range of the backup subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#backup_subnet_cidr GoogleOracleDatabaseCloudVmCluster#backup_subnet_cidr}
        :param cidr: Network settings. CIDR to use for cluster IP allocation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cidr GoogleOracleDatabaseCloudVmCluster#cidr}
        :param cloud_vm_cluster_id: The ID of the VM Cluster to create. This value is restricted to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63 characters in length. The value must start with a letter and end with a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cloud_vm_cluster_id GoogleOracleDatabaseCloudVmCluster#cloud_vm_cluster_id}
        :param exadata_infrastructure: The name of the Exadata Infrastructure resource on which VM cluster resource is created, in the following format: projects/{project}/locations/{region}/cloudExadataInfrastuctures/{cloud_extradata_infrastructure}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#exadata_infrastructure GoogleOracleDatabaseCloudVmCluster#exadata_infrastructure}
        :param location: Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/DbNode'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#location GoogleOracleDatabaseCloudVmCluster#location}
        :param network: The name of the VPC network. Format: projects/{project}/global/networks/{network}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#network GoogleOracleDatabaseCloudVmCluster#network}
        :param deletion_protection: Whether Terraform will be prevented from destroying the cluster. Deleting this cluster via terraform destroy or terraform apply will only succeed if this field is false in the Terraform state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#deletion_protection GoogleOracleDatabaseCloudVmCluster#deletion_protection}
        :param display_name: User friendly name for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#display_name GoogleOracleDatabaseCloudVmCluster#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#id GoogleOracleDatabaseCloudVmCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels or tags associated with the VM Cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#labels GoogleOracleDatabaseCloudVmCluster#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#project GoogleOracleDatabaseCloudVmCluster#project}.
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#properties GoogleOracleDatabaseCloudVmCluster#properties}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#timeouts GoogleOracleDatabaseCloudVmCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cef4451f3dad81eb81ad4e98dd1bd7d039c60089c76b4300c4b83d6df9d75b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleOracleDatabaseCloudVmClusterConfig(
            backup_subnet_cidr=backup_subnet_cidr,
            cidr=cidr,
            cloud_vm_cluster_id=cloud_vm_cluster_id,
            exadata_infrastructure=exadata_infrastructure,
            location=location,
            network=network,
            deletion_protection=deletion_protection,
            display_name=display_name,
            id=id,
            labels=labels,
            project=project,
            properties=properties,
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
        '''Generates CDKTF code for importing a GoogleOracleDatabaseCloudVmCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleOracleDatabaseCloudVmCluster to import.
        :param import_from_id: The id of the existing GoogleOracleDatabaseCloudVmCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleOracleDatabaseCloudVmCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eae00fb67fa1198d82eae3b24a7ea38a9d508f889fe83bffe646233a4d26e58)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        *,
        cpu_core_count: jsii.Number,
        license_type: builtins.str,
        cluster_name: typing.Optional[builtins.str] = None,
        data_storage_size_tb: typing.Optional[jsii.Number] = None,
        db_node_storage_size_gb: typing.Optional[jsii.Number] = None,
        db_server_ocids: typing.Optional[typing.Sequence[builtins.str]] = None,
        diagnostics_data_collection_options: typing.Optional[typing.Union["GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_redundancy: typing.Optional[builtins.str] = None,
        gi_version: typing.Optional[builtins.str] = None,
        hostname_prefix: typing.Optional[builtins.str] = None,
        local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_size_gb: typing.Optional[jsii.Number] = None,
        node_count: typing.Optional[jsii.Number] = None,
        ocpu_count: typing.Optional[jsii.Number] = None,
        sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        time_zone: typing.Optional[typing.Union["GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cpu_core_count: Number of enabled CPU cores. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cpu_core_count GoogleOracleDatabaseCloudVmCluster#cpu_core_count}
        :param license_type: License type of VM Cluster. Possible values: LICENSE_TYPE_UNSPECIFIED LICENSE_INCLUDED BRING_YOUR_OWN_LICENSE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#license_type GoogleOracleDatabaseCloudVmCluster#license_type}
        :param cluster_name: OCI Cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cluster_name GoogleOracleDatabaseCloudVmCluster#cluster_name}
        :param data_storage_size_tb: The data disk group size to be allocated in TBs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#data_storage_size_tb GoogleOracleDatabaseCloudVmCluster#data_storage_size_tb}
        :param db_node_storage_size_gb: Local storage per VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#db_node_storage_size_gb GoogleOracleDatabaseCloudVmCluster#db_node_storage_size_gb}
        :param db_server_ocids: OCID of database servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#db_server_ocids GoogleOracleDatabaseCloudVmCluster#db_server_ocids}
        :param diagnostics_data_collection_options: diagnostics_data_collection_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#diagnostics_data_collection_options GoogleOracleDatabaseCloudVmCluster#diagnostics_data_collection_options}
        :param disk_redundancy: The type of redundancy. Possible values: DISK_REDUNDANCY_UNSPECIFIED HIGH NORMAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#disk_redundancy GoogleOracleDatabaseCloudVmCluster#disk_redundancy}
        :param gi_version: Grid Infrastructure Version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#gi_version GoogleOracleDatabaseCloudVmCluster#gi_version}
        :param hostname_prefix: Prefix for VM cluster host names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#hostname_prefix GoogleOracleDatabaseCloudVmCluster#hostname_prefix}
        :param local_backup_enabled: Use local backup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#local_backup_enabled GoogleOracleDatabaseCloudVmCluster#local_backup_enabled}
        :param memory_size_gb: Memory allocated in GBs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#memory_size_gb GoogleOracleDatabaseCloudVmCluster#memory_size_gb}
        :param node_count: Number of database servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#node_count GoogleOracleDatabaseCloudVmCluster#node_count}
        :param ocpu_count: OCPU count per VM. Minimum is 0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#ocpu_count GoogleOracleDatabaseCloudVmCluster#ocpu_count}
        :param sparse_diskgroup_enabled: Use exadata sparse snapshots. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#sparse_diskgroup_enabled GoogleOracleDatabaseCloudVmCluster#sparse_diskgroup_enabled}
        :param ssh_public_keys: SSH public keys to be stored with cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#ssh_public_keys GoogleOracleDatabaseCloudVmCluster#ssh_public_keys}
        :param time_zone: time_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#time_zone GoogleOracleDatabaseCloudVmCluster#time_zone}
        '''
        value = GoogleOracleDatabaseCloudVmClusterProperties(
            cpu_core_count=cpu_core_count,
            license_type=license_type,
            cluster_name=cluster_name,
            data_storage_size_tb=data_storage_size_tb,
            db_node_storage_size_gb=db_node_storage_size_gb,
            db_server_ocids=db_server_ocids,
            diagnostics_data_collection_options=diagnostics_data_collection_options,
            disk_redundancy=disk_redundancy,
            gi_version=gi_version,
            hostname_prefix=hostname_prefix,
            local_backup_enabled=local_backup_enabled,
            memory_size_gb=memory_size_gb,
            node_count=node_count,
            ocpu_count=ocpu_count,
            sparse_diskgroup_enabled=sparse_diskgroup_enabled,
            ssh_public_keys=ssh_public_keys,
            time_zone=time_zone,
        )

        return typing.cast(None, jsii.invoke(self, "putProperties", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#create GoogleOracleDatabaseCloudVmCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#delete GoogleOracleDatabaseCloudVmCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#update GoogleOracleDatabaseCloudVmCluster#update}.
        '''
        value = GoogleOracleDatabaseCloudVmClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="gcpOracleZone")
    def gcp_oracle_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpOracleZone"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> "GoogleOracleDatabaseCloudVmClusterPropertiesOutputReference":
        return typing.cast("GoogleOracleDatabaseCloudVmClusterPropertiesOutputReference", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleOracleDatabaseCloudVmClusterTimeoutsOutputReference":
        return typing.cast("GoogleOracleDatabaseCloudVmClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backupSubnetCidrInput")
    def backup_subnet_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupSubnetCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrInput")
    def cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cidrInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudVmClusterIdInput")
    def cloud_vm_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudVmClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="exadataInfrastructureInput")
    def exadata_infrastructure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exadataInfrastructureInput"))

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
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional["GoogleOracleDatabaseCloudVmClusterProperties"]:
        return typing.cast(typing.Optional["GoogleOracleDatabaseCloudVmClusterProperties"], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOracleDatabaseCloudVmClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOracleDatabaseCloudVmClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="backupSubnetCidr")
    def backup_subnet_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupSubnetCidr"))

    @backup_subnet_cidr.setter
    def backup_subnet_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10438cc4256c266fcc07c2cf672b4f1690e6f391c54f21b9a9e80a4ce525196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupSubnetCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @cidr.setter
    def cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e822316db9773aaa8d0b4a32ad44b287227cd25d3cd2d8026df68938435bcfd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudVmClusterId")
    def cloud_vm_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudVmClusterId"))

    @cloud_vm_cluster_id.setter
    def cloud_vm_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337cc6a87cfd65089823d23894f764f1a7de8e5d67d4acc8ef66bb95e4357c08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudVmClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f737bb5293ba21b415b153374b74f9079ff141328934b7708456a52bbc0eebd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ecbc5e706d9f5544dda44de13e3e01ca66803e1da0bace700ae4bd7fca2d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exadataInfrastructure")
    def exadata_infrastructure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exadataInfrastructure"))

    @exadata_infrastructure.setter
    def exadata_infrastructure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b998d6e4ef46f5ddda6dda3491140e8587bdecce2cc87772f957efe6b194869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exadataInfrastructure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4533ac01424763b22244b1d98dd99e5245260bdf1b9a106fdbd9730cc94f6c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966fafbccff3ac44daa5af6fcf8a47e296908d836610f9bf172fa9ce934c6f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb0e8fafba3ee6d5cede0ebda82606b0079bf378fc6cae5eb08ecc1add7642b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca6e6cebf88ddf68ba9ac0024b3461e9385cfdfaa5bc53a2a023979658e4f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea1f6358adb342df97f953be5aacb81b173d54f92a23a8744a6def06bee05bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudVmCluster.GoogleOracleDatabaseCloudVmClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backup_subnet_cidr": "backupSubnetCidr",
        "cidr": "cidr",
        "cloud_vm_cluster_id": "cloudVmClusterId",
        "exadata_infrastructure": "exadataInfrastructure",
        "location": "location",
        "network": "network",
        "deletion_protection": "deletionProtection",
        "display_name": "displayName",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "properties": "properties",
        "timeouts": "timeouts",
    },
)
class GoogleOracleDatabaseCloudVmClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backup_subnet_cidr: builtins.str,
        cidr: builtins.str,
        cloud_vm_cluster_id: builtins.str,
        exadata_infrastructure: builtins.str,
        location: builtins.str,
        network: builtins.str,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union["GoogleOracleDatabaseCloudVmClusterProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleOracleDatabaseCloudVmClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backup_subnet_cidr: CIDR range of the backup subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#backup_subnet_cidr GoogleOracleDatabaseCloudVmCluster#backup_subnet_cidr}
        :param cidr: Network settings. CIDR to use for cluster IP allocation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cidr GoogleOracleDatabaseCloudVmCluster#cidr}
        :param cloud_vm_cluster_id: The ID of the VM Cluster to create. This value is restricted to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63 characters in length. The value must start with a letter and end with a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cloud_vm_cluster_id GoogleOracleDatabaseCloudVmCluster#cloud_vm_cluster_id}
        :param exadata_infrastructure: The name of the Exadata Infrastructure resource on which VM cluster resource is created, in the following format: projects/{project}/locations/{region}/cloudExadataInfrastuctures/{cloud_extradata_infrastructure}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#exadata_infrastructure GoogleOracleDatabaseCloudVmCluster#exadata_infrastructure}
        :param location: Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/DbNode'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#location GoogleOracleDatabaseCloudVmCluster#location}
        :param network: The name of the VPC network. Format: projects/{project}/global/networks/{network}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#network GoogleOracleDatabaseCloudVmCluster#network}
        :param deletion_protection: Whether Terraform will be prevented from destroying the cluster. Deleting this cluster via terraform destroy or terraform apply will only succeed if this field is false in the Terraform state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#deletion_protection GoogleOracleDatabaseCloudVmCluster#deletion_protection}
        :param display_name: User friendly name for this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#display_name GoogleOracleDatabaseCloudVmCluster#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#id GoogleOracleDatabaseCloudVmCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels or tags associated with the VM Cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#labels GoogleOracleDatabaseCloudVmCluster#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#project GoogleOracleDatabaseCloudVmCluster#project}.
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#properties GoogleOracleDatabaseCloudVmCluster#properties}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#timeouts GoogleOracleDatabaseCloudVmCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(properties, dict):
            properties = GoogleOracleDatabaseCloudVmClusterProperties(**properties)
        if isinstance(timeouts, dict):
            timeouts = GoogleOracleDatabaseCloudVmClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e16f423bae5997a5194690b2695051218a5644f5ea6c43c65bdf7ef236445d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backup_subnet_cidr", value=backup_subnet_cidr, expected_type=type_hints["backup_subnet_cidr"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument cloud_vm_cluster_id", value=cloud_vm_cluster_id, expected_type=type_hints["cloud_vm_cluster_id"])
            check_type(argname="argument exadata_infrastructure", value=exadata_infrastructure, expected_type=type_hints["exadata_infrastructure"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_subnet_cidr": backup_subnet_cidr,
            "cidr": cidr,
            "cloud_vm_cluster_id": cloud_vm_cluster_id,
            "exadata_infrastructure": exadata_infrastructure,
            "location": location,
            "network": network,
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
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if properties is not None:
            self._values["properties"] = properties
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
    def backup_subnet_cidr(self) -> builtins.str:
        '''CIDR range of the backup subnet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#backup_subnet_cidr GoogleOracleDatabaseCloudVmCluster#backup_subnet_cidr}
        '''
        result = self._values.get("backup_subnet_cidr")
        assert result is not None, "Required property 'backup_subnet_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cidr(self) -> builtins.str:
        '''Network settings. CIDR to use for cluster IP allocation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cidr GoogleOracleDatabaseCloudVmCluster#cidr}
        '''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_vm_cluster_id(self) -> builtins.str:
        '''The ID of the VM Cluster to create.

        This value is restricted
        to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63
        characters in length. The value must start with a letter and end with
        a letter or a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cloud_vm_cluster_id GoogleOracleDatabaseCloudVmCluster#cloud_vm_cluster_id}
        '''
        result = self._values.get("cloud_vm_cluster_id")
        assert result is not None, "Required property 'cloud_vm_cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exadata_infrastructure(self) -> builtins.str:
        '''The name of the Exadata Infrastructure resource on which VM cluster resource is created, in the following format: projects/{project}/locations/{region}/cloudExadataInfrastuctures/{cloud_extradata_infrastructure}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#exadata_infrastructure GoogleOracleDatabaseCloudVmCluster#exadata_infrastructure}
        '''
        result = self._values.get("exadata_infrastructure")
        assert result is not None, "Required property 'exadata_infrastructure' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/DbNode'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#location GoogleOracleDatabaseCloudVmCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''The name of the VPC network. Format: projects/{project}/global/networks/{network}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#network GoogleOracleDatabaseCloudVmCluster#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Terraform will be prevented from destroying the cluster.

        Deleting this cluster via terraform destroy or terraform apply will only succeed if this field is false in the Terraform state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#deletion_protection GoogleOracleDatabaseCloudVmCluster#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User friendly name for this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#display_name GoogleOracleDatabaseCloudVmCluster#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#id GoogleOracleDatabaseCloudVmCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels or tags associated with the VM Cluster.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#labels GoogleOracleDatabaseCloudVmCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#project GoogleOracleDatabaseCloudVmCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional["GoogleOracleDatabaseCloudVmClusterProperties"]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#properties GoogleOracleDatabaseCloudVmCluster#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional["GoogleOracleDatabaseCloudVmClusterProperties"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleOracleDatabaseCloudVmClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#timeouts GoogleOracleDatabaseCloudVmCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleOracleDatabaseCloudVmClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseCloudVmClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudVmCluster.GoogleOracleDatabaseCloudVmClusterProperties",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_core_count": "cpuCoreCount",
        "license_type": "licenseType",
        "cluster_name": "clusterName",
        "data_storage_size_tb": "dataStorageSizeTb",
        "db_node_storage_size_gb": "dbNodeStorageSizeGb",
        "db_server_ocids": "dbServerOcids",
        "diagnostics_data_collection_options": "diagnosticsDataCollectionOptions",
        "disk_redundancy": "diskRedundancy",
        "gi_version": "giVersion",
        "hostname_prefix": "hostnamePrefix",
        "local_backup_enabled": "localBackupEnabled",
        "memory_size_gb": "memorySizeGb",
        "node_count": "nodeCount",
        "ocpu_count": "ocpuCount",
        "sparse_diskgroup_enabled": "sparseDiskgroupEnabled",
        "ssh_public_keys": "sshPublicKeys",
        "time_zone": "timeZone",
    },
)
class GoogleOracleDatabaseCloudVmClusterProperties:
    def __init__(
        self,
        *,
        cpu_core_count: jsii.Number,
        license_type: builtins.str,
        cluster_name: typing.Optional[builtins.str] = None,
        data_storage_size_tb: typing.Optional[jsii.Number] = None,
        db_node_storage_size_gb: typing.Optional[jsii.Number] = None,
        db_server_ocids: typing.Optional[typing.Sequence[builtins.str]] = None,
        diagnostics_data_collection_options: typing.Optional[typing.Union["GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_redundancy: typing.Optional[builtins.str] = None,
        gi_version: typing.Optional[builtins.str] = None,
        hostname_prefix: typing.Optional[builtins.str] = None,
        local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        memory_size_gb: typing.Optional[jsii.Number] = None,
        node_count: typing.Optional[jsii.Number] = None,
        ocpu_count: typing.Optional[jsii.Number] = None,
        sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        time_zone: typing.Optional[typing.Union["GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cpu_core_count: Number of enabled CPU cores. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cpu_core_count GoogleOracleDatabaseCloudVmCluster#cpu_core_count}
        :param license_type: License type of VM Cluster. Possible values: LICENSE_TYPE_UNSPECIFIED LICENSE_INCLUDED BRING_YOUR_OWN_LICENSE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#license_type GoogleOracleDatabaseCloudVmCluster#license_type}
        :param cluster_name: OCI Cluster name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cluster_name GoogleOracleDatabaseCloudVmCluster#cluster_name}
        :param data_storage_size_tb: The data disk group size to be allocated in TBs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#data_storage_size_tb GoogleOracleDatabaseCloudVmCluster#data_storage_size_tb}
        :param db_node_storage_size_gb: Local storage per VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#db_node_storage_size_gb GoogleOracleDatabaseCloudVmCluster#db_node_storage_size_gb}
        :param db_server_ocids: OCID of database servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#db_server_ocids GoogleOracleDatabaseCloudVmCluster#db_server_ocids}
        :param diagnostics_data_collection_options: diagnostics_data_collection_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#diagnostics_data_collection_options GoogleOracleDatabaseCloudVmCluster#diagnostics_data_collection_options}
        :param disk_redundancy: The type of redundancy. Possible values: DISK_REDUNDANCY_UNSPECIFIED HIGH NORMAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#disk_redundancy GoogleOracleDatabaseCloudVmCluster#disk_redundancy}
        :param gi_version: Grid Infrastructure Version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#gi_version GoogleOracleDatabaseCloudVmCluster#gi_version}
        :param hostname_prefix: Prefix for VM cluster host names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#hostname_prefix GoogleOracleDatabaseCloudVmCluster#hostname_prefix}
        :param local_backup_enabled: Use local backup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#local_backup_enabled GoogleOracleDatabaseCloudVmCluster#local_backup_enabled}
        :param memory_size_gb: Memory allocated in GBs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#memory_size_gb GoogleOracleDatabaseCloudVmCluster#memory_size_gb}
        :param node_count: Number of database servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#node_count GoogleOracleDatabaseCloudVmCluster#node_count}
        :param ocpu_count: OCPU count per VM. Minimum is 0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#ocpu_count GoogleOracleDatabaseCloudVmCluster#ocpu_count}
        :param sparse_diskgroup_enabled: Use exadata sparse snapshots. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#sparse_diskgroup_enabled GoogleOracleDatabaseCloudVmCluster#sparse_diskgroup_enabled}
        :param ssh_public_keys: SSH public keys to be stored with cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#ssh_public_keys GoogleOracleDatabaseCloudVmCluster#ssh_public_keys}
        :param time_zone: time_zone block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#time_zone GoogleOracleDatabaseCloudVmCluster#time_zone}
        '''
        if isinstance(diagnostics_data_collection_options, dict):
            diagnostics_data_collection_options = GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions(**diagnostics_data_collection_options)
        if isinstance(time_zone, dict):
            time_zone = GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone(**time_zone)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e3825b1eac2315c6c0253aae6c13269b28d7c1ec3dd1cc148f37eb56d0a627)
            check_type(argname="argument cpu_core_count", value=cpu_core_count, expected_type=type_hints["cpu_core_count"])
            check_type(argname="argument license_type", value=license_type, expected_type=type_hints["license_type"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument data_storage_size_tb", value=data_storage_size_tb, expected_type=type_hints["data_storage_size_tb"])
            check_type(argname="argument db_node_storage_size_gb", value=db_node_storage_size_gb, expected_type=type_hints["db_node_storage_size_gb"])
            check_type(argname="argument db_server_ocids", value=db_server_ocids, expected_type=type_hints["db_server_ocids"])
            check_type(argname="argument diagnostics_data_collection_options", value=diagnostics_data_collection_options, expected_type=type_hints["diagnostics_data_collection_options"])
            check_type(argname="argument disk_redundancy", value=disk_redundancy, expected_type=type_hints["disk_redundancy"])
            check_type(argname="argument gi_version", value=gi_version, expected_type=type_hints["gi_version"])
            check_type(argname="argument hostname_prefix", value=hostname_prefix, expected_type=type_hints["hostname_prefix"])
            check_type(argname="argument local_backup_enabled", value=local_backup_enabled, expected_type=type_hints["local_backup_enabled"])
            check_type(argname="argument memory_size_gb", value=memory_size_gb, expected_type=type_hints["memory_size_gb"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument ocpu_count", value=ocpu_count, expected_type=type_hints["ocpu_count"])
            check_type(argname="argument sparse_diskgroup_enabled", value=sparse_diskgroup_enabled, expected_type=type_hints["sparse_diskgroup_enabled"])
            check_type(argname="argument ssh_public_keys", value=ssh_public_keys, expected_type=type_hints["ssh_public_keys"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu_core_count": cpu_core_count,
            "license_type": license_type,
        }
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if data_storage_size_tb is not None:
            self._values["data_storage_size_tb"] = data_storage_size_tb
        if db_node_storage_size_gb is not None:
            self._values["db_node_storage_size_gb"] = db_node_storage_size_gb
        if db_server_ocids is not None:
            self._values["db_server_ocids"] = db_server_ocids
        if diagnostics_data_collection_options is not None:
            self._values["diagnostics_data_collection_options"] = diagnostics_data_collection_options
        if disk_redundancy is not None:
            self._values["disk_redundancy"] = disk_redundancy
        if gi_version is not None:
            self._values["gi_version"] = gi_version
        if hostname_prefix is not None:
            self._values["hostname_prefix"] = hostname_prefix
        if local_backup_enabled is not None:
            self._values["local_backup_enabled"] = local_backup_enabled
        if memory_size_gb is not None:
            self._values["memory_size_gb"] = memory_size_gb
        if node_count is not None:
            self._values["node_count"] = node_count
        if ocpu_count is not None:
            self._values["ocpu_count"] = ocpu_count
        if sparse_diskgroup_enabled is not None:
            self._values["sparse_diskgroup_enabled"] = sparse_diskgroup_enabled
        if ssh_public_keys is not None:
            self._values["ssh_public_keys"] = ssh_public_keys
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def cpu_core_count(self) -> jsii.Number:
        '''Number of enabled CPU cores.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cpu_core_count GoogleOracleDatabaseCloudVmCluster#cpu_core_count}
        '''
        result = self._values.get("cpu_core_count")
        assert result is not None, "Required property 'cpu_core_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def license_type(self) -> builtins.str:
        '''License type of VM Cluster.   Possible values:  LICENSE_TYPE_UNSPECIFIED LICENSE_INCLUDED BRING_YOUR_OWN_LICENSE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#license_type GoogleOracleDatabaseCloudVmCluster#license_type}
        '''
        result = self._values.get("license_type")
        assert result is not None, "Required property 'license_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''OCI Cluster name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#cluster_name GoogleOracleDatabaseCloudVmCluster#cluster_name}
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_storage_size_tb(self) -> typing.Optional[jsii.Number]:
        '''The data disk group size to be allocated in TBs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#data_storage_size_tb GoogleOracleDatabaseCloudVmCluster#data_storage_size_tb}
        '''
        result = self._values.get("data_storage_size_tb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_node_storage_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Local storage per VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#db_node_storage_size_gb GoogleOracleDatabaseCloudVmCluster#db_node_storage_size_gb}
        '''
        result = self._values.get("db_node_storage_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_server_ocids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''OCID of database servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#db_server_ocids GoogleOracleDatabaseCloudVmCluster#db_server_ocids}
        '''
        result = self._values.get("db_server_ocids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def diagnostics_data_collection_options(
        self,
    ) -> typing.Optional["GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions"]:
        '''diagnostics_data_collection_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#diagnostics_data_collection_options GoogleOracleDatabaseCloudVmCluster#diagnostics_data_collection_options}
        '''
        result = self._values.get("diagnostics_data_collection_options")
        return typing.cast(typing.Optional["GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions"], result)

    @builtins.property
    def disk_redundancy(self) -> typing.Optional[builtins.str]:
        '''The type of redundancy.   Possible values:  DISK_REDUNDANCY_UNSPECIFIED HIGH NORMAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#disk_redundancy GoogleOracleDatabaseCloudVmCluster#disk_redundancy}
        '''
        result = self._values.get("disk_redundancy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gi_version(self) -> typing.Optional[builtins.str]:
        '''Grid Infrastructure Version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#gi_version GoogleOracleDatabaseCloudVmCluster#gi_version}
        '''
        result = self._values.get("gi_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hostname_prefix(self) -> typing.Optional[builtins.str]:
        '''Prefix for VM cluster host names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#hostname_prefix GoogleOracleDatabaseCloudVmCluster#hostname_prefix}
        '''
        result = self._values.get("hostname_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use local backup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#local_backup_enabled GoogleOracleDatabaseCloudVmCluster#local_backup_enabled}
        '''
        result = self._values.get("local_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def memory_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Memory allocated in GBs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#memory_size_gb GoogleOracleDatabaseCloudVmCluster#memory_size_gb}
        '''
        result = self._values.get("memory_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Number of database servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#node_count GoogleOracleDatabaseCloudVmCluster#node_count}
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ocpu_count(self) -> typing.Optional[jsii.Number]:
        '''OCPU count per VM. Minimum is 0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#ocpu_count GoogleOracleDatabaseCloudVmCluster#ocpu_count}
        '''
        result = self._values.get("ocpu_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sparse_diskgroup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use exadata sparse snapshots.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#sparse_diskgroup_enabled GoogleOracleDatabaseCloudVmCluster#sparse_diskgroup_enabled}
        '''
        result = self._values.get("sparse_diskgroup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssh_public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''SSH public keys to be stored with cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#ssh_public_keys GoogleOracleDatabaseCloudVmCluster#ssh_public_keys}
        '''
        result = self._values.get("ssh_public_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def time_zone(
        self,
    ) -> typing.Optional["GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone"]:
        '''time_zone block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#time_zone GoogleOracleDatabaseCloudVmCluster#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional["GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseCloudVmClusterProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudVmCluster.GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "diagnostics_events_enabled": "diagnosticsEventsEnabled",
        "health_monitoring_enabled": "healthMonitoringEnabled",
        "incident_logs_enabled": "incidentLogsEnabled",
    },
)
class GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions:
    def __init__(
        self,
        *,
        diagnostics_events_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        health_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        incident_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param diagnostics_events_enabled: Indicates whether diagnostic collection is enabled for the VM cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#diagnostics_events_enabled GoogleOracleDatabaseCloudVmCluster#diagnostics_events_enabled}
        :param health_monitoring_enabled: Indicates whether health monitoring is enabled for the VM cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#health_monitoring_enabled GoogleOracleDatabaseCloudVmCluster#health_monitoring_enabled}
        :param incident_logs_enabled: Indicates whether incident logs and trace collection are enabled for the VM cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#incident_logs_enabled GoogleOracleDatabaseCloudVmCluster#incident_logs_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb028d3c8a97d0cc330f4554320c547a9c6279daa010d6f6d10dde8ce390b04e)
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
        '''Indicates whether diagnostic collection is enabled for the VM cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#diagnostics_events_enabled GoogleOracleDatabaseCloudVmCluster#diagnostics_events_enabled}
        '''
        result = self._values.get("diagnostics_events_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def health_monitoring_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether health monitoring is enabled for the VM cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#health_monitoring_enabled GoogleOracleDatabaseCloudVmCluster#health_monitoring_enabled}
        '''
        result = self._values.get("health_monitoring_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def incident_logs_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether incident logs and trace collection are enabled for the VM cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#incident_logs_enabled GoogleOracleDatabaseCloudVmCluster#incident_logs_enabled}
        '''
        result = self._values.get("incident_logs_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudVmCluster.GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5abb20315271015148b0617464f71fbd8a3f0e2e5018a9e9094c067c19467e4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97ddd0daec21cd1c929b5e77225bd53481049eac59589de120cbc41c6cebfa74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8df03dc95edae6c61cc39953ad92f93567b67a2cbe974a13003a687925fdb2a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0997b2d9f22990da38fbc331843acb24a49603e1838d7641f23b51c51c18247f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "incidentLogsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__920d942c6e7afd0edf81074c6030db7f1bde5be01b5276c1ac3584f9c7dc21b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOracleDatabaseCloudVmClusterPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudVmCluster.GoogleOracleDatabaseCloudVmClusterPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e74a1028e4d4eb3cfb6527458fbbc25c4b4e95ca07851c142d40c56089835fb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDiagnosticsDataCollectionOptions")
    def put_diagnostics_data_collection_options(
        self,
        *,
        diagnostics_events_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        health_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        incident_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param diagnostics_events_enabled: Indicates whether diagnostic collection is enabled for the VM cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#diagnostics_events_enabled GoogleOracleDatabaseCloudVmCluster#diagnostics_events_enabled}
        :param health_monitoring_enabled: Indicates whether health monitoring is enabled for the VM cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#health_monitoring_enabled GoogleOracleDatabaseCloudVmCluster#health_monitoring_enabled}
        :param incident_logs_enabled: Indicates whether incident logs and trace collection are enabled for the VM cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#incident_logs_enabled GoogleOracleDatabaseCloudVmCluster#incident_logs_enabled}
        '''
        value = GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions(
            diagnostics_events_enabled=diagnostics_events_enabled,
            health_monitoring_enabled=health_monitoring_enabled,
            incident_logs_enabled=incident_logs_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putDiagnosticsDataCollectionOptions", [value]))

    @jsii.member(jsii_name="putTimeZone")
    def put_time_zone(self, *, id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param id: IANA Time Zone Database time zone, e.g. "America/New_York". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#id GoogleOracleDatabaseCloudVmCluster#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone(id=id)

        return typing.cast(None, jsii.invoke(self, "putTimeZone", [value]))

    @jsii.member(jsii_name="resetClusterName")
    def reset_cluster_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterName", []))

    @jsii.member(jsii_name="resetDataStorageSizeTb")
    def reset_data_storage_size_tb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStorageSizeTb", []))

    @jsii.member(jsii_name="resetDbNodeStorageSizeGb")
    def reset_db_node_storage_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbNodeStorageSizeGb", []))

    @jsii.member(jsii_name="resetDbServerOcids")
    def reset_db_server_ocids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbServerOcids", []))

    @jsii.member(jsii_name="resetDiagnosticsDataCollectionOptions")
    def reset_diagnostics_data_collection_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiagnosticsDataCollectionOptions", []))

    @jsii.member(jsii_name="resetDiskRedundancy")
    def reset_disk_redundancy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskRedundancy", []))

    @jsii.member(jsii_name="resetGiVersion")
    def reset_gi_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGiVersion", []))

    @jsii.member(jsii_name="resetHostnamePrefix")
    def reset_hostname_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostnamePrefix", []))

    @jsii.member(jsii_name="resetLocalBackupEnabled")
    def reset_local_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalBackupEnabled", []))

    @jsii.member(jsii_name="resetMemorySizeGb")
    def reset_memory_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemorySizeGb", []))

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @jsii.member(jsii_name="resetOcpuCount")
    def reset_ocpu_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOcpuCount", []))

    @jsii.member(jsii_name="resetSparseDiskgroupEnabled")
    def reset_sparse_diskgroup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparseDiskgroupEnabled", []))

    @jsii.member(jsii_name="resetSshPublicKeys")
    def reset_ssh_public_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshPublicKeys", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @builtins.property
    @jsii.member(jsii_name="compartmentId")
    def compartment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compartmentId"))

    @builtins.property
    @jsii.member(jsii_name="diagnosticsDataCollectionOptions")
    def diagnostics_data_collection_options(
        self,
    ) -> GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptionsOutputReference:
        return typing.cast(GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptionsOutputReference, jsii.get(self, "diagnosticsDataCollectionOptions"))

    @builtins.property
    @jsii.member(jsii_name="dnsListenerIp")
    def dns_listener_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsListenerIp"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="ocid")
    def ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ocid"))

    @builtins.property
    @jsii.member(jsii_name="ociUrl")
    def oci_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociUrl"))

    @builtins.property
    @jsii.member(jsii_name="scanDns")
    def scan_dns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scanDns"))

    @builtins.property
    @jsii.member(jsii_name="scanDnsRecordId")
    def scan_dns_record_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scanDnsRecordId"))

    @builtins.property
    @jsii.member(jsii_name="scanIpIds")
    def scan_ip_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scanIpIds"))

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTcp")
    def scan_listener_port_tcp(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scanListenerPortTcp"))

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTcpSsl")
    def scan_listener_port_tcp_ssl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scanListenerPortTcpSsl"))

    @builtins.property
    @jsii.member(jsii_name="shape")
    def shape(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shape"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="storageSizeGb")
    def storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="systemVersion")
    def system_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemVersion"))

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(
        self,
    ) -> "GoogleOracleDatabaseCloudVmClusterPropertiesTimeZoneOutputReference":
        return typing.cast("GoogleOracleDatabaseCloudVmClusterPropertiesTimeZoneOutputReference", jsii.get(self, "timeZone"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCoreCountInput")
    def cpu_core_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuCoreCountInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeTbInput")
    def data_storage_size_tb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataStorageSizeTbInput"))

    @builtins.property
    @jsii.member(jsii_name="dbNodeStorageSizeGbInput")
    def db_node_storage_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dbNodeStorageSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="dbServerOcidsInput")
    def db_server_ocids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dbServerOcidsInput"))

    @builtins.property
    @jsii.member(jsii_name="diagnosticsDataCollectionOptionsInput")
    def diagnostics_data_collection_options_input(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions], jsii.get(self, "diagnosticsDataCollectionOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskRedundancyInput")
    def disk_redundancy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskRedundancyInput"))

    @builtins.property
    @jsii.member(jsii_name="giVersionInput")
    def gi_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "giVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnamePrefixInput")
    def hostname_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseTypeInput")
    def license_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="localBackupEnabledInput")
    def local_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeGbInput")
    def memory_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="ocpuCountInput")
    def ocpu_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ocpuCountInput"))

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
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(
        self,
    ) -> typing.Optional["GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone"]:
        return typing.cast(typing.Optional["GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone"], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5229859914535a0feeac666098247e78bed37942758ae9db35291a9eeb6bdf14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCoreCount")
    def cpu_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCoreCount"))

    @cpu_core_count.setter
    def cpu_core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efc91cf6504256603e39d4134358b17609e71a693734aaa1c0cade61a84309b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeTb")
    def data_storage_size_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeTb"))

    @data_storage_size_tb.setter
    def data_storage_size_tb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9589c277cd67fc274971a27c3331b57f21703b11e111814e3df6e52f88b71f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStorageSizeTb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbNodeStorageSizeGb")
    def db_node_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dbNodeStorageSizeGb"))

    @db_node_storage_size_gb.setter
    def db_node_storage_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5edc5a1b9826acf95c1ecc80eb81bdc4673bc5bc3ae7881251d0cac2829917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbNodeStorageSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbServerOcids")
    def db_server_ocids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dbServerOcids"))

    @db_server_ocids.setter
    def db_server_ocids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506fc69fa9707db8c356f9426c91422d3968580895c29396d905f40bef7fa6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbServerOcids", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskRedundancy")
    def disk_redundancy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskRedundancy"))

    @disk_redundancy.setter
    def disk_redundancy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d62da0d327491fbd4c5fba11077d2b4f6b8d456014f3f67b233d4f831f75f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskRedundancy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="giVersion")
    def gi_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "giVersion"))

    @gi_version.setter
    def gi_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e04e1f03fa7a798f40c9cfc5590635817e778b2f3b8fd3ba091bb0310412352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "giVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostnamePrefix")
    def hostname_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostnamePrefix"))

    @hostname_prefix.setter
    def hostname_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036e1a0435c29e12ebec84f8ec1de114748cea3c2839945ed70cf985d7375b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostnamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @license_type.setter
    def license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691746413a8a4ed728b765808b988ab549fc141be9972c989036cc7fa0ffd747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseType", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__1bb0dc4350b87c305fb7338d8bcdbdbebe3b87f12de164d6769c89324451c33f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localBackupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySizeGb")
    def memory_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeGb"))

    @memory_size_gb.setter
    def memory_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f35f1f7dd172bdbdd2037236c1760aa9e4764710a91c98b4e29eb94e04b402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6407c1739f782eb402180cbe5568e6517be7210be0ebd086537ef5054362588a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ocpuCount")
    def ocpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ocpuCount"))

    @ocpu_count.setter
    def ocpu_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9dee08ef40f9dd97a2a37c4415dd248a0f4a74bfd1dbdb22d899dbd726b44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ocpuCount", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__cbbc466d779434cd15b069594b8c1ce5e8aaf61129aa4b0df06bc56dce2483f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparseDiskgroupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeys")
    def ssh_public_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshPublicKeys"))

    @ssh_public_keys.setter
    def ssh_public_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8d20c21a3c4723010707f8880f711f9510dbc112d573cc4c16d85f1d48edb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseCloudVmClusterProperties]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseCloudVmClusterProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseCloudVmClusterProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8a9dfb32938a3dda8beece4a3af25ccfa8e5dfa80a586f27491db09973877a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudVmCluster.GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone:
    def __init__(self, *, id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param id: IANA Time Zone Database time zone, e.g. "America/New_York". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#id GoogleOracleDatabaseCloudVmCluster#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43bf1db8499db326f706af2af62e11614fdf8196e279ca143cfa5fe1c6f313ce)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''IANA Time Zone Database time zone, e.g. "America/New_York".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#id GoogleOracleDatabaseCloudVmCluster#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseCloudVmClusterPropertiesTimeZoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudVmCluster.GoogleOracleDatabaseCloudVmClusterPropertiesTimeZoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__593dda012d6376af2131b5e983dcd44ba1b8d42da27f00b6a5ff75c68a125161)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da00c4175712e38315e64e0bf6412c16da66b88dbbdb529bf5aa257dd56c95c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone]:
        return typing.cast(typing.Optional[GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32c8aa9eee485b927fe293aa8f128438d20d68bce0366a06ba9c07095ef9bc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudVmCluster.GoogleOracleDatabaseCloudVmClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleOracleDatabaseCloudVmClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#create GoogleOracleDatabaseCloudVmCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#delete GoogleOracleDatabaseCloudVmCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#update GoogleOracleDatabaseCloudVmCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff68bc6d07516fbee3040164778bed7dd9d478962d00a499fbfd62c1be4b272)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#create GoogleOracleDatabaseCloudVmCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#delete GoogleOracleDatabaseCloudVmCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_oracle_database_cloud_vm_cluster#update GoogleOracleDatabaseCloudVmCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOracleDatabaseCloudVmClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOracleDatabaseCloudVmClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOracleDatabaseCloudVmCluster.GoogleOracleDatabaseCloudVmClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06b447ed62a8df9912aa93835dce35c99869784cdc6781eb384058745170ff10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff3024cc31eb6e59763bb245c5e2c40cc47a392da1c76ace70967cb1a062232a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef709ed46e88af42cd22a4160827007e04825ee607ff166774afe4e9dcd5518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de1aabeb99e1ff884c7b3b7578227323cf626d9ef01ab98066f796e00b7f5c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudVmClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudVmClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudVmClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245d216b898ed3be7005e72ac00975d1f62eebf7bea4f0cebd993fa1f0692121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleOracleDatabaseCloudVmCluster",
    "GoogleOracleDatabaseCloudVmClusterConfig",
    "GoogleOracleDatabaseCloudVmClusterProperties",
    "GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions",
    "GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptionsOutputReference",
    "GoogleOracleDatabaseCloudVmClusterPropertiesOutputReference",
    "GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone",
    "GoogleOracleDatabaseCloudVmClusterPropertiesTimeZoneOutputReference",
    "GoogleOracleDatabaseCloudVmClusterTimeouts",
    "GoogleOracleDatabaseCloudVmClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8cef4451f3dad81eb81ad4e98dd1bd7d039c60089c76b4300c4b83d6df9d75b4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backup_subnet_cidr: builtins.str,
    cidr: builtins.str,
    cloud_vm_cluster_id: builtins.str,
    exadata_infrastructure: builtins.str,
    location: builtins.str,
    network: builtins.str,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[GoogleOracleDatabaseCloudVmClusterProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleOracleDatabaseCloudVmClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9eae00fb67fa1198d82eae3b24a7ea38a9d508f889fe83bffe646233a4d26e58(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10438cc4256c266fcc07c2cf672b4f1690e6f391c54f21b9a9e80a4ce525196(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e822316db9773aaa8d0b4a32ad44b287227cd25d3cd2d8026df68938435bcfd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337cc6a87cfd65089823d23894f764f1a7de8e5d67d4acc8ef66bb95e4357c08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f737bb5293ba21b415b153374b74f9079ff141328934b7708456a52bbc0eebd5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ecbc5e706d9f5544dda44de13e3e01ca66803e1da0bace700ae4bd7fca2d2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b998d6e4ef46f5ddda6dda3491140e8587bdecce2cc87772f957efe6b194869(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4533ac01424763b22244b1d98dd99e5245260bdf1b9a106fdbd9730cc94f6c5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966fafbccff3ac44daa5af6fcf8a47e296908d836610f9bf172fa9ce934c6f7c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb0e8fafba3ee6d5cede0ebda82606b0079bf378fc6cae5eb08ecc1add7642b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca6e6cebf88ddf68ba9ac0024b3461e9385cfdfaa5bc53a2a023979658e4f80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea1f6358adb342df97f953be5aacb81b173d54f92a23a8744a6def06bee05bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e16f423bae5997a5194690b2695051218a5644f5ea6c43c65bdf7ef236445d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backup_subnet_cidr: builtins.str,
    cidr: builtins.str,
    cloud_vm_cluster_id: builtins.str,
    exadata_infrastructure: builtins.str,
    location: builtins.str,
    network: builtins.str,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[GoogleOracleDatabaseCloudVmClusterProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleOracleDatabaseCloudVmClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e3825b1eac2315c6c0253aae6c13269b28d7c1ec3dd1cc148f37eb56d0a627(
    *,
    cpu_core_count: jsii.Number,
    license_type: builtins.str,
    cluster_name: typing.Optional[builtins.str] = None,
    data_storage_size_tb: typing.Optional[jsii.Number] = None,
    db_node_storage_size_gb: typing.Optional[jsii.Number] = None,
    db_server_ocids: typing.Optional[typing.Sequence[builtins.str]] = None,
    diagnostics_data_collection_options: typing.Optional[typing.Union[GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_redundancy: typing.Optional[builtins.str] = None,
    gi_version: typing.Optional[builtins.str] = None,
    hostname_prefix: typing.Optional[builtins.str] = None,
    local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    memory_size_gb: typing.Optional[jsii.Number] = None,
    node_count: typing.Optional[jsii.Number] = None,
    ocpu_count: typing.Optional[jsii.Number] = None,
    sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    time_zone: typing.Optional[typing.Union[GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb028d3c8a97d0cc330f4554320c547a9c6279daa010d6f6d10dde8ce390b04e(
    *,
    diagnostics_events_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    health_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    incident_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abb20315271015148b0617464f71fbd8a3f0e2e5018a9e9094c067c19467e4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ddd0daec21cd1c929b5e77225bd53481049eac59589de120cbc41c6cebfa74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df03dc95edae6c61cc39953ad92f93567b67a2cbe974a13003a687925fdb2a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0997b2d9f22990da38fbc331843acb24a49603e1838d7641f23b51c51c18247f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920d942c6e7afd0edf81074c6030db7f1bde5be01b5276c1ac3584f9c7dc21b9(
    value: typing.Optional[GoogleOracleDatabaseCloudVmClusterPropertiesDiagnosticsDataCollectionOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74a1028e4d4eb3cfb6527458fbbc25c4b4e95ca07851c142d40c56089835fb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5229859914535a0feeac666098247e78bed37942758ae9db35291a9eeb6bdf14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efc91cf6504256603e39d4134358b17609e71a693734aaa1c0cade61a84309b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9589c277cd67fc274971a27c3331b57f21703b11e111814e3df6e52f88b71f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5edc5a1b9826acf95c1ecc80eb81bdc4673bc5bc3ae7881251d0cac2829917(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506fc69fa9707db8c356f9426c91422d3968580895c29396d905f40bef7fa6f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d62da0d327491fbd4c5fba11077d2b4f6b8d456014f3f67b233d4f831f75f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e04e1f03fa7a798f40c9cfc5590635817e778b2f3b8fd3ba091bb0310412352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036e1a0435c29e12ebec84f8ec1de114748cea3c2839945ed70cf985d7375b6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691746413a8a4ed728b765808b988ab549fc141be9972c989036cc7fa0ffd747(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb0dc4350b87c305fb7338d8bcdbdbebe3b87f12de164d6769c89324451c33f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f35f1f7dd172bdbdd2037236c1760aa9e4764710a91c98b4e29eb94e04b402(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6407c1739f782eb402180cbe5568e6517be7210be0ebd086537ef5054362588a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9dee08ef40f9dd97a2a37c4415dd248a0f4a74bfd1dbdb22d899dbd726b44e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbbc466d779434cd15b069594b8c1ce5e8aaf61129aa4b0df06bc56dce2483f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8d20c21a3c4723010707f8880f711f9510dbc112d573cc4c16d85f1d48edb6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8a9dfb32938a3dda8beece4a3af25ccfa8e5dfa80a586f27491db09973877a(
    value: typing.Optional[GoogleOracleDatabaseCloudVmClusterProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bf1db8499db326f706af2af62e11614fdf8196e279ca143cfa5fe1c6f313ce(
    *,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593dda012d6376af2131b5e983dcd44ba1b8d42da27f00b6a5ff75c68a125161(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da00c4175712e38315e64e0bf6412c16da66b88dbbdb529bf5aa257dd56c95c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c8aa9eee485b927fe293aa8f128438d20d68bce0366a06ba9c07095ef9bc20(
    value: typing.Optional[GoogleOracleDatabaseCloudVmClusterPropertiesTimeZone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff68bc6d07516fbee3040164778bed7dd9d478962d00a499fbfd62c1be4b272(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b447ed62a8df9912aa93835dce35c99869784cdc6781eb384058745170ff10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3024cc31eb6e59763bb245c5e2c40cc47a392da1c76ace70967cb1a062232a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef709ed46e88af42cd22a4160827007e04825ee607ff166774afe4e9dcd5518(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de1aabeb99e1ff884c7b3b7578227323cf626d9ef01ab98066f796e00b7f5c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245d216b898ed3be7005e72ac00975d1f62eebf7bea4f0cebd993fa1f0692121(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOracleDatabaseCloudVmClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
