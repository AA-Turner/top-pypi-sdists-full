r'''
# `google_netapp_storage_pool`

Refer to the Terraform Registry for docs: [`google_netapp_storage_pool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool).
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


class NetappStoragePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappStoragePool.NetappStoragePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool google_netapp_storage_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        capacity_gib: builtins.str,
        location: builtins.str,
        name: builtins.str,
        network: builtins.str,
        service_level: builtins.str,
        active_directory: typing.Optional[builtins.str] = None,
        allow_auto_tiering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_performance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_config: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        ldap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        replica_zone: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetappStoragePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        total_iops: typing.Optional[builtins.str] = None,
        total_throughput_mibps: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool google_netapp_storage_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capacity_gib: Capacity of the storage pool (in GiB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#capacity_gib NetappStoragePool#capacity_gib}
        :param location: Name of the location. For zonal Flex pools specify a zone name, in all other cases a region name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#location NetappStoragePool#location}
        :param name: The resource name of the storage pool. Needs to be unique per location/region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#name NetappStoragePool#name}
        :param network: VPC network name with format: 'projects/{{project}}/global/networks/{{network}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#network NetappStoragePool#network}
        :param service_level: Service level of the storage pool. Possible values: ["PREMIUM", "EXTREME", "STANDARD", "FLEX"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#service_level NetappStoragePool#service_level}
        :param active_directory: Specifies the Active Directory policy to be used. Format: 'projects/{{project}}/locations/{{location}}/activeDirectories/{{name}}'. The policy needs to be in the same location as the storage pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#active_directory NetappStoragePool#active_directory}
        :param allow_auto_tiering: Optional. True if the storage pool supports Auto Tiering enabled volumes. Default is false. Auto-tiering can be enabled after storage pool creation but it can't be disabled once enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#allow_auto_tiering NetappStoragePool#allow_auto_tiering}
        :param custom_performance_enabled: Optional. True if using Independent Scaling of capacity and performance (Hyperdisk). Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#custom_performance_enabled NetappStoragePool#custom_performance_enabled}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#description NetappStoragePool#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#id NetappStoragePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_config: Specifies the CMEK policy to be used for volume encryption. Format: 'projects/{{project}}/locations/{{location}}/kmsConfigs/{{name}}'. The policy needs to be in the same location as the storage pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#kms_config NetappStoragePool#kms_config}
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#labels NetappStoragePool#labels}
        :param ldap_enabled: When enabled, the volumes uses Active Directory as LDAP name service for UID/GID lookups. Required to enable extended group support for NFSv3, using security identifiers for NFSv4.1 or principal names for kerberized NFSv4.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#ldap_enabled NetappStoragePool#ldap_enabled}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#project NetappStoragePool#project}.
        :param replica_zone: Specifies the replica zone for regional Flex pools. 'zone' and 'replica_zone' values can be swapped to initiate a `zone switch <https://cloud.google.com/netapp/volumes/docs/configure-and-use/storage-pools/edit-or-delete-storage-pool#switch_active_and_replica_zones>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#replica_zone NetappStoragePool#replica_zone}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#timeouts NetappStoragePool#timeouts}
        :param total_iops: Optional. Custom Performance Total IOPS of the pool If not provided, it will be calculated based on the totalThroughputMibps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#total_iops NetappStoragePool#total_iops}
        :param total_throughput_mibps: Optional. Custom Performance Total Throughput of the pool (in MiB/s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#total_throughput_mibps NetappStoragePool#total_throughput_mibps}
        :param zone: Specifies the active zone for regional Flex pools. 'zone' and 'replica_zone' values can be swapped to initiate a `zone switch <https://cloud.google.com/netapp/volumes/docs/configure-and-use/storage-pools/edit-or-delete-storage-pool#switch_active_and_replica_zones>`_. If you want to create a zonal Flex pool, specify a zone name for 'location' and omit 'zone'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#zone NetappStoragePool#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd008b4be379c37d0eaad0a24c5b59b9e9a986cb3431b1828a6e93194b484db0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetappStoragePoolConfig(
            capacity_gib=capacity_gib,
            location=location,
            name=name,
            network=network,
            service_level=service_level,
            active_directory=active_directory,
            allow_auto_tiering=allow_auto_tiering,
            custom_performance_enabled=custom_performance_enabled,
            description=description,
            id=id,
            kms_config=kms_config,
            labels=labels,
            ldap_enabled=ldap_enabled,
            project=project,
            replica_zone=replica_zone,
            timeouts=timeouts,
            total_iops=total_iops,
            total_throughput_mibps=total_throughput_mibps,
            zone=zone,
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
        '''Generates CDKTF code for importing a NetappStoragePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetappStoragePool to import.
        :param import_from_id: The id of the existing NetappStoragePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetappStoragePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125cceda74504f1aa60f409cd2f3cd10f633ee75b57e3916f3a45eb9ff56921b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#create NetappStoragePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#delete NetappStoragePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#update NetappStoragePool#update}.
        '''
        value = NetappStoragePoolTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetActiveDirectory")
    def reset_active_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectory", []))

    @jsii.member(jsii_name="resetAllowAutoTiering")
    def reset_allow_auto_tiering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAutoTiering", []))

    @jsii.member(jsii_name="resetCustomPerformanceEnabled")
    def reset_custom_performance_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomPerformanceEnabled", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsConfig")
    def reset_kms_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsConfig", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLdapEnabled")
    def reset_ldap_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLdapEnabled", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReplicaZone")
    def reset_replica_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaZone", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTotalIops")
    def reset_total_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotalIops", []))

    @jsii.member(jsii_name="resetTotalThroughputMibps")
    def reset_total_throughput_mibps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotalThroughputMibps", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetappStoragePoolTimeoutsOutputReference":
        return typing.cast("NetappStoragePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="volumeCapacityGib")
    def volume_capacity_gib(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeCapacityGib"))

    @builtins.property
    @jsii.member(jsii_name="volumeCount")
    def volume_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeCount"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryInput")
    def active_directory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activeDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAutoTieringInput")
    def allow_auto_tiering_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAutoTieringInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityGibInput")
    def capacity_gib_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityGibInput"))

    @builtins.property
    @jsii.member(jsii_name="customPerformanceEnabledInput")
    def custom_performance_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customPerformanceEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsConfigInput")
    def kms_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="ldapEnabledInput")
    def ldap_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ldapEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaZoneInput")
    def replica_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicaZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceLevelInput")
    def service_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappStoragePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappStoragePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="totalIopsInput")
    def total_iops_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "totalIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="totalThroughputMibpsInput")
    def total_throughput_mibps_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "totalThroughputMibpsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectory")
    def active_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activeDirectory"))

    @active_directory.setter
    def active_directory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c2ad50be44462fe477c392660931320a86a36033098fc59d6782f338ee7090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowAutoTiering")
    def allow_auto_tiering(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAutoTiering"))

    @allow_auto_tiering.setter
    def allow_auto_tiering(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88c031230548a2a6f62124fdc4106f497a649cbe25a7f59f9e15f949f995c07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAutoTiering", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capacityGib")
    def capacity_gib(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityGib"))

    @capacity_gib.setter
    def capacity_gib(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fd82dff63ba33e498cde52f9c2ea66d7656180cb51292dcaeb8b14490bf61c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customPerformanceEnabled")
    def custom_performance_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customPerformanceEnabled"))

    @custom_performance_enabled.setter
    def custom_performance_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f546d45caa2d76e016b107ac811ad6f51054f94a445c0a72ceb2ba5c1c8703a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customPerformanceEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a30d7f083700483af811d9aac307bd270744c4de468009cbf82e39ceb6db56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c926ee5d799b850ff5b959daf764fb7a7edb466b9006d958ca51dc50a29c47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsConfig")
    def kms_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsConfig"))

    @kms_config.setter
    def kms_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3037a9911bb8a4948b79f44b586d60de6be46170301b706f373f13b12cde9f33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d3f8ccc0f57090e64d990cad3d99ae71f22b753292d96ddd4cd4ee9b3797d92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ldapEnabled")
    def ldap_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ldapEnabled"))

    @ldap_enabled.setter
    def ldap_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a963c053bb20372cbde76e131d38a0536a266a5919a982bbfbe0e0b05edd0765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ldapEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15da61bb1a206f3c1572f80b3f5b4e4de2180a3199b2e18761216f73602d06ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2903c2a94a4d96687ebb3a340e29cd7cea7331a99769993d1f22556de11a1ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a4ca1ab0136937b356187736a184179237abcf46c5ad72a016a87cfb6a9be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e312772d6bf8991c1caf869390dd0e3f2b76057f551ab60b3f1e05c469ae0750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaZone")
    def replica_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicaZone"))

    @replica_zone.setter
    def replica_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca5036ecae7822ad3437b7661f4da908098cd58053a4290a66a9fed73d5d2929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceLevel")
    def service_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceLevel"))

    @service_level.setter
    def service_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d021bd2ad0fb498868acd8f75ecbb1a7664708a4d81c0609308fa60d7d6cde9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalIops")
    def total_iops(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalIops"))

    @total_iops.setter
    def total_iops(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a5b60f8c754988f3681b5105069058c7382ca93541a29fe495b73b52b91cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="totalThroughputMibps")
    def total_throughput_mibps(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalThroughputMibps"))

    @total_throughput_mibps.setter
    def total_throughput_mibps(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f77998026b718b0a7ac37df88d8b7129e94bb868b8729bf1ecee621d746fe72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalThroughputMibps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5701ef5e34eca9f209c2acdfc1c4563b50b1747b5c02c6aa29cd25c079bf5d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappStoragePool.NetappStoragePoolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "capacity_gib": "capacityGib",
        "location": "location",
        "name": "name",
        "network": "network",
        "service_level": "serviceLevel",
        "active_directory": "activeDirectory",
        "allow_auto_tiering": "allowAutoTiering",
        "custom_performance_enabled": "customPerformanceEnabled",
        "description": "description",
        "id": "id",
        "kms_config": "kmsConfig",
        "labels": "labels",
        "ldap_enabled": "ldapEnabled",
        "project": "project",
        "replica_zone": "replicaZone",
        "timeouts": "timeouts",
        "total_iops": "totalIops",
        "total_throughput_mibps": "totalThroughputMibps",
        "zone": "zone",
    },
)
class NetappStoragePoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        capacity_gib: builtins.str,
        location: builtins.str,
        name: builtins.str,
        network: builtins.str,
        service_level: builtins.str,
        active_directory: typing.Optional[builtins.str] = None,
        allow_auto_tiering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_performance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_config: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        ldap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        replica_zone: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetappStoragePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        total_iops: typing.Optional[builtins.str] = None,
        total_throughput_mibps: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capacity_gib: Capacity of the storage pool (in GiB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#capacity_gib NetappStoragePool#capacity_gib}
        :param location: Name of the location. For zonal Flex pools specify a zone name, in all other cases a region name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#location NetappStoragePool#location}
        :param name: The resource name of the storage pool. Needs to be unique per location/region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#name NetappStoragePool#name}
        :param network: VPC network name with format: 'projects/{{project}}/global/networks/{{network}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#network NetappStoragePool#network}
        :param service_level: Service level of the storage pool. Possible values: ["PREMIUM", "EXTREME", "STANDARD", "FLEX"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#service_level NetappStoragePool#service_level}
        :param active_directory: Specifies the Active Directory policy to be used. Format: 'projects/{{project}}/locations/{{location}}/activeDirectories/{{name}}'. The policy needs to be in the same location as the storage pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#active_directory NetappStoragePool#active_directory}
        :param allow_auto_tiering: Optional. True if the storage pool supports Auto Tiering enabled volumes. Default is false. Auto-tiering can be enabled after storage pool creation but it can't be disabled once enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#allow_auto_tiering NetappStoragePool#allow_auto_tiering}
        :param custom_performance_enabled: Optional. True if using Independent Scaling of capacity and performance (Hyperdisk). Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#custom_performance_enabled NetappStoragePool#custom_performance_enabled}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#description NetappStoragePool#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#id NetappStoragePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_config: Specifies the CMEK policy to be used for volume encryption. Format: 'projects/{{project}}/locations/{{location}}/kmsConfigs/{{name}}'. The policy needs to be in the same location as the storage pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#kms_config NetappStoragePool#kms_config}
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#labels NetappStoragePool#labels}
        :param ldap_enabled: When enabled, the volumes uses Active Directory as LDAP name service for UID/GID lookups. Required to enable extended group support for NFSv3, using security identifiers for NFSv4.1 or principal names for kerberized NFSv4.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#ldap_enabled NetappStoragePool#ldap_enabled}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#project NetappStoragePool#project}.
        :param replica_zone: Specifies the replica zone for regional Flex pools. 'zone' and 'replica_zone' values can be swapped to initiate a `zone switch <https://cloud.google.com/netapp/volumes/docs/configure-and-use/storage-pools/edit-or-delete-storage-pool#switch_active_and_replica_zones>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#replica_zone NetappStoragePool#replica_zone}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#timeouts NetappStoragePool#timeouts}
        :param total_iops: Optional. Custom Performance Total IOPS of the pool If not provided, it will be calculated based on the totalThroughputMibps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#total_iops NetappStoragePool#total_iops}
        :param total_throughput_mibps: Optional. Custom Performance Total Throughput of the pool (in MiB/s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#total_throughput_mibps NetappStoragePool#total_throughput_mibps}
        :param zone: Specifies the active zone for regional Flex pools. 'zone' and 'replica_zone' values can be swapped to initiate a `zone switch <https://cloud.google.com/netapp/volumes/docs/configure-and-use/storage-pools/edit-or-delete-storage-pool#switch_active_and_replica_zones>`_. If you want to create a zonal Flex pool, specify a zone name for 'location' and omit 'zone'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#zone NetappStoragePool#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetappStoragePoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f1691731abe0e0f37abf1ec7211eaf979387f68339433f7480582a0b11e412)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument capacity_gib", value=capacity_gib, expected_type=type_hints["capacity_gib"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument service_level", value=service_level, expected_type=type_hints["service_level"])
            check_type(argname="argument active_directory", value=active_directory, expected_type=type_hints["active_directory"])
            check_type(argname="argument allow_auto_tiering", value=allow_auto_tiering, expected_type=type_hints["allow_auto_tiering"])
            check_type(argname="argument custom_performance_enabled", value=custom_performance_enabled, expected_type=type_hints["custom_performance_enabled"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_config", value=kms_config, expected_type=type_hints["kms_config"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument ldap_enabled", value=ldap_enabled, expected_type=type_hints["ldap_enabled"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument replica_zone", value=replica_zone, expected_type=type_hints["replica_zone"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument total_iops", value=total_iops, expected_type=type_hints["total_iops"])
            check_type(argname="argument total_throughput_mibps", value=total_throughput_mibps, expected_type=type_hints["total_throughput_mibps"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_gib": capacity_gib,
            "location": location,
            "name": name,
            "network": network,
            "service_level": service_level,
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
        if active_directory is not None:
            self._values["active_directory"] = active_directory
        if allow_auto_tiering is not None:
            self._values["allow_auto_tiering"] = allow_auto_tiering
        if custom_performance_enabled is not None:
            self._values["custom_performance_enabled"] = custom_performance_enabled
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if kms_config is not None:
            self._values["kms_config"] = kms_config
        if labels is not None:
            self._values["labels"] = labels
        if ldap_enabled is not None:
            self._values["ldap_enabled"] = ldap_enabled
        if project is not None:
            self._values["project"] = project
        if replica_zone is not None:
            self._values["replica_zone"] = replica_zone
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if total_iops is not None:
            self._values["total_iops"] = total_iops
        if total_throughput_mibps is not None:
            self._values["total_throughput_mibps"] = total_throughput_mibps
        if zone is not None:
            self._values["zone"] = zone

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
    def capacity_gib(self) -> builtins.str:
        '''Capacity of the storage pool (in GiB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#capacity_gib NetappStoragePool#capacity_gib}
        '''
        result = self._values.get("capacity_gib")
        assert result is not None, "Required property 'capacity_gib' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Name of the location. For zonal Flex pools specify a zone name, in all other cases a region name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#location NetappStoragePool#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name of the storage pool. Needs to be unique per location/region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#name NetappStoragePool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''VPC network name with format: 'projects/{{project}}/global/networks/{{network}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#network NetappStoragePool#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_level(self) -> builtins.str:
        '''Service level of the storage pool. Possible values: ["PREMIUM", "EXTREME", "STANDARD", "FLEX"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#service_level NetappStoragePool#service_level}
        '''
        result = self._values.get("service_level")
        assert result is not None, "Required property 'service_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active_directory(self) -> typing.Optional[builtins.str]:
        '''Specifies the Active Directory policy to be used.

        Format: 'projects/{{project}}/locations/{{location}}/activeDirectories/{{name}}'.
        The policy needs to be in the same location as the storage pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#active_directory NetappStoragePool#active_directory}
        '''
        result = self._values.get("active_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_auto_tiering(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        True if the storage pool supports Auto Tiering enabled volumes. Default is false.
        Auto-tiering can be enabled after storage pool creation but it can't be disabled once enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#allow_auto_tiering NetappStoragePool#allow_auto_tiering}
        '''
        result = self._values.get("allow_auto_tiering")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom_performance_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. True if using Independent Scaling of capacity and performance (Hyperdisk). Default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#custom_performance_enabled NetappStoragePool#custom_performance_enabled}
        '''
        result = self._values.get("custom_performance_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#description NetappStoragePool#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#id NetappStoragePool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_config(self) -> typing.Optional[builtins.str]:
        '''Specifies the CMEK policy to be used for volume encryption.

        Format: 'projects/{{project}}/locations/{{location}}/kmsConfigs/{{name}}'.
        The policy needs to be in the same location as the storage pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#kms_config NetappStoragePool#kms_config}
        '''
        result = self._values.get("kms_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#labels NetappStoragePool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def ldap_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, the volumes uses Active Directory as LDAP name service for UID/GID lookups.

        Required to enable extended group support for NFSv3,
        using security identifiers for NFSv4.1 or principal names for kerberized NFSv4.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#ldap_enabled NetappStoragePool#ldap_enabled}
        '''
        result = self._values.get("ldap_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#project NetappStoragePool#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_zone(self) -> typing.Optional[builtins.str]:
        '''Specifies the replica zone for regional Flex pools. 'zone' and 'replica_zone' values can be swapped to initiate a `zone switch <https://cloud.google.com/netapp/volumes/docs/configure-and-use/storage-pools/edit-or-delete-storage-pool#switch_active_and_replica_zones>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#replica_zone NetappStoragePool#replica_zone}
        '''
        result = self._values.get("replica_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetappStoragePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#timeouts NetappStoragePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetappStoragePoolTimeouts"], result)

    @builtins.property
    def total_iops(self) -> typing.Optional[builtins.str]:
        '''Optional. Custom Performance Total IOPS of the pool If not provided, it will be calculated based on the totalThroughputMibps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#total_iops NetappStoragePool#total_iops}
        '''
        result = self._values.get("total_iops")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def total_throughput_mibps(self) -> typing.Optional[builtins.str]:
        '''Optional. Custom Performance Total Throughput of the pool (in MiB/s).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#total_throughput_mibps NetappStoragePool#total_throughput_mibps}
        '''
        result = self._values.get("total_throughput_mibps")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Specifies the active zone for regional Flex pools.

        'zone' and 'replica_zone' values can be swapped to initiate a
        `zone switch <https://cloud.google.com/netapp/volumes/docs/configure-and-use/storage-pools/edit-or-delete-storage-pool#switch_active_and_replica_zones>`_.
        If you want to create a zonal Flex pool, specify a zone name for 'location' and omit 'zone'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#zone NetappStoragePool#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappStoragePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappStoragePool.NetappStoragePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetappStoragePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#create NetappStoragePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#delete NetappStoragePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#update NetappStoragePool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bea40083f3e0d943b85fde6edfb7b8502e470a44f125176b23d35a0e7a9a785)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#create NetappStoragePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#delete NetappStoragePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_storage_pool#update NetappStoragePool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappStoragePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappStoragePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappStoragePool.NetappStoragePoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86564db9ab3b6d3845a35ee5c101666ac9ac001e1984d09726151a3a35c610b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6ec1b0652b1d6115403553533971c089950d48d4bb080916061cd7c94985fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636d5cb757e72eb51e626c075e13ea66e17861f000f12712356aa7e613b95af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98aea2876973da934b747924445ae7f6453826e5f14357fdb04f6f518854c2a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappStoragePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappStoragePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappStoragePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e654087cc4dad78efa85d96e6eb7be3315830c1174644ce4646de942e9c4f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetappStoragePool",
    "NetappStoragePoolConfig",
    "NetappStoragePoolTimeouts",
    "NetappStoragePoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bd008b4be379c37d0eaad0a24c5b59b9e9a986cb3431b1828a6e93194b484db0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    capacity_gib: builtins.str,
    location: builtins.str,
    name: builtins.str,
    network: builtins.str,
    service_level: builtins.str,
    active_directory: typing.Optional[builtins.str] = None,
    allow_auto_tiering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_performance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_config: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ldap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    replica_zone: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetappStoragePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    total_iops: typing.Optional[builtins.str] = None,
    total_throughput_mibps: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__125cceda74504f1aa60f409cd2f3cd10f633ee75b57e3916f3a45eb9ff56921b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c2ad50be44462fe477c392660931320a86a36033098fc59d6782f338ee7090(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88c031230548a2a6f62124fdc4106f497a649cbe25a7f59f9e15f949f995c07(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd82dff63ba33e498cde52f9c2ea66d7656180cb51292dcaeb8b14490bf61c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f546d45caa2d76e016b107ac811ad6f51054f94a445c0a72ceb2ba5c1c8703a7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a30d7f083700483af811d9aac307bd270744c4de468009cbf82e39ceb6db56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c926ee5d799b850ff5b959daf764fb7a7edb466b9006d958ca51dc50a29c47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3037a9911bb8a4948b79f44b586d60de6be46170301b706f373f13b12cde9f33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3f8ccc0f57090e64d990cad3d99ae71f22b753292d96ddd4cd4ee9b3797d92(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a963c053bb20372cbde76e131d38a0536a266a5919a982bbfbe0e0b05edd0765(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15da61bb1a206f3c1572f80b3f5b4e4de2180a3199b2e18761216f73602d06ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2903c2a94a4d96687ebb3a340e29cd7cea7331a99769993d1f22556de11a1ced(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a4ca1ab0136937b356187736a184179237abcf46c5ad72a016a87cfb6a9be0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e312772d6bf8991c1caf869390dd0e3f2b76057f551ab60b3f1e05c469ae0750(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca5036ecae7822ad3437b7661f4da908098cd58053a4290a66a9fed73d5d2929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d021bd2ad0fb498868acd8f75ecbb1a7664708a4d81c0609308fa60d7d6cde9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a5b60f8c754988f3681b5105069058c7382ca93541a29fe495b73b52b91cee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f77998026b718b0a7ac37df88d8b7129e94bb868b8729bf1ecee621d746fe72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5701ef5e34eca9f209c2acdfc1c4563b50b1747b5c02c6aa29cd25c079bf5d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f1691731abe0e0f37abf1ec7211eaf979387f68339433f7480582a0b11e412(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity_gib: builtins.str,
    location: builtins.str,
    name: builtins.str,
    network: builtins.str,
    service_level: builtins.str,
    active_directory: typing.Optional[builtins.str] = None,
    allow_auto_tiering: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_performance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_config: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ldap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    replica_zone: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetappStoragePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    total_iops: typing.Optional[builtins.str] = None,
    total_throughput_mibps: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bea40083f3e0d943b85fde6edfb7b8502e470a44f125176b23d35a0e7a9a785(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86564db9ab3b6d3845a35ee5c101666ac9ac001e1984d09726151a3a35c610b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ec1b0652b1d6115403553533971c089950d48d4bb080916061cd7c94985fb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636d5cb757e72eb51e626c075e13ea66e17861f000f12712356aa7e613b95af0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98aea2876973da934b747924445ae7f6453826e5f14357fdb04f6f518854c2a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e654087cc4dad78efa85d96e6eb7be3315830c1174644ce4646de942e9c4f46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappStoragePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
