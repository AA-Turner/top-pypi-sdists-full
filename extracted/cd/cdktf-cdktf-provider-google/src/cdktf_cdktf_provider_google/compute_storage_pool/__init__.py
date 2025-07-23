r'''
# `google_compute_storage_pool`

Refer to the Terraform Registry for docs: [`google_compute_storage_pool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool).
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


class ComputeStoragePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeStoragePool.ComputeStoragePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool google_compute_storage_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        pool_provisioned_capacity_gb: builtins.str,
        pool_provisioned_throughput: builtins.str,
        storage_pool_type: builtins.str,
        capacity_provisioning_type: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        performance_provisioning_type: typing.Optional[builtins.str] = None,
        pool_provisioned_iops: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeStoragePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool google_compute_storage_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#name ComputeStoragePool#name}
        :param pool_provisioned_capacity_gb: Size, in GiB, of the storage pool. For more information about the size limits, see https://cloud.google.com/compute/docs/disks/storage-pools. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#pool_provisioned_capacity_gb ComputeStoragePool#pool_provisioned_capacity_gb}
        :param pool_provisioned_throughput: Provisioned throughput, in MB/s, of the storage pool. Only relevant if the storage pool type is 'hyperdisk-balanced' or 'hyperdisk-throughput'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#pool_provisioned_throughput ComputeStoragePool#pool_provisioned_throughput}
        :param storage_pool_type: Type of the storage pool. For example, the following are valid values:. - 'https://www.googleapis.com/compute/v1/projects/{project_id}/zones/{zone}/storagePoolTypes/hyperdisk-balanced' - 'hyperdisk-throughput' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#storage_pool_type ComputeStoragePool#storage_pool_type}
        :param capacity_provisioning_type: Provisioning type of the byte capacity of the pool. Possible values: ["STANDARD", "ADVANCED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#capacity_provisioning_type ComputeStoragePool#capacity_provisioning_type}
        :param deletion_protection: Whether Terraform will be prevented from destroying the StoragePool. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the StoragePool will fail. When the field is set to false, deleting the StoragePool is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#deletion_protection ComputeStoragePool#deletion_protection}
        :param description: A description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#description ComputeStoragePool#description}
        :param performance_provisioning_type: Provisioning type of the performance-related parameters of the pool, such as throughput and IOPS. Possible values: ["STANDARD", "ADVANCED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#performance_provisioning_type ComputeStoragePool#performance_provisioning_type}
        :param pool_provisioned_iops: Provisioned IOPS of the storage pool. Only relevant if the storage pool type is 'hyperdisk-balanced'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#pool_provisioned_iops ComputeStoragePool#pool_provisioned_iops}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#project ComputeStoragePool#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#timeouts ComputeStoragePool#timeouts}
        :param zone: A reference to the zone where the storage pool resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#zone ComputeStoragePool#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fb5c4c51bde8f09294184615b7478580602aad24b685d4ede1b2b54be4ec02)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ComputeStoragePoolConfig(
            name=name,
            pool_provisioned_capacity_gb=pool_provisioned_capacity_gb,
            pool_provisioned_throughput=pool_provisioned_throughput,
            storage_pool_type=storage_pool_type,
            capacity_provisioning_type=capacity_provisioning_type,
            deletion_protection=deletion_protection,
            description=description,
            performance_provisioning_type=performance_provisioning_type,
            pool_provisioned_iops=pool_provisioned_iops,
            project=project,
            timeouts=timeouts,
            zone=zone,
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
        '''Generates CDKTF code for importing a ComputeStoragePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeStoragePool to import.
        :param import_from_id: The id of the existing ComputeStoragePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeStoragePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f99bfcf9dab572c945e399c0ac651499ef5cb673cabdd3f36fdccbad467f6c)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#create ComputeStoragePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#delete ComputeStoragePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#update ComputeStoragePool#update}.
        '''
        value = ComputeStoragePoolTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCapacityProvisioningType")
    def reset_capacity_provisioning_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityProvisioningType", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetPerformanceProvisioningType")
    def reset_performance_provisioning_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerformanceProvisioningType", []))

    @jsii.member(jsii_name="resetPoolProvisionedIops")
    def reset_pool_provisioned_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPoolProvisionedIops", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="labelFingerprint")
    def label_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="resourceStatus")
    def resource_status(self) -> "ComputeStoragePoolResourceStatusList":
        return typing.cast("ComputeStoragePoolResourceStatusList", jsii.get(self, "resourceStatus"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "ComputeStoragePoolStatusList":
        return typing.cast("ComputeStoragePoolStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeStoragePoolTimeoutsOutputReference":
        return typing.cast("ComputeStoragePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="capacityProvisioningTypeInput")
    def capacity_provisioning_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityProvisioningTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="performanceProvisioningTypeInput")
    def performance_provisioning_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "performanceProvisioningTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="poolProvisionedCapacityGbInput")
    def pool_provisioned_capacity_gb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolProvisionedCapacityGbInput"))

    @builtins.property
    @jsii.member(jsii_name="poolProvisionedIopsInput")
    def pool_provisioned_iops_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolProvisionedIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="poolProvisionedThroughputInput")
    def pool_provisioned_throughput_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolProvisionedThroughputInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="storagePoolTypeInput")
    def storage_pool_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storagePoolTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeStoragePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeStoragePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityProvisioningType")
    def capacity_provisioning_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityProvisioningType"))

    @capacity_provisioning_type.setter
    def capacity_provisioning_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f94fac42356bf772ec2c7a1209c0f41c9f517b0257aa03cb1c716bc0dff3f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityProvisioningType", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__ca989df4265c40d2599fb4ce82b2ac085012a50515128668db727d9455940656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4142f6f68b8c84002254e635d60eb4dafb195e15dfa3daed5e18e0aad9b0b1f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea5e1d6a640e4164a0aa4d2617d148a808af5d61dd926cb22990978e3d4a5dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="performanceProvisioningType")
    def performance_provisioning_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "performanceProvisioningType"))

    @performance_provisioning_type.setter
    def performance_provisioning_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb8afff747ef96c4865ae785195e8189f32d2c0e4c1d39057f9d54862ee9381f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performanceProvisioningType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="poolProvisionedCapacityGb")
    def pool_provisioned_capacity_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolProvisionedCapacityGb"))

    @pool_provisioned_capacity_gb.setter
    def pool_provisioned_capacity_gb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f4948c881c67791c1e4d690cb4309059dd619969c68edfeff858b85eaf51df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolProvisionedCapacityGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="poolProvisionedIops")
    def pool_provisioned_iops(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolProvisionedIops"))

    @pool_provisioned_iops.setter
    def pool_provisioned_iops(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a0bb0828ab60aaa1a89691653ceb4f376834180f7ba5589a64e529d7e277013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolProvisionedIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="poolProvisionedThroughput")
    def pool_provisioned_throughput(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolProvisionedThroughput"))

    @pool_provisioned_throughput.setter
    def pool_provisioned_throughput(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7c92e111c49a0df246e4cece3657ebbf33bc91c6591c603f32cdfb8d2bd161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolProvisionedThroughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc254454ad6a81f78350303c320f7482c0869e73d6f7dcf78097b8e01bf2353a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePoolType")
    def storage_pool_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePoolType"))

    @storage_pool_type.setter
    def storage_pool_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93248b9b67905f01c8506074b31c6ed9e04d5056d72e30dd6322635ed96efd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePoolType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f6ec431ef13c456cc7654554b9e147f31b21dc2a0d0d589255cc73b42e2ef0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeStoragePool.ComputeStoragePoolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "pool_provisioned_capacity_gb": "poolProvisionedCapacityGb",
        "pool_provisioned_throughput": "poolProvisionedThroughput",
        "storage_pool_type": "storagePoolType",
        "capacity_provisioning_type": "capacityProvisioningType",
        "deletion_protection": "deletionProtection",
        "description": "description",
        "performance_provisioning_type": "performanceProvisioningType",
        "pool_provisioned_iops": "poolProvisionedIops",
        "project": "project",
        "timeouts": "timeouts",
        "zone": "zone",
    },
)
class ComputeStoragePoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        pool_provisioned_capacity_gb: builtins.str,
        pool_provisioned_throughput: builtins.str,
        storage_pool_type: builtins.str,
        capacity_provisioning_type: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        performance_provisioning_type: typing.Optional[builtins.str] = None,
        pool_provisioned_iops: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeStoragePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#name ComputeStoragePool#name}
        :param pool_provisioned_capacity_gb: Size, in GiB, of the storage pool. For more information about the size limits, see https://cloud.google.com/compute/docs/disks/storage-pools. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#pool_provisioned_capacity_gb ComputeStoragePool#pool_provisioned_capacity_gb}
        :param pool_provisioned_throughput: Provisioned throughput, in MB/s, of the storage pool. Only relevant if the storage pool type is 'hyperdisk-balanced' or 'hyperdisk-throughput'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#pool_provisioned_throughput ComputeStoragePool#pool_provisioned_throughput}
        :param storage_pool_type: Type of the storage pool. For example, the following are valid values:. - 'https://www.googleapis.com/compute/v1/projects/{project_id}/zones/{zone}/storagePoolTypes/hyperdisk-balanced' - 'hyperdisk-throughput' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#storage_pool_type ComputeStoragePool#storage_pool_type}
        :param capacity_provisioning_type: Provisioning type of the byte capacity of the pool. Possible values: ["STANDARD", "ADVANCED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#capacity_provisioning_type ComputeStoragePool#capacity_provisioning_type}
        :param deletion_protection: Whether Terraform will be prevented from destroying the StoragePool. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the StoragePool will fail. When the field is set to false, deleting the StoragePool is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#deletion_protection ComputeStoragePool#deletion_protection}
        :param description: A description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#description ComputeStoragePool#description}
        :param performance_provisioning_type: Provisioning type of the performance-related parameters of the pool, such as throughput and IOPS. Possible values: ["STANDARD", "ADVANCED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#performance_provisioning_type ComputeStoragePool#performance_provisioning_type}
        :param pool_provisioned_iops: Provisioned IOPS of the storage pool. Only relevant if the storage pool type is 'hyperdisk-balanced'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#pool_provisioned_iops ComputeStoragePool#pool_provisioned_iops}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#project ComputeStoragePool#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#timeouts ComputeStoragePool#timeouts}
        :param zone: A reference to the zone where the storage pool resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#zone ComputeStoragePool#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ComputeStoragePoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa780a6193f1cc18bcada00a807276e25c67aeabb84ed63256f80c0c9512eff)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pool_provisioned_capacity_gb", value=pool_provisioned_capacity_gb, expected_type=type_hints["pool_provisioned_capacity_gb"])
            check_type(argname="argument pool_provisioned_throughput", value=pool_provisioned_throughput, expected_type=type_hints["pool_provisioned_throughput"])
            check_type(argname="argument storage_pool_type", value=storage_pool_type, expected_type=type_hints["storage_pool_type"])
            check_type(argname="argument capacity_provisioning_type", value=capacity_provisioning_type, expected_type=type_hints["capacity_provisioning_type"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument performance_provisioning_type", value=performance_provisioning_type, expected_type=type_hints["performance_provisioning_type"])
            check_type(argname="argument pool_provisioned_iops", value=pool_provisioned_iops, expected_type=type_hints["pool_provisioned_iops"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "pool_provisioned_capacity_gb": pool_provisioned_capacity_gb,
            "pool_provisioned_throughput": pool_provisioned_throughput,
            "storage_pool_type": storage_pool_type,
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
        if capacity_provisioning_type is not None:
            self._values["capacity_provisioning_type"] = capacity_provisioning_type
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if description is not None:
            self._values["description"] = description
        if performance_provisioning_type is not None:
            self._values["performance_provisioning_type"] = performance_provisioning_type
        if pool_provisioned_iops is not None:
            self._values["pool_provisioned_iops"] = pool_provisioned_iops
        if project is not None:
            self._values["project"] = project
        if timeouts is not None:
            self._values["timeouts"] = timeouts
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
    def name(self) -> builtins.str:
        '''Name of the resource.

        Provided by the client when the resource is created.
        The name must be 1-63 characters long, and comply with RFC1035.
        Specifically, the name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'
        which means the first character must be a lowercase letter,
        and all following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#name ComputeStoragePool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pool_provisioned_capacity_gb(self) -> builtins.str:
        '''Size, in GiB, of the storage pool. For more information about the size limits, see https://cloud.google.com/compute/docs/disks/storage-pools.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#pool_provisioned_capacity_gb ComputeStoragePool#pool_provisioned_capacity_gb}
        '''
        result = self._values.get("pool_provisioned_capacity_gb")
        assert result is not None, "Required property 'pool_provisioned_capacity_gb' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pool_provisioned_throughput(self) -> builtins.str:
        '''Provisioned throughput, in MB/s, of the storage pool. Only relevant if the storage pool type is 'hyperdisk-balanced' or 'hyperdisk-throughput'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#pool_provisioned_throughput ComputeStoragePool#pool_provisioned_throughput}
        '''
        result = self._values.get("pool_provisioned_throughput")
        assert result is not None, "Required property 'pool_provisioned_throughput' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_pool_type(self) -> builtins.str:
        '''Type of the storage pool. For example, the following are valid values:.

        - 'https://www.googleapis.com/compute/v1/projects/{project_id}/zones/{zone}/storagePoolTypes/hyperdisk-balanced'
        - 'hyperdisk-throughput'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#storage_pool_type ComputeStoragePool#storage_pool_type}
        '''
        result = self._values.get("storage_pool_type")
        assert result is not None, "Required property 'storage_pool_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity_provisioning_type(self) -> typing.Optional[builtins.str]:
        '''Provisioning type of the byte capacity of the pool. Possible values: ["STANDARD", "ADVANCED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#capacity_provisioning_type ComputeStoragePool#capacity_provisioning_type}
        '''
        result = self._values.get("capacity_provisioning_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Terraform will be prevented from destroying the StoragePool.

        When the field is set to true or unset in Terraform state, a 'terraform apply'
        or 'terraform destroy' that would delete the StoragePool will fail.
        When the field is set to false, deleting the StoragePool is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#deletion_protection ComputeStoragePool#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#description ComputeStoragePool#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def performance_provisioning_type(self) -> typing.Optional[builtins.str]:
        '''Provisioning type of the performance-related parameters of the pool, such as throughput and IOPS. Possible values: ["STANDARD", "ADVANCED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#performance_provisioning_type ComputeStoragePool#performance_provisioning_type}
        '''
        result = self._values.get("performance_provisioning_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pool_provisioned_iops(self) -> typing.Optional[builtins.str]:
        '''Provisioned IOPS of the storage pool. Only relevant if the storage pool type is 'hyperdisk-balanced'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#pool_provisioned_iops ComputeStoragePool#pool_provisioned_iops}
        '''
        result = self._values.get("pool_provisioned_iops")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#project ComputeStoragePool#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeStoragePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#timeouts ComputeStoragePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeStoragePoolTimeouts"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''A reference to the zone where the storage pool resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#zone ComputeStoragePool#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeStoragePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeStoragePool.ComputeStoragePoolResourceStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeStoragePoolResourceStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeStoragePoolResourceStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeStoragePoolResourceStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeStoragePool.ComputeStoragePoolResourceStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54098287ece9b5aae825a37f71cfe1aaf4b5f71c881cecb5f3152d0b70f29871)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeStoragePoolResourceStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163dd3d5e2a3bf508090607e616c585b0e480c7806f937bd0ee80935a0ca229c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeStoragePoolResourceStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1aa48bbf29f66c7015a3a25d40f87e690caef2f10060f65ba5b1a65ed4d4c8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dff660f6718a31a0efd965de4a2031fed2ef8be9f7c6a7b902c0c8712327e19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7994915e2b122436769eab93103c05c44481ab1425c1897cef949ccd6ec68117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeStoragePoolResourceStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeStoragePool.ComputeStoragePoolResourceStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d68c961f8091fa6c655ed7de2c539470f00df5784baefec0e38d80b1fca8b413)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="diskCount")
    def disk_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskCount"))

    @builtins.property
    @jsii.member(jsii_name="lastResizeTimestamp")
    def last_resize_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastResizeTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="maxTotalProvisionedDiskCapacityGb")
    def max_total_provisioned_disk_capacity_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxTotalProvisionedDiskCapacityGb"))

    @builtins.property
    @jsii.member(jsii_name="poolUsedCapacityBytes")
    def pool_used_capacity_bytes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolUsedCapacityBytes"))

    @builtins.property
    @jsii.member(jsii_name="poolUsedIops")
    def pool_used_iops(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolUsedIops"))

    @builtins.property
    @jsii.member(jsii_name="poolUsedThroughput")
    def pool_used_throughput(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolUsedThroughput"))

    @builtins.property
    @jsii.member(jsii_name="poolUserWrittenBytes")
    def pool_user_written_bytes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolUserWrittenBytes"))

    @builtins.property
    @jsii.member(jsii_name="totalProvisionedDiskCapacityGb")
    def total_provisioned_disk_capacity_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalProvisionedDiskCapacityGb"))

    @builtins.property
    @jsii.member(jsii_name="totalProvisionedDiskIops")
    def total_provisioned_disk_iops(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalProvisionedDiskIops"))

    @builtins.property
    @jsii.member(jsii_name="totalProvisionedDiskThroughput")
    def total_provisioned_disk_throughput(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalProvisionedDiskThroughput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeStoragePoolResourceStatus]:
        return typing.cast(typing.Optional[ComputeStoragePoolResourceStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeStoragePoolResourceStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c76c696610e1deb4073919df4fd4094c7f992586124ec823056d7266dd5c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeStoragePool.ComputeStoragePoolStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class ComputeStoragePoolStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeStoragePoolStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeStoragePoolStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeStoragePool.ComputeStoragePoolStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b6984ca3a63f520a7ef59bec0ec45001650606643852d397c19a1c47710db82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeStoragePoolStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3af34b3bf6dd1f55ee28f9dc6093942b7924f954df1329a307b7b405f02ed4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeStoragePoolStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b99f76b56e0b7a3451f39b6d05157c9dde985919072a4e48b5a92950a72973)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71c1dbf24b67575f046c08167a6838b4603e85c2e27346f7156cc2ea01da44da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bbbfeaa8dc12705ecc950ac226cd51d39e66729422dddd14039e95aed8ab36a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ComputeStoragePoolStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeStoragePool.ComputeStoragePoolStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b2e9a45470c89715b83cffefeccd45be032357422128d32ea4ea8e20f35b26a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="diskCount")
    def disk_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskCount"))

    @builtins.property
    @jsii.member(jsii_name="lastResizeTimestamp")
    def last_resize_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastResizeTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="maxTotalProvisionedDiskCapacityGb")
    def max_total_provisioned_disk_capacity_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxTotalProvisionedDiskCapacityGb"))

    @builtins.property
    @jsii.member(jsii_name="poolUsedCapacityBytes")
    def pool_used_capacity_bytes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolUsedCapacityBytes"))

    @builtins.property
    @jsii.member(jsii_name="poolUsedIops")
    def pool_used_iops(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolUsedIops"))

    @builtins.property
    @jsii.member(jsii_name="poolUsedThroughput")
    def pool_used_throughput(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolUsedThroughput"))

    @builtins.property
    @jsii.member(jsii_name="poolUserWrittenBytes")
    def pool_user_written_bytes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolUserWrittenBytes"))

    @builtins.property
    @jsii.member(jsii_name="totalProvisionedDiskCapacityGb")
    def total_provisioned_disk_capacity_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalProvisionedDiskCapacityGb"))

    @builtins.property
    @jsii.member(jsii_name="totalProvisionedDiskIops")
    def total_provisioned_disk_iops(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalProvisionedDiskIops"))

    @builtins.property
    @jsii.member(jsii_name="totalProvisionedDiskThroughput")
    def total_provisioned_disk_throughput(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalProvisionedDiskThroughput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeStoragePoolStatus]:
        return typing.cast(typing.Optional[ComputeStoragePoolStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeStoragePoolStatus]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87db00f6ee48cb3e5b4decef3a77251c9db53c4f781d02b59a28a51cfdd1e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeStoragePool.ComputeStoragePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeStoragePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#create ComputeStoragePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#delete ComputeStoragePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#update ComputeStoragePool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3c7ada97e2c36160628d3d4e8d275303dc9dba8ec9ce6feec820fcd3de3b57)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#create ComputeStoragePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#delete ComputeStoragePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_storage_pool#update ComputeStoragePool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeStoragePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeStoragePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeStoragePool.ComputeStoragePoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c4a88c586970822423cde4f2647f77f179bd437a5388c6f5fcce1a53a7cd2f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd3d6d91eb784d247d501d9839691332630d50362e75f50cfb62bc20f8239551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292e2a43794e7fa7c7c3b32ea01a11780c11ab0d83214e4a223701d8ec20c325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38b558be4aa25d2323fef7724b10fc4d537d226e8c674935c9cc89a6948b7ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeStoragePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeStoragePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeStoragePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c810b6f14136c10fc04afc5ad2b07c22f4345fd7c30c6aa5ce6214d2ea9b059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeStoragePool",
    "ComputeStoragePoolConfig",
    "ComputeStoragePoolResourceStatus",
    "ComputeStoragePoolResourceStatusList",
    "ComputeStoragePoolResourceStatusOutputReference",
    "ComputeStoragePoolStatus",
    "ComputeStoragePoolStatusList",
    "ComputeStoragePoolStatusOutputReference",
    "ComputeStoragePoolTimeouts",
    "ComputeStoragePoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d4fb5c4c51bde8f09294184615b7478580602aad24b685d4ede1b2b54be4ec02(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    pool_provisioned_capacity_gb: builtins.str,
    pool_provisioned_throughput: builtins.str,
    storage_pool_type: builtins.str,
    capacity_provisioning_type: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    performance_provisioning_type: typing.Optional[builtins.str] = None,
    pool_provisioned_iops: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeStoragePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__90f99bfcf9dab572c945e399c0ac651499ef5cb673cabdd3f36fdccbad467f6c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f94fac42356bf772ec2c7a1209c0f41c9f517b0257aa03cb1c716bc0dff3f1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca989df4265c40d2599fb4ce82b2ac085012a50515128668db727d9455940656(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4142f6f68b8c84002254e635d60eb4dafb195e15dfa3daed5e18e0aad9b0b1f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea5e1d6a640e4164a0aa4d2617d148a808af5d61dd926cb22990978e3d4a5dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8afff747ef96c4865ae785195e8189f32d2c0e4c1d39057f9d54862ee9381f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f4948c881c67791c1e4d690cb4309059dd619969c68edfeff858b85eaf51df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0bb0828ab60aaa1a89691653ceb4f376834180f7ba5589a64e529d7e277013(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7c92e111c49a0df246e4cece3657ebbf33bc91c6591c603f32cdfb8d2bd161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc254454ad6a81f78350303c320f7482c0869e73d6f7dcf78097b8e01bf2353a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93248b9b67905f01c8506074b31c6ed9e04d5056d72e30dd6322635ed96efd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6ec431ef13c456cc7654554b9e147f31b21dc2a0d0d589255cc73b42e2ef0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa780a6193f1cc18bcada00a807276e25c67aeabb84ed63256f80c0c9512eff(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    pool_provisioned_capacity_gb: builtins.str,
    pool_provisioned_throughput: builtins.str,
    storage_pool_type: builtins.str,
    capacity_provisioning_type: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    performance_provisioning_type: typing.Optional[builtins.str] = None,
    pool_provisioned_iops: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeStoragePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54098287ece9b5aae825a37f71cfe1aaf4b5f71c881cecb5f3152d0b70f29871(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163dd3d5e2a3bf508090607e616c585b0e480c7806f937bd0ee80935a0ca229c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1aa48bbf29f66c7015a3a25d40f87e690caef2f10060f65ba5b1a65ed4d4c8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dff660f6718a31a0efd965de4a2031fed2ef8be9f7c6a7b902c0c8712327e19(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7994915e2b122436769eab93103c05c44481ab1425c1897cef949ccd6ec68117(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68c961f8091fa6c655ed7de2c539470f00df5784baefec0e38d80b1fca8b413(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c76c696610e1deb4073919df4fd4094c7f992586124ec823056d7266dd5c1e(
    value: typing.Optional[ComputeStoragePoolResourceStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6984ca3a63f520a7ef59bec0ec45001650606643852d397c19a1c47710db82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3af34b3bf6dd1f55ee28f9dc6093942b7924f954df1329a307b7b405f02ed4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b99f76b56e0b7a3451f39b6d05157c9dde985919072a4e48b5a92950a72973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c1dbf24b67575f046c08167a6838b4603e85c2e27346f7156cc2ea01da44da(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbbfeaa8dc12705ecc950ac226cd51d39e66729422dddd14039e95aed8ab36a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2e9a45470c89715b83cffefeccd45be032357422128d32ea4ea8e20f35b26a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87db00f6ee48cb3e5b4decef3a77251c9db53c4f781d02b59a28a51cfdd1e79(
    value: typing.Optional[ComputeStoragePoolStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3c7ada97e2c36160628d3d4e8d275303dc9dba8ec9ce6feec820fcd3de3b57(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4a88c586970822423cde4f2647f77f179bd437a5388c6f5fcce1a53a7cd2f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3d6d91eb784d247d501d9839691332630d50362e75f50cfb62bc20f8239551(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292e2a43794e7fa7c7c3b32ea01a11780c11ab0d83214e4a223701d8ec20c325(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b558be4aa25d2323fef7724b10fc4d537d226e8c674935c9cc89a6948b7ead(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c810b6f14136c10fc04afc5ad2b07c22f4345fd7c30c6aa5ce6214d2ea9b059(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeStoragePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
